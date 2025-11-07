import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Tuple
import logging

class NLPAnalyzer:
    def __init__(self):
        # Use basic text processing for now
        self.nlp = None
        self.sentence_model = None
            
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )

    def extract_questions_from_text(self, text: str) -> List[Dict[str, any]]:
        """
        Extract questions with their marks from uploaded documents
        """
        # Enhanced question patterns that capture marks
        question_patterns = [
            # Pattern: "1. Question text [8 marks]" or "1. Question text (8 marks)"
            r'(\d+)\.\s*(.+?)[\[\(](\d+)\s*marks?[\]\)]',
            # Pattern: "Q1. Question text - 8 marks"
            r'Q(\d+)\.?\s*(.+?)\s*[-–]\s*(\d+)\s*marks?',
            # Pattern: "Question text [8]" or "Question text (8)"
            r'(.+?)[\[\(](\d+)[\]\)](?:\s*marks?)?',
            # Pattern: "8 marks: Question text"
            r'(\d+)\s*marks?[:\-]\s*(.+)',
            # Pattern: Standard numbered questions
            r'(\d+)\.\s*(.+?)(?=\d+\.|$)',
            # Pattern: Q format
            r'Q(\d+)[:\.]?\s*(.+?)(?=Q\d+|$)',
        ]
        
        questions = []
        lines = text.split('\n')
        
        # First pass: Look for questions with explicit marks
        for line in lines:
            line = line.strip()
            if not line or len(line) < 10:
                continue
            
            # Try patterns with marks first
            for i, pattern in enumerate(question_patterns[:4]):
                matches = re.findall(pattern, line, re.IGNORECASE)
                for match in matches:
                    if i == 0:  # Pattern: "1. Question text [8 marks]"
                        q_num, question_text, marks = match
                        marks = int(marks)
                    elif i == 1:  # Pattern: "Q1. Question text - 8 marks"
                        q_num, question_text, marks = match
                        marks = int(marks)
                    elif i == 2:  # Pattern: "Question text [8]"
                        question_text, marks = match
                        marks = int(marks)
                        q_num = len(questions) + 1
                    elif i == 3:  # Pattern: "8 marks: Question text"
                        marks, question_text = match
                        marks = int(marks)
                        q_num = len(questions) + 1
                    
                    question_text = question_text.strip()
                    if len(question_text) > 10:
                        questions.append({
                            'text': question_text,
                            'marks': marks,
                            'question_number': q_num,
                            'source_line': line
                        })
                        break
        
        # Second pass: Look for questions without explicit marks
        if len(questions) < 5:  # If we didn't find enough questions with marks
            for line in lines:
                line = line.strip()
                if not line or len(line) < 10:
                    continue
                
                # Check if this line already processed
                already_processed = any(q['source_line'] == line for q in questions)
                if already_processed:
                    continue
                
                # Try patterns without explicit marks
                for i, pattern in enumerate(question_patterns[4:], 4):
                    matches = re.findall(pattern, line, re.IGNORECASE)
                    for match in matches:
                        if i == 4:  # Standard numbered questions
                            q_num, question_text = match
                        elif i == 5:  # Q format
                            q_num, question_text = match
                        
                        question_text = question_text.strip()
                        if len(question_text) > 10:
                            # Try to infer marks from question complexity
                            inferred_marks = self._infer_marks_from_question(question_text)
                            questions.append({
                                'text': question_text,
                                'marks': inferred_marks,
                                'question_number': q_num,
                                'source_line': line,
                                'marks_inferred': True
                            })
                            break
        
        # Remove duplicates based on question text similarity
        unique_questions = []
        for q in questions:
            is_duplicate = False
            for existing in unique_questions:
                if self._are_questions_similar(q['text'], existing['text']):
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_questions.append(q)
        
        return unique_questions
    
    def _infer_marks_from_question(self, question_text: str) -> int:
        """
        Infer marks based on question complexity and keywords
        """
        question_lower = question_text.lower()
        
        # High marks indicators (10-15 marks)
        if any(keyword in question_lower for keyword in [
            'analyze', 'evaluate', 'compare and contrast', 'discuss in detail', 
            'critically examine', 'justify', 'assess', 'elaborate'
        ]):
            return 15
        
        # Medium-high marks (8-10 marks)
        elif any(keyword in question_lower for keyword in [
            'explain', 'describe', 'discuss', 'compare', 'differentiate',
            'illustrate', 'demonstrate', 'outline'
        ]):
            return 8
        
        # Medium marks (5-6 marks)
        elif any(keyword in question_lower for keyword in [
            'how', 'why', 'process', 'method', 'steps', 'procedure'
        ]):
            return 5
        
        # Low marks (2-3 marks)
        elif any(keyword in question_lower for keyword in [
            'define', 'what is', 'meaning', 'list', 'name', 'identify'
        ]):
            return 2
        
        # Default based on length
        if len(question_text) > 100:
            return 8
        elif len(question_text) > 50:
            return 5
        else:
            return 2
    
    def _are_questions_similar(self, q1: str, q2: str, threshold: float = 0.8) -> bool:
        """
        Check if two questions are similar to avoid duplicates
        """
        # Simple similarity check based on common words
        words1 = set(q1.lower().split())
        words2 = set(q2.lower().split())
        
        if not words1 or not words2:
            return False
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        similarity = intersection / union if union > 0 else 0
        return similarity > threshold

    def preprocess_text(self, text: str) -> str:
        """
        Clean and preprocess text for analysis
        """
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Remove special characters but keep question marks
        text = re.sub(r'[^\w\s\?]', ' ', text)
        
        return text

    def calculate_similarity_matrix(self, questions: List[str]) -> np.ndarray:
        """
        Calculate similarity matrix between questions using TF-IDF and cosine similarity
        """
        if len(questions) < 2:
            return np.array([[1.0]])
            
        # Preprocess questions
        processed_questions = [self.preprocess_text(q) for q in questions]
        
        try:
            # Use TF-IDF for similarity calculation
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(processed_questions)
            similarity_matrix = cosine_similarity(tfidf_matrix)
            return similarity_matrix
            
        except Exception as e:
            logging.error(f"Error calculating similarity: {e}")
            # Return identity matrix as fallback
            return np.eye(len(questions))

    def cluster_similar_questions(self, questions: List[str], similarity_threshold: float = 0.7) -> Dict[str, List[str]]:
        """
        Group similar questions together
        """
        if not questions:
            return {}
            
        similarity_matrix = self.calculate_similarity_matrix(questions)
        clusters = {}
        processed = set()
        
        for i, question in enumerate(questions):
            if i in processed:
                continue
                
            # Find similar questions
            similar_indices = np.where(similarity_matrix[i] > similarity_threshold)[0]
            cluster_questions = [questions[j] for j in similar_indices if j not in processed]
            
            if cluster_questions:
                # Use the first question as cluster key
                clusters[question] = cluster_questions
                processed.update(similar_indices)
        
        return clusters

    def extract_key_topics(self, text: str) -> List[str]:
        """
        Extract key topics and concepts from text
        """
        if not self.nlp:
            # Basic keyword extraction without spaCy
            words = text.lower().split()
            # Filter common words and return unique terms
            stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
            keywords = [word for word in words if len(word) > 3 and word not in stopwords]
            return list(set(keywords))[:10]  # Return top 10 unique keywords
        
        doc = self.nlp(text)
        
        # Extract named entities and noun phrases
        topics = []
        
        # Named entities
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE', 'EVENT', 'WORK_OF_ART']:
                topics.append(ent.text)
        
        # Noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text) > 3:
                topics.append(chunk.text)
        
        # Remove duplicates and return top topics
        return list(set(topics))[:15]

    def analyze_question_frequency(self, question_clusters: Dict[str, List[str]]) -> Dict[str, int]:
        """
        Analyze how frequently similar questions appear
        """
        frequency_map = {}
        
        for main_question, similar_questions in question_clusters.items():
            frequency_map[main_question] = len(similar_questions)
        
        return frequency_map