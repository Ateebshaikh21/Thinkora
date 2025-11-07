#!/usr/bin/env python3

# Test script to verify marks extraction from PDF content

import sys
import os
sys.path.append('backend')

from backend.ai_engine.nlp_analysis import NLPAnalyzer

def test_marks_extraction():
    """Test the marks extraction functionality"""
    
    # Sample PDF content with marks
    sample_pdf_content = """
    COMPUTER SCIENCE EXAMINATION
    
    1. Define machine learning and explain its types. [8 marks]
    
    2. What is supervised learning? Give examples. [5 marks]
    
    Q3. Compare and contrast supervised vs unsupervised learning algorithms. Discuss their applications in real-world scenarios. [15 marks]
    
    4. List the steps involved in data preprocessing. (3 marks)
    
    5 marks: Explain the concept of overfitting and how to prevent it.
    
    6. Describe the working of neural networks in detail. [12 marks]
    
    Q7. What are the different types of machine learning algorithms? [6 marks]
    """
    
    print("🧪 Testing Marks Extraction from PDF Content")
    print("=" * 50)
    
    analyzer = NLPAnalyzer()
    questions = analyzer.extract_questions_from_text(sample_pdf_content)
    
    print(f"📊 Extracted {len(questions)} questions with marks:")
    print()
    
    for i, q in enumerate(questions, 1):
        print(f"{i}. Question: {q['text'][:80]}...")
        print(f"   Marks: {q['marks']} {'(inferred)' if q.get('marks_inferred') else '(from PDF)'}")
        print(f"   Source: {q['source_line'][:60]}...")
        print()
    
    # Verify marks are correctly extracted
    expected_marks = [8, 5, 15, 3, 5, 12, 6]
    actual_marks = [q['marks'] for q in questions]
    
    print("✅ Verification:")
    print(f"Expected marks: {expected_marks}")
    print(f"Actual marks:   {actual_marks}")
    
    if actual_marks == expected_marks:
        print("🎉 SUCCESS: All marks extracted correctly!")
    else:
        print("❌ FAILURE: Marks extraction needs improvement")
        
        # Show differences
        for i, (expected, actual) in enumerate(zip(expected_marks, actual_marks)):
            if expected != actual:
                print(f"   Question {i+1}: Expected {expected}, Got {actual}")

if __name__ == "__main__":
    test_marks_extraction()