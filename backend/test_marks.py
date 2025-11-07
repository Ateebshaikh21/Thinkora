from ai_engine.nlp_analysis import NLPAnalyzer

sample_text = '''
1. Define machine learning and explain its types. [8 marks]
2. What is supervised learning? [5 marks]  
Q3. Compare supervised vs unsupervised learning. [15 marks]
4. List the steps in data preprocessing. (3 marks)
'''

analyzer = NLPAnalyzer()
questions = analyzer.extract_questions_from_text(sample_text)

print('🧪 Testing Marks Extraction:')
print('=' * 40)
for i, q in enumerate(questions, 1):
    print(f'{i}. Text: {q["text"][:60]}...')
    print(f'   Marks: {q["marks"]}')
    print(f'   Source: {q["source_line"][:50]}...')
    print()

print(f'✅ Total questions extracted: {len(questions)}')