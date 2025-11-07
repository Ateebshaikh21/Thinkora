from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Dict
import logging
from models.schemas import StudySession
from database.db_connection import get_sessions_collection
from ai_engine.question_generator import QuestionGenerator
from utils.session_manager import session_manager
import random
import csv
import io

router = APIRouter()

@router.post("/quiz/generate/{session_id}")
async def generate_quiz(session_id: str, question_count: int = 20):
    """
    Generate a quiz with realistic questions and answers from session content
    """
    try:
        sessions_collection = get_sessions_collection()
        
        # Get study session (try database first, fallback to file storage)
        session = None
        
        if sessions_collection:
            try:
                session = await sessions_collection.find_one({"_id": session_id})
            except Exception as e:
                logging.warning(f"Database read failed, trying file storage: {e}")
        
        if not session:
            # Try file-based session storage
            session = session_manager.get_session(session_id)
            
        if not session:
            raise HTTPException(status_code=404, detail="Study session not found")
        
        # Check if session has questions
        if not session.get("question_set"):
            raise HTTPException(status_code=400, detail="Session has no questions available for quiz")
        
        # Get all content from documents
        all_content = ""
        for doc in session.get("documents", []):
            all_content += doc.get("content", "") + "\n\n"
        
        if not all_content.strip():
            raise HTTPException(status_code=400, detail="No content available for quiz generation")
        
        # Get existing questions
        question_set = session["question_set"]
        existing_questions = []
        existing_questions.extend(question_set.get("frequent_questions", []))
        existing_questions.extend(question_set.get("moderate_questions", []))
        existing_questions.extend(question_set.get("important_questions", []))
        existing_questions.extend(question_set.get("predicted_questions", []))
        
        if len(existing_questions) < question_count:
            raise HTTPException(
                status_code=400, 
                detail=f"Not enough questions available. Need {question_count}, have {len(existing_questions)}"
            )
        
        # Shuffle existing questions to ensure variety on each attempt
        random.shuffle(existing_questions)
        
        # Initialize question generator
        question_generator = QuestionGenerator()
        
        # Generate quiz questions with realistic answers
        # Each call will produce different questions due to shuffling
        quiz_questions = question_generator.generate_quiz_questions(
            content=all_content,
            existing_questions=existing_questions,
            count=question_count
        )
        
        return {
            "session_id": session_id,
            "questions": quiz_questions,
            "total_questions": len(quiz_questions),
            "time_limit": 1800,  # 30 minutes
            "instructions": "Select the best answer for each question. You have 30 minutes to complete the quiz."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error generating quiz: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate quiz")

@router.post("/quiz/submit")
async def submit_quiz(quiz_data: Dict):
    """
    Submit quiz answers, calculate score, and provide AI feedback
    """
    try:
        session_id = quiz_data.get("session_id")
        answers = quiz_data.get("answers", {})
        questions = quiz_data.get("questions", [])
        time_taken = quiz_data.get("time_taken", 0)
        user_id = quiz_data.get("user_id", "demo_user")
        
        if not session_id or not questions:
            raise HTTPException(status_code=400, detail="Missing required quiz data")
        
        # Calculate score
        correct_answers = 0
        total_marks = 0
        earned_marks = 0
        detailed_results = []
        topic_performance = {}
        
        for question in questions:
            question_id = str(question["id"])
            user_answer = answers.get(question_id)
            correct_answer = question["correct_answer"]
            marks = question.get("marks", 1)
            topic = question.get("topic", "General")
            
            total_marks += marks
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct_answers += 1
                earned_marks += marks
            
            # Track performance by topic
            if topic not in topic_performance:
                topic_performance[topic] = {"correct": 0, "total": 0}
            topic_performance[topic]["total"] += 1
            if is_correct:
                topic_performance[topic]["correct"] += 1
            
            detailed_results.append({
                "question_id": question_id,
                "question_text": question["text"],
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "marks": marks,
                "explanation": question.get("explanation", ""),
                "topic": topic
            })
        
        # Calculate percentage
        percentage = (earned_marks / total_marks * 100) if total_marks > 0 else 0
        
        # Determine grade
        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 50:
            grade = "D"
        else:
            grade = "F"
        
        # Generate AI feedback based on performance
        ai_feedback = _generate_ai_feedback(
            percentage=percentage,
            correct_answers=correct_answers,
            total_questions=len(questions),
            time_taken=time_taken,
            topic_performance=topic_performance,
            grade=grade
        )
        
        # Calculate weak and strong areas
        weak_areas = []
        strong_areas = []
        for topic, perf in topic_performance.items():
            topic_percentage = (perf["correct"] / perf["total"] * 100) if perf["total"] > 0 else 0
            if topic_percentage < 60:
                weak_areas.append(topic)
            elif topic_percentage >= 80:
                strong_areas.append(topic)
        
        from datetime import datetime
        quiz_result = {
            "session_id": session_id,
            "user_id": user_id,
            "total_questions": len(questions),
            "correct_answers": correct_answers,
            "total_marks": total_marks,
            "earned_marks": earned_marks,
            "percentage": round(percentage, 1),
            "grade": grade,
            "time_taken": time_taken,
            "detailed_results": detailed_results,
            "topic_performance": topic_performance,
            "weak_areas": weak_areas,
            "strong_areas": strong_areas,
            "ai_feedback": ai_feedback,
            "completed_at": datetime.now().isoformat()
        }
        
        # Save quiz result to storage
        _save_quiz_result(session_id, user_id, quiz_result)
        
        return quiz_result
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error submitting quiz: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit quiz")

def _generate_ai_feedback(percentage: float, correct_answers: int, total_questions: int, 
                         time_taken: int, topic_performance: Dict, grade: str) -> Dict:
    """Generate personalized AI feedback based on quiz performance"""
    
    # Overall assessment
    if percentage >= 90:
        overall = "Excellent work! You have demonstrated a strong understanding of the subject matter."
        mastery_level = "Expert"
        recommendation = "You've mastered this topic! Consider exploring advanced concepts or helping others learn."
    elif percentage >= 80:
        overall = "Great job! You have a solid grasp of the material with minor areas for improvement."
        mastery_level = "Advanced"
        recommendation = "You're doing very well! Review the questions you missed to achieve mastery."
    elif percentage >= 70:
        overall = "Good effort! You understand most concepts but need to strengthen some areas."
        mastery_level = "Intermediate"
        recommendation = "You're on the right track. Focus on the topics where you struggled and retake the quiz."
    elif percentage >= 60:
        overall = "Fair performance. You have basic understanding but need more practice."
        mastery_level = "Beginner"
        recommendation = "Review the study materials thoroughly and practice more questions in weak areas."
    elif percentage >= 50:
        overall = "You're making progress, but significant improvement is needed."
        mastery_level = "Novice"
        recommendation = "Spend more time studying the fundamentals. Consider reviewing notes and examples carefully."
    else:
        overall = "You need substantial improvement in understanding this subject."
        mastery_level = "Needs Improvement"
        recommendation = "Don't be discouraged! Start with the basics, review all materials, and seek help if needed."
    
    # Time analysis
    avg_time_per_question = time_taken / total_questions if total_questions > 0 else 0
    if avg_time_per_question < 30:
        time_feedback = "You completed the quiz quickly. Make sure you're reading questions carefully."
    elif avg_time_per_question > 120:
        time_feedback = "You took your time with each question, which shows careful consideration."
    else:
        time_feedback = "Your pacing was good, balancing speed with accuracy."
    
    # Learning status
    if percentage >= 75:
        learning_status = "✅ Subject Learned Successfully"
        learning_message = "You have demonstrated sufficient understanding of this subject. You're ready to move forward!"
    elif percentage >= 60:
        learning_status = "⚠️ Partial Understanding"
        learning_message = "You have a basic understanding but need more practice to fully master the subject."
    else:
        learning_status = "❌ Needs More Study"
        learning_message = "You need to spend more time studying this subject before moving forward."
    
    # Specific suggestions
    suggestions = []
    if percentage < 75:
        suggestions.append("Retake the quiz after reviewing the material to improve your score")
        suggestions.append("Focus on understanding concepts rather than memorizing answers")
    
    if avg_time_per_question < 30:
        suggestions.append("Take more time to read and understand each question carefully")
    
    # Topic-specific feedback
    topic_feedback = []
    for topic, perf in topic_performance.items():
        topic_percentage = (perf["correct"] / perf["total"] * 100) if perf["total"] > 0 else 0
        if topic_percentage < 60:
            topic_feedback.append(f"Need improvement in: {topic} ({perf['correct']}/{perf['total']} correct)")
        elif topic_percentage == 100:
            topic_feedback.append(f"Perfect score in: {topic} ({perf['correct']}/{perf['total']} correct)")
    
    return {
        "overall_assessment": overall,
        "mastery_level": mastery_level,
        "learning_status": learning_status,
        "learning_message": learning_message,
        "recommendation": recommendation,
        "time_feedback": time_feedback,
        "suggestions": suggestions,
        "topic_feedback": topic_feedback,
        "ready_to_advance": percentage >= 75
    }

def _save_quiz_result(session_id: str, user_id: str, quiz_result: Dict):
    """Save quiz result to file storage"""
    import os
    import json
    from datetime import datetime
    
    # Create quiz results directory
    results_dir = "quiz_results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Create session-specific directory
    session_dir = os.path.join(results_dir, session_id)
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"quiz_{timestamp}.json"
    filepath = os.path.join(session_dir, filename)
    
    # Save quiz result
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(quiz_result, f, indent=2, ensure_ascii=False)
        logging.info(f"Quiz result saved: {filepath}")
    except Exception as e:
        logging.error(f"Failed to save quiz result: {e}")

@router.get("/quiz/download/{session_id}")
async def download_quiz_csv(session_id: str):
    """
    Download quiz questions and answers as CSV file
    """
    try:
        sessions_collection = get_sessions_collection()
        
        # Get study session
        session = None
        if sessions_collection:
            try:
                session = await sessions_collection.find_one({"_id": session_id})
            except Exception as e:
                logging.warning(f"Database read failed, trying file storage: {e}")
        
        if not session:
            session = session_manager.get_session(session_id)
            
        if not session:
            raise HTTPException(status_code=404, detail="Study session not found")
        
        # Get all content from documents
        all_content = ""
        for doc in session.get("documents", []):
            all_content += doc.get("content", "") + "\n\n"
        
        # Get existing questions
        question_set = session.get("question_set", {})
        existing_questions = []
        existing_questions.extend(question_set.get("frequent_questions", []))
        existing_questions.extend(question_set.get("moderate_questions", []))
        existing_questions.extend(question_set.get("important_questions", []))
        existing_questions.extend(question_set.get("predicted_questions", []))
        
        if not existing_questions:
            raise HTTPException(status_code=400, detail="No questions available for this session")
        
        # Generate quiz questions
        question_generator = QuestionGenerator()
        quiz_questions = question_generator.generate_quiz_questions(
            content=all_content,
            existing_questions=existing_questions,
            count=min(20, len(existing_questions))
        )
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Question Number',
            'Question',
            'Option A',
            'Option B',
            'Option C',
            'Option D',
            'Correct Answer',
            'Explanation',
            'Topic',
            'Marks'
        ])
        
        # Write questions
        for i, q in enumerate(quiz_questions, 1):
            options = q.get('options', [])
            correct_index = q.get('correct_answer', 0)
            correct_letter = chr(65 + correct_index)  # Convert 0->A, 1->B, etc.
            
            writer.writerow([
                i,
                q.get('text', ''),
                options[0] if len(options) > 0 else '',
                options[1] if len(options) > 1 else '',
                options[2] if len(options) > 2 else '',
                options[3] if len(options) > 3 else '',
                f"{correct_letter} - {options[correct_index] if correct_index < len(options) else ''}",
                q.get('explanation', ''),
                q.get('topic', 'General'),
                q.get('marks', 1)
            ])
        
        # Prepare response
        output.seek(0)
        
        # Get session name for filename
        session_name = session.get('display_name', session.get('subject', 'quiz'))
        safe_name = "".join(c for c in session_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_quiz_{timestamp}.csv"
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error generating CSV: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate CSV file")

@router.get("/quiz/history/{session_id}")
async def get_quiz_history(session_id: str, user_id: str = "demo_user"):
    """
    Get quiz attempt history for a session
    """
    try:
        import os
        import json
        from datetime import datetime
        
        results_dir = os.path.join("quiz_results", session_id)
        
        if not os.path.exists(results_dir):
            return {
                "session_id": session_id,
                "quiz_attempts": [],
                "total_attempts": 0,
                "best_score": None,
                "average_score": None,
                "latest_attempt": None
            }
        
        # Load all quiz results for this session
        quiz_attempts = []
        for filename in os.listdir(results_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(results_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        result = json.load(f)
                        # Filter by user_id if needed
                        if result.get("user_id") == user_id:
                            quiz_attempts.append(result)
                except Exception as e:
                    logging.error(f"Error loading quiz result {filepath}: {e}")
        
        # Sort by completion time (most recent first)
        quiz_attempts.sort(key=lambda x: x.get("completed_at", ""), reverse=True)
        
        # Calculate statistics
        total_attempts = len(quiz_attempts)
        
        if total_attempts > 0:
            scores = [attempt.get("percentage", 0) for attempt in quiz_attempts]
            best_score = max(scores)
            average_score = sum(scores) / len(scores)
            latest_attempt = quiz_attempts[0]
            
            # Calculate improvement trend
            if total_attempts >= 2:
                recent_scores = scores[:min(3, total_attempts)]
                improvement = recent_scores[0] - recent_scores[-1]
            else:
                improvement = 0
        else:
            best_score = None
            average_score = None
            latest_attempt = None
            improvement = 0
        
        return {
            "session_id": session_id,
            "quiz_attempts": quiz_attempts,
            "total_attempts": total_attempts,
            "best_score": round(best_score, 1) if best_score is not None else None,
            "average_score": round(average_score, 1) if average_score is not None else None,
            "latest_attempt": latest_attempt,
            "improvement_trend": round(improvement, 1) if improvement != 0 else 0
        }
        
    except Exception as e:
        logging.error(f"Error getting quiz history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get quiz history")