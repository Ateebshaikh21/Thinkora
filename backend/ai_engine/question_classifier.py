from typing import List, Dict, Tuple
from models.schemas import Question, QuestionCategory, QuestionSet
import random
import logging
from .nlp_analysis import NLPAnalyzer

class QuestionClassifier:
    def __init__(self):
        self.nlp_analyzer = NLPAnalyzer()
        
    def classify_questions(self, questions: List[Dict], document_type: str = "mixed") -> QuestionSet:
        """
        Classify questions into different categories with fixed distribution:
        - Frequent: 6 questions
        - Moderate: 6 questions  
        - Important: 6 questions
        - Predicted: 4 questions
        Total: 22 questions
        
        Now accepts questions as dictionaries with 'text' and 'marks' keys
        """
        if not questions:
            return QuestionSet()
        
        # Convert old format to new format if needed
        if isinstance(questions[0], str):
            questions = [{'text': q, 'marks': 5, 'marks_inferred': True} for q in questions]
        
        # Ensure we have enough questions, duplicate if necessary
        if len(questions) < 22:
            # Duplicate questions to reach minimum count
            original_count = len(questions)
            while len(questions) < 22:
                questions.extend(questions[:min(22-len(questions), original_count)])
        
        # Extract question texts for clustering
        question_texts = [q['text'] for q in questions]
        question_clusters = self.nlp_analyzer.cluster_similar_questions(question_texts)
        frequency_map = self.nlp_analyzer.analyze_question_frequency(question_clusters)
        
        # Create Question objects with REAL marks from PDF
        classified_questions = []
        
        for question_data in questions:
            question_text = question_data['text']
            actual_marks = question_data.get('marks', 5)  # Use REAL marks from PDF
            
            # Enhanced analysis for each question
            category = self._determine_category_by_marks(question_text, actual_marks, frequency_map, document_type)
            confidence = self._calculate_confidence(question_text, frequency_map)
            
            question = Question(
                text=question_text,
                category=category,
                confidence_score=confidence,
                topic=self._extract_topic(question_text),
                difficulty=self._assess_difficulty_by_marks(question_text, actual_marks),
                source=document_type,
                marks_weightage=actual_marks  # Use ACTUAL marks from PDF
            )
            classified_questions.append(question)
        
        # Organize into QuestionSet with fixed distribution
        return self._organize_question_set_fixed(classified_questions)
    
    def _determine_category_by_marks(self, question: str, marks: int, frequency_map: Dict[str, int], doc_type: str) -> QuestionCategory:
        """
        Determine the category of a question based on ACTUAL marks from PDF and other factors
        """
        frequency = frequency_map.get(question, 1)
        question_lower = question.lower()
        
        # Primary categorization based on ACTUAL marks from PDF
        if marks >= 12:  # High marks questions are usually Important
            return QuestionCategory.IMPORTANT
        elif marks >= 8:  # Medium-high marks
            # Check if it's application/modern topic for Predicted
            if any(keyword in question_lower for keyword in ['application', 'future', 'trend', 'impact', 'recent', 'modern', 'current']):
                return QuestionCategory.PREDICTED
            else:
                return QuestionCategory.IMPORTANT
        elif marks >= 5:  # Medium marks
            # Check frequency and keywords
            if frequency > 2 or any(keyword in question_lower for keyword in ['basic', 'define', 'what is', 'meaning']):
                return QuestionCategory.FREQUENT
            else:
                return QuestionCategory.MODERATE
        else:  # Low marks (2-4)
            return QuestionCategory.FREQUENT
    
    def _assess_difficulty_by_marks(self, question: str, marks: int) -> str:
        """
        Assess difficulty based on ACTUAL marks from PDF
        """
        if marks >= 12:
            return "Hard"
        elif marks >= 6:
            return "Medium"
        else:
            return "Easy"
    
    def _determine_category(self, question: str, frequency_map: Dict[str, int], doc_type: str) -> QuestionCategory:
        """
        Determine the category of a question based on various factors
        """
        frequency = frequency_map.get(question, 1)
        
        # Keywords that indicate different categories
        frequent_keywords = ['basic', 'define', 'what is', 'meaning', 'introduction']
        important_keywords = ['explain', 'describe', 'analyze', 'compare', 'discuss']
        predicted_keywords = ['future', 'trend', 'impact', 'application', 'recent']
        
        question_lower = question.lower()
        
        # High frequency questions are usually frequent
        if frequency > 3:
            return QuestionCategory.FREQUENT
        
        # Check for keyword patterns
        if any(keyword in question_lower for keyword in predicted_keywords):
            return QuestionCategory.PREDICTED
        elif any(keyword in question_lower for keyword in important_keywords):
            return QuestionCategory.IMPORTANT
        elif any(keyword in question_lower for keyword in frequent_keywords):
            return QuestionCategory.FREQUENT
        else:
            return QuestionCategory.MODERATE
    
    def _calculate_confidence(self, question: str, frequency_map: Dict[str, int]) -> float:
        """
        Calculate confidence score for the classification
        """
        base_confidence = 0.7
        frequency = frequency_map.get(question, 1)
        
        # Higher frequency increases confidence
        frequency_boost = min(frequency * 0.1, 0.3)
        
        # Question length and complexity factors
        length_factor = min(len(question.split()) / 20, 0.1)
        
        confidence = base_confidence + frequency_boost + length_factor
        return min(confidence, 1.0)
    
    def _extract_topic(self, question: str) -> str:
        """
        Extract the main topic from a question
        """
        # Simple topic extraction - can be enhanced with NLP
        topics = self.nlp_analyzer.extract_key_topics(question)
        return topics[0] if topics else "General"
    
    def _assess_difficulty(self, question: str) -> str:
        """
        Assess the difficulty level of a question
        """
        easy_indicators = ['define', 'what is', 'list', 'name']
        medium_indicators = ['explain', 'describe', 'how']
        hard_indicators = ['analyze', 'evaluate', 'compare', 'synthesize']
        
        question_lower = question.lower()
        
        if any(indicator in question_lower for indicator in hard_indicators):
            return "Hard"
        elif any(indicator in question_lower for indicator in medium_indicators):
            return "Medium"
        elif any(indicator in question_lower for indicator in easy_indicators):
            return "Easy"
        else:
            return "Medium"
    
    def _organize_question_set_fixed(self, questions: List[Question]) -> QuestionSet:
        """
        Organize questions into fixed distribution:
        - Frequent: 6 questions (basic/definition type)
        - Moderate: 6 questions (standard difficulty)
        - Important: 6 questions (high weightage/complex)
        - Predicted: 4 questions (trending/application based)
        """
        # Sort questions by confidence and difficulty for better distribution
        questions.sort(key=lambda q: (q.confidence_score, self._get_difficulty_score(q.difficulty)), reverse=True)
        
        question_set = QuestionSet()
        
        # Separate questions by initial category preference
        frequent_candidates = [q for q in questions if self._is_frequent_type(q.text)]
        moderate_candidates = [q for q in questions if self._is_moderate_type(q.text)]
        important_candidates = [q for q in questions if self._is_important_type(q.text)]
        predicted_candidates = [q for q in questions if self._is_predicted_type(q.text)]
        
        # Fill remaining from general pool
        remaining_questions = [q for q in questions if q not in frequent_candidates + moderate_candidates + important_candidates + predicted_candidates]
        
        # Distribute questions with fixed counts
        question_set.frequent_questions = self._select_questions(frequent_candidates + remaining_questions, 6, QuestionCategory.FREQUENT)
        question_set.moderate_questions = self._select_questions(moderate_candidates + remaining_questions, 6, QuestionCategory.MODERATE)
        question_set.important_questions = self._select_questions(important_candidates + remaining_questions, 6, QuestionCategory.IMPORTANT)
        question_set.predicted_questions = self._select_questions(predicted_candidates + remaining_questions, 4, QuestionCategory.PREDICTED)
        
        return question_set
    
    def _select_questions(self, candidates: List[Question], count: int, category: QuestionCategory) -> List[Question]:
        """Select specified number of questions for a category"""
        selected = []
        used_texts = set()
        
        for question in candidates:
            if len(selected) >= count:
                break
            if question.text not in used_texts:
                question.category = category
                selected.append(question)
                used_texts.add(question.text)
        
        # If we don't have enough, create variations or use remaining
        while len(selected) < count and candidates:
            base_question = candidates[len(selected) % len(candidates)]
            if base_question.text not in used_texts:
                new_question = Question(
                    text=base_question.text,
                    category=category,
                    confidence_score=base_question.confidence_score,
                    topic=base_question.topic,
                    difficulty=base_question.difficulty,
                    source=base_question.source
                )
                selected.append(new_question)
                used_texts.add(base_question.text)
        
        return selected
    
    def _is_frequent_type(self, question: str) -> bool:
        """Check if question is frequent type (basic/definition)"""
        frequent_keywords = ['define', 'what is', 'meaning', 'introduction', 'basic', 'explain briefly']
        return any(keyword in question.lower() for keyword in frequent_keywords)
    
    def _is_moderate_type(self, question: str) -> bool:
        """Check if question is moderate type (standard)"""
        moderate_keywords = ['how', 'describe', 'explain', 'process', 'method', 'steps']
        return any(keyword in question.lower() for keyword in moderate_keywords)
    
    def _is_important_type(self, question: str) -> bool:
        """Check if question is important type (complex/high marks)"""
        important_keywords = ['analyze', 'compare', 'evaluate', 'discuss', 'critically', 'detail']
        return any(keyword in question.lower() for keyword in important_keywords)
    
    def _is_predicted_type(self, question: str) -> bool:
        """Check if question is predicted type (application/trending)"""
        predicted_keywords = ['application', 'future', 'trend', 'impact', 'recent', 'modern', 'current']
        return any(keyword in question.lower() for keyword in predicted_keywords)
    
    def _get_difficulty_score(self, difficulty: str) -> int:
        """Convert difficulty to numeric score"""
        difficulty_scores = {"Easy": 1, "Medium": 2, "Hard": 3}
        return difficulty_scores.get(difficulty, 2)
    
    def _estimate_marks(self, question: str) -> int:
        """Estimate marks for a question based on complexity"""
        question_lower = question.lower()
        
        # High marks indicators (10-15 marks)
        if any(keyword in question_lower for keyword in ['analyze', 'evaluate', 'compare and contrast', 'discuss in detail', 'critically examine']):
            return 15
        
        # Medium-high marks (5-10 marks)
        elif any(keyword in question_lower for keyword in ['explain', 'describe', 'discuss', 'compare', 'differentiate']):
            return 10
        
        # Medium marks (3-5 marks)
        elif any(keyword in question_lower for keyword in ['how', 'why', 'process', 'method', 'steps']):
            return 5
        
        # Low marks (1-2 marks)
        elif any(keyword in question_lower for keyword in ['define', 'what is', 'meaning', 'list', 'name']):
            return 2
        
        return 5  # Default medium marks