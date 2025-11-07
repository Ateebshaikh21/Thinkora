import re
import random
from typing import List, Dict, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class QuestionGenerator:
    """
    AI-powered question generator that creates meaningful quiz questions
    with realistic multiple choice options from document content
    """
    
    def __init__(self):
        self.question_templates = {
            'definition': [
                "What is {term}?",
                "Define {term}.",
                "Which of the following best describes {term}?",
                "{term} refers to:",
                "The term {term} means:"
            ],
            'function': [
                "What is the primary function of {term}?",
                "What does {term} do?",
                "The main purpose of {term} is to:",
                "{term} is used for:",
                "Which of the following is the main function of {term}?"
            ],
            'comparison': [
                "What is the difference between {term1} and {term2}?",
                "How does {term1} differ from {term2}?",
                "Which statement correctly compares {term1} and {term2}?",
                "The main difference between {term1} and {term2} is:",
                "{term1} and {term2} differ in that:"
            ],
            'process': [
                "What are the steps involved in {process}?",
                "How does {process} work?",
                "The process of {process} involves:",
                "Which of the following describes the {process} process?",
                "The correct sequence for {process} is:"
            ],
            'application': [
                "When would you use {term}?",
                "In which scenario is {term} most appropriate?",
                "{term} is best applied when:",
                "A practical application of {term} is:",
                "You would use {term} in which situation?"
            ]
        }
        
        # Common technical terms and concepts
        self.technical_terms = {
            'machine learning': ['algorithm', 'model', 'training', 'data', 'prediction', 'classification', 'regression'],
            'programming': ['function', 'variable', 'loop', 'condition', 'array', 'object', 'class'],
            'database': ['table', 'query', 'index', 'relationship', 'primary key', 'foreign key', 'normalization'],
            'networking': ['protocol', 'packet', 'router', 'switch', 'IP address', 'DNS', 'firewall'],
            'web development': ['HTML', 'CSS', 'JavaScript', 'framework', 'API', 'database', 'server']
        }
    
    def generate_quiz_questions(self, content: str, existing_questions: List[Dict], count: int = 20) -> List[Dict]:
        """
        Generate quiz questions with realistic multiple choice answers
        """
        # Extract key concepts and facts from content
        concepts = self._extract_key_concepts(content)
        facts = self._extract_factual_statements(content)
        processes = self._extract_processes(content)
        
        generated_questions = []
        
        # Generate different types of questions
        for i in range(count):
            if i < len(existing_questions):
                # Use existing question as base and generate proper options
                base_question = existing_questions[i]
                quiz_question = self._create_quiz_from_existing(base_question, content, concepts)
            else:
                # Generate completely new question
                quiz_question = self._generate_new_question(content, concepts, facts, processes)
            
            if quiz_question:
                generated_questions.append(quiz_question)
        
        return generated_questions[:count]
    
    def _extract_key_concepts(self, content: str) -> List[str]:
        """Extract key technical terms and concepts from content"""
        concepts = []
        
        # Look for capitalized terms (likely to be important concepts)
        capitalized_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
        concepts.extend(capitalized_terms[:10])
        
        # Look for terms in parentheses (often definitions)
        parenthetical = re.findall(r'\(([^)]+)\)', content)
        concepts.extend([p.strip() for p in parenthetical if len(p.strip()) < 50])
        
        # Look for quoted terms
        quoted_terms = re.findall(r'"([^"]+)"', content)
        concepts.extend([q.strip() for q in quoted_terms if len(q.strip()) < 30])
        
        # Remove duplicates and filter
        unique_concepts = []
        for concept in concepts:
            if concept not in unique_concepts and len(concept) > 2 and len(concept) < 50:
                unique_concepts.append(concept)
        
        return unique_concepts[:20]
    
    def _extract_factual_statements(self, content: str) -> List[str]:
        """Extract factual statements that can be turned into questions"""
        sentences = re.split(r'[.!?]+', content)
        facts = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 200:
                # Look for sentences with "is", "are", "can", "will", etc.
                if any(word in sentence.lower() for word in ['is', 'are', 'can', 'will', 'does', 'has', 'have']):
                    facts.append(sentence)
        
        return facts[:15]
    
    def _extract_processes(self, content: str) -> List[str]:
        """Extract process descriptions"""
        processes = []
        
        # Look for numbered steps
        numbered_steps = re.findall(r'\d+\.\s*([^.]+)', content)
        if len(numbered_steps) > 2:
            processes.append("the process described in steps")
        
        # Look for process keywords
        process_keywords = ['algorithm', 'method', 'procedure', 'process', 'workflow', 'steps']
        for keyword in process_keywords:
            if keyword in content.lower():
                processes.append(keyword)
        
        return processes[:5]
    
    def _create_quiz_from_existing(self, base_question: Dict, content: str, concepts: List[str]) -> Dict:
        """Create a quiz question from an existing question with proper options"""
        question_text = base_question.get('text', '')
        
        # Determine question type
        question_type = self._determine_question_type(question_text)
        
        # Generate realistic options based on the question
        options, correct_index = self._generate_realistic_options(question_text, content, concepts)
        
        return {
            'id': base_question.get('id', random.randint(1000, 9999)),
            'text': question_text,
            'type': 'multiple_choice',
            'options': options,
            'correct_answer': correct_index,
            'explanation': self._generate_explanation(question_text, options[correct_index]),
            'marks': base_question.get('marks_weightage', 1),
            'topic': base_question.get('topic', 'General'),
            'difficulty': base_question.get('difficulty', 'medium')
        }
    
    def _generate_new_question(self, content: str, concepts: List[str], facts: List[str], processes: List[str]) -> Dict:
        """Generate a completely new question"""
        if not concepts:
            return None
        
        # Choose a concept to ask about
        concept = random.choice(concepts)
        
        # Choose question type
        question_types = ['definition', 'function', 'application']
        question_type = random.choice(question_types)
        
        # Generate question text
        template = random.choice(self.question_templates[question_type])
        question_text = template.format(term=concept)
        
        # Generate options
        options, correct_index = self._generate_realistic_options(question_text, content, concepts, concept)
        
        return {
            'id': random.randint(1000, 9999),
            'text': question_text,
            'type': 'multiple_choice',
            'options': options,
            'correct_answer': correct_index,
            'explanation': f"The correct answer relates to {concept} as described in the content.",
            'marks': 1,
            'topic': concept,
            'difficulty': 'medium'
        }
    
    def _determine_question_type(self, question_text: str) -> str:
        """Determine the type of question based on its text"""
        question_lower = question_text.lower()
        
        if any(word in question_lower for word in ['what is', 'define', 'definition']):
            return 'definition'
        elif any(word in question_lower for word in ['how', 'process', 'steps']):
            return 'process'
        elif any(word in question_lower for word in ['difference', 'compare', 'contrast']):
            return 'comparison'
        elif any(word in question_lower for word in ['when', 'where', 'application']):
            return 'application'
        else:
            return 'general'
    
    def _generate_realistic_options(self, question_text: str, content: str, concepts: List[str], main_concept: str = None) -> Tuple[List[str], int]:
        """Generate realistic multiple choice options"""
        options = []
        
        # Try to extract the correct answer from content
        correct_answer = self._extract_answer_from_content(question_text, content, main_concept)
        
        if not correct_answer:
            correct_answer = "The correct answer based on the provided content"
        
        options.append(correct_answer)
        
        # Generate plausible distractors
        distractors = self._generate_distractors(question_text, content, concepts, correct_answer)
        options.extend(distractors[:3])
        
        # Shuffle options and find correct index
        correct_index = 0
        shuffled_options = options.copy()
        random.shuffle(shuffled_options)
        correct_index = shuffled_options.index(correct_answer)
        
        return shuffled_options, correct_index
    
    def _extract_answer_from_content(self, question_text: str, content: str, concept: str = None) -> str:
        """Try to extract the actual answer from the content"""
        question_lower = question_text.lower()
        
        # First, try to find the exact question and its answer in the content
        question_clean = question_text.strip().rstrip('?').rstrip('.')
        
        # Look for the question followed by an answer
        question_patterns = [
            rf'{re.escape(question_clean)}\s*\??\s*\n([^?]+?)(?=\n\d+\.|\n[A-Z]|\Z)',
            rf'{re.escape(question_clean)}\s*\??\s*([^?]+?)(?=\n\d+\.|\n[A-Z]|\Z)',
            rf'{re.escape(question_clean)}\s*\??\s*\n?([^?]+?)(?=\n|\Z)'
        ]
        
        for pattern in question_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            if matches:
                answer = matches[0].strip()
                # Clean up the answer
                answer = re.sub(r'\n+', ' ', answer)  # Replace newlines with spaces
                answer = re.sub(r'\s+', ' ', answer)  # Replace multiple spaces with single space
                if len(answer) > 10 and len(answer) < 200:
                    return answer.strip()
        
        # Extract term from question for targeted search
        term = None
        if 'what is' in question_lower:
            term_match = re.search(r'what is\s+([^?]+)', question_lower)
            if term_match:
                term = term_match.group(1).strip()
        elif 'define' in question_lower:
            term_match = re.search(r'define\s+([^?.]+)', question_lower)
            if term_match:
                term = term_match.group(1).strip()
        
        # If we have a term, look for its definition
        if term:
            # Look for definition patterns with the term
            definition_patterns = [
                rf'{re.escape(term)}\s+is\s+([^.!?]+(?:\.[^.!?]*)*)',
                rf'{re.escape(term)}\s+are\s+([^.!?]+(?:\.[^.!?]*)*)',
                rf'{re.escape(term)}\s*:\s*([^.!?]+(?:\.[^.!?]*)*)',
                rf'{re.escape(term)}\s+refers?\s+to\s+([^.!?]+(?:\.[^.!?]*)*)',
                rf'{re.escape(term)}\s+means?\s+([^.!?]+(?:\.[^.!?]*)*)'
            ]
            
            for pattern in definition_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    definition = matches[0].strip()
                    # Clean up the definition
                    definition = re.sub(r'\s+', ' ', definition)
                    if len(definition) > 10 and len(definition) < 200:
                        return definition.capitalize()
        
        # Look for concept-based definitions if concept is provided
        if concept:
            concept_lower = concept.lower()
            
            # Look for definition patterns with the concept
            definition_patterns = [
                rf'{re.escape(concept_lower)}\s+is\s+([^.!?]+(?:\.[^.!?]*)*)',
                rf'{re.escape(concept_lower)}\s+are\s+([^.!?]+(?:\.[^.!?]*)*)',
                rf'{re.escape(concept_lower)}\s*:\s*([^.!?]+(?:\.[^.!?]*)*)'
            ]
            
            for pattern in definition_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    definition = matches[0].strip()
                    definition = re.sub(r'\s+', ' ', definition)
                    if len(definition) > 10 and len(definition) < 200:
                        return definition.capitalize()
        
        # Fallback: look for any definition-like sentences
        sentences = re.split(r'[.!?]+', content)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 200:
                # Check if it's a definition sentence
                if any(pattern in sentence.lower() for pattern in [' is ', ' are ', ' means ', ' refers to ']):
                    if term and term.lower() in sentence.lower():
                        return sentence.capitalize()
                    elif concept and concept.lower() in sentence.lower():
                        return sentence.capitalize()
        
        # Final fallback
        if term:
            return f"The definition of {term} as described in the material"
        elif concept:
            return f"A key concept related to {concept} in the subject matter"
        else:
            return "The answer based on the provided content"
    
    def _generate_distractors(self, question_text: str, content: str, concepts: List[str], correct_answer: str) -> List[str]:
        """Generate plausible but incorrect answer options"""
        distractors = []
        question_lower = question_text.lower()
        
        # Use other concepts as distractors
        other_concepts = [c for c in concepts if c.lower() not in correct_answer.lower()]
        
        # Extract domain-specific terms from content
        domain_terms = self._extract_domain_terms(content)
        
        # Generate contextually relevant but incorrect options
        if 'what is' in question_lower or 'define' in question_lower:
            # Create definition-style distractors
            if other_concepts:
                distractors.extend([
                    f"A process that involves {random.choice(other_concepts).lower()} and data analysis",
                    f"A technique used for {random.choice(other_concepts).lower()} optimization",
                    f"A method that combines {random.choice(other_concepts).lower()} with statistical analysis"
                ])
            else:
                distractors.extend([
                    "A process that involves data transformation and analysis",
                    "A technique used for system optimization and performance",
                    "A method that combines statistical analysis with computational algorithms"
                ])
                
        elif 'how' in question_lower or 'process' in question_lower:
            distractors.extend([
                "By implementing recursive algorithms with dynamic programming",
                "Through iterative refinement using gradient descent methods",
                "Via ensemble methods combining multiple prediction models"
            ])
            
        elif 'when' in question_lower or 'where' in question_lower:
            distractors.extend([
                "When working with high-dimensional feature spaces",
                "In scenarios involving real-time data streaming",
                "During cross-validation and model selection phases"
            ])
            
        elif 'why' in question_lower:
            distractors.extend([
                "To reduce computational complexity and improve efficiency",
                "To handle overfitting and improve model generalization",
                "To optimize memory usage and processing speed"
            ])
            
        else:
            # Create generic but domain-relevant distractors
            if domain_terms:
                distractors.extend([
                    f"An approach that utilizes {random.choice(domain_terms)} for enhanced performance",
                    f"A framework designed for {random.choice(domain_terms)} applications",
                    f"A methodology that incorporates {random.choice(domain_terms)} principles"
                ])
            else:
                distractors.extend([
                    "An approach that utilizes advanced algorithms for enhanced performance",
                    "A framework designed for large-scale data processing applications",
                    "A methodology that incorporates machine learning principles"
                ])
        
        # Add some variation by modifying existing distractors
        enhanced_distractors = []
        for distractor in distractors[:3]:
            # Sometimes add qualifiers to make them more plausible
            if random.random() < 0.3:
                qualifiers = ["primarily", "mainly", "specifically", "generally", "typically"]
                distractor = f"{random.choice(qualifiers).capitalize()} {distractor.lower()}"
            enhanced_distractors.append(distractor)
        
        return enhanced_distractors[:3]
    
    def _extract_domain_terms(self, content: str) -> List[str]:
        """Extract domain-specific technical terms from content"""
        # Common technical terms by domain
        technical_patterns = [
            r'\b(?:algorithm|model|training|prediction|classification|regression)\b',
            r'\b(?:neural|network|deep|learning|machine|artificial)\b',
            r'\b(?:data|dataset|feature|parameter|optimization|gradient)\b',
            r'\b(?:clustering|supervised|unsupervised|reinforcement)\b',
            r'\b(?:accuracy|precision|recall|validation|testing)\b'
        ]
        
        domain_terms = []
        for pattern in technical_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            domain_terms.extend([match.lower() for match in matches])
        
        # Remove duplicates and return most common terms
        unique_terms = list(set(domain_terms))
        return unique_terms[:10]
    
    def _generate_explanation(self, question_text: str, correct_answer: str) -> str:
        """Generate an explanation for why the answer is correct"""
        return f"This is the correct answer because it accurately describes the concept as presented in the source material. {correct_answer}"
    
    def create_true_false_question(self, statement: str) -> Dict:
        """Create a true/false question from a statement"""
        # Randomly make it true or false
        is_true = random.choice([True, False])
        
        if not is_true:
            # Modify the statement to make it false
            statement = self._make_statement_false(statement)
        
        return {
            'id': random.randint(1000, 9999),
            'text': f"True or False: {statement}",
            'type': 'true_false',
            'options': ['True', 'False'],
            'correct_answer': 0 if is_true else 1,
            'explanation': f"This statement is {'true' if is_true else 'false'} based on the content.",
            'marks': 1,
            'difficulty': 'easy'
        }
    
    def _make_statement_false(self, statement: str) -> str:
        """Modify a statement to make it false"""
        # Simple modifications to make statements false
        modifications = [
            ('is', 'is not'),
            ('can', 'cannot'),
            ('will', 'will not'),
            ('always', 'never'),
            ('all', 'no'),
            ('increase', 'decrease'),
            ('improve', 'worsen')
        ]
        
        for original, replacement in modifications:
            if original in statement.lower():
                return statement.lower().replace(original, replacement)
        
        # If no modifications possible, add "not"
        return statement.replace(' is ', ' is not ')