from fastapi import APIRouter, HTTPException
from models.schemas import ExplanationRequest, ExplanationResponse
import logging
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# OpenAI integration
OPENAI_AVAILABLE = False
try:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client = OpenAI(api_key=api_key)
        OPENAI_AVAILABLE = True
    else:
        client = None
        OPENAI_AVAILABLE = False
except ImportError:
    client = None
    OPENAI_AVAILABLE = False

@router.post("/generate", response_model=ExplanationResponse)
async def generate_explanation(request: ExplanationRequest):
    """
    Generate AI-powered explanations for questions
    """
    try:
        # Create context-aware prompt
        prompt = _create_explanation_prompt(request)
        
        # Call OpenAI API
        response = await _call_openai_api(prompt)
        
        # Parse response into structured format
        explanation_response = _parse_explanation_response(response, request.question)
        
        return explanation_response
        
    except Exception as e:
        logging.error(f"Error generating explanation: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate explanation")

@router.post("/short-notes")
async def generate_short_notes(request: ExplanationRequest):
    """
    Generate concise study notes for a topic
    """
    try:
        prompt = f"""
        Create concise study notes for the following {request.subject} question:
        
        Question: {request.question}
        
        Provide:
        1. Key concepts (3-5 bullet points)
        2. Important formulas or definitions
        3. Quick revision points
        4. Memory tricks or mnemonics if applicable
        
        Keep it brief and exam-focused.
        """
        
        response = await _call_openai_api(prompt)
        
        return {
            "question": request.question,
            "short_notes": response,
            "subject": request.subject
        }
        
    except Exception as e:
        logging.error(f"Error generating short notes: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate short notes")

@router.post("/exam-tips")
async def generate_exam_tips(request: ExplanationRequest):
    """
    Generate exam-specific tips for a question
    """
    try:
        prompt = f"""
        Provide exam-specific tips for this {request.subject} question:
        
        Question: {request.question}
        
        Include:
        1. How to approach this type of question in exams
        2. Common mistakes to avoid
        3. Time management tips
        4. Scoring strategies
        5. Related topics that might be asked
        
        Focus on practical exam advice.
        """
        
        response = await _call_openai_api(prompt)
        
        return {
            "question": request.question,
            "exam_tips": response,
            "subject": request.subject
        }
        
    except Exception as e:
        logging.error(f"Error generating exam tips: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate exam tips")

async def _call_openai_api(prompt: str) -> str:
    """
    Call OpenAI API with error handling
    """
    try:
        if not OPENAI_AVAILABLE or not client:
            return _generate_fallback_response(prompt)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert tutor helping students prepare for exams. Provide clear, detailed, and exam-focused explanations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return _generate_fallback_response(prompt)

def _create_explanation_prompt(request: ExplanationRequest) -> str:
    """
    Create a comprehensive prompt for detailed explanation generation with marks-based analysis
    """
    # Get marks weightage from question if available
    marks_weightage = getattr(request, 'marks_weightage', 5)
    
    prompt = f"""
    You are an expert {request.subject} tutor and examiner. Provide a comprehensive, exam-focused explanation for this question.
    
    Question: "{request.question}"
    Estimated Marks: {marks_weightage} marks
    
    Based on the {marks_weightage}-mark allocation, provide a detailed analysis:
    
    1. COMPREHENSIVE EXPLANATION ({marks_weightage} marks):
    - Provide thorough, step-by-step explanation appropriate for {marks_weightage} marks
    - Include underlying concepts, principles, and theoretical background
    - Show calculations, formulas, derivations, or processes with clear steps
    - Include relevant examples, case studies, or real-world applications
    - Use proper academic terminology and technical language
    - Cover ALL aspects needed to earn full {marks_weightage} marks
    
    2. INTERACTIVE VISUAL DIAGRAMS:
    Create proper visual diagrams using modern web technologies. Use these formats:
    
    DIAGRAM_START: [diagram_type] - [title]
    [diagram_configuration_in_json]
    DIAGRAM_END
    
    Diagram types to create:
    
    A) MERMAID DIAGRAMS (for flowcharts, sequences, etc.):
    DIAGRAM_START: mermaid - Process Flow
    {{
      "mermaid_code": "flowchart TD\\n    A[Start] --> B{{Decision}}\\n    B -->|Yes| C[Process]\\n    B -->|No| D[End]\\n    C --> D"
    }}
    DIAGRAM_END
    
    B) CHART DIAGRAMS (for data visualization):
    DIAGRAM_START: chart - Performance Analysis
    {{
      "chart_config": {{
        "type": "bar",
        "data": {{
          "labels": ["Category A", "Category B", "Category C"],
          "datasets": [{{
            "label": "Performance",
            "data": [65, 59, 80],
            "backgroundColor": ["#3b82f6", "#10b981", "#f59e0b"]
          }}]
        }},
        "options": {{
          "responsive": true,
          "plugins": {{
            "title": {{
              "display": true,
              "text": "Performance Analysis"
            }}
          }}
        }}
      }}
    }}
    DIAGRAM_END
    
    C) SVG DIAGRAMS (for custom shapes and structures):
    DIAGRAM_START: svg - System Architecture
    {{
      "svg_config": {{
        "width": 400,
        "height": 300,
        "elements": [
          {{"type": "rect", "x": 50, "y": 50, "width": 100, "height": 60, "fill": "#3b82f6", "rx": 5}},
          {{"type": "text", "x": 100, "y": 85, "text": "Component A", "fill": "white", "textAnchor": "middle"}},
          {{"type": "line", "x1": 150, "y1": 80, "x2": 200, "y2": 80, "stroke": "#6b7280", "strokeWidth": 2, "arrow": true}}
        ]
      }}
    }}
    DIAGRAM_END
    
    D) D3 DIAGRAMS (for complex hierarchies and networks):
    DIAGRAM_START: d3 - Concept Hierarchy
    {{
      "d3_config": {{
        "type": "tree",
        "width": 400,
        "height": 300,
        "data": {{
          "name": "Main Concept",
          "children": [
            {{"name": "Sub A", "children": [{{"name": "Detail 1"}}, {{"name": "Detail 2"}}]}},
            {{"name": "Sub B", "children": [{{"name": "Detail 3"}}]}}
          ]
        }}
      }}
    }}
    DIAGRAM_END
    
    Create 1-3 relevant diagrams for this {marks_weightage}-mark question. Choose the most appropriate diagram type based on the content.
    
    3. MARKS DISTRIBUTION BREAKDOWN:
    - Show exactly how {marks_weightage} marks are distributed across answer components
    - Introduction/Definition: {max(1, marks_weightage//5)} marks
    - Main Content/Explanation: {marks_weightage*3//4} marks  
    - Examples/Applications: {max(1, marks_weightage//4)} marks
    - Conclusion/Summary: {max(1, marks_weightage//5)} marks
    - Specify which specific points carry more weightage
    - Recommended word count: {marks_weightage * 40}-{marks_weightage * 60} words
    
    4. POINTWISE ANSWER STRUCTURE:
    - Provide exact format with clear headings and numbered points
    - Show main headings (I, II, III), sub-points (A, B, C), and details (1, 2, 3)
    - Include specific examples, formulas, or data for each point
    - Format for maximum examiner appeal and easy marking
    - Show how to use bullet points, tables, or lists effectively
    
    5. MEMORY TECHNIQUES & MNEMONICS:
    - Create specific mnemonics for key concepts and formulas
    - Provide acronyms for remembering sequences or processes
    - Suggest visual associations and memory palace techniques
    - Include rhymes, word associations, or story methods for complex terms
    - Quick revision tricks for last-minute preparation
    
    6. EXAM STRATEGY & SCORING TIPS:
    - Time allocation: {marks_weightage * 1.5}-{marks_weightage * 2} minutes recommended
    - Common examiner expectations for {marks_weightage}-mark questions
    - Typical mistakes that cost marks in this topic
    - Essential keywords and phrases examiners look for
    - How to impress examiners and potentially score bonus marks
    - Presentation tips (neat diagrams, clear handwriting, proper formatting)
    
    7. RELATED CONCEPTS & CROSS-CONNECTIONS:
    - Connect to other important topics in {request.subject}
    - Potential follow-up questions (both higher and lower marks)
    - Interdisciplinary connections with other subjects
    - Current trends, recent developments, or applications
    - How this topic fits into the broader curriculum
    
    Make this explanation extremely comprehensive, practical, and specifically tailored for scoring full {marks_weightage} marks in {request.subject} examinations. Focus on actionable advice that students can immediately apply.
    """
    
    return prompt

def _parse_explanation_response(response: str, question: str) -> ExplanationResponse:
    """
    Parse comprehensive OpenAI response into structured ExplanationResponse with diagrams
    """
    from models.schemas import DiagramElement
    
    # Extract diagrams first
    diagrams = []
    diagram_pattern = r'DIAGRAM_START:\s*(\w+)\s*-\s*(.+?)\n(.*?)\nDIAGRAM_END'
    import re
    import json
    
    diagram_matches = re.findall(diagram_pattern, response, re.DOTALL)
    for diagram_type, title, config_json in diagram_matches:
        try:
            # Parse the JSON configuration
            config = json.loads(config_json.strip())
            
            diagram = DiagramElement(
                title=title.strip(),
                description=f"Interactive visual representation for {title.strip()}",
                diagram_type=diagram_type.lower()
            )
            
            # Set the appropriate configuration based on diagram type
            if diagram_type.lower() == 'mermaid':
                diagram.mermaid_code = config.get('mermaid_code', '')
            elif diagram_type.lower() == 'chart':
                diagram.chart_config = config.get('chart_config', {})
            elif diagram_type.lower() == 'svg':
                diagram.svg_config = config.get('svg_config', {})
            elif diagram_type.lower() == 'd3':
                diagram.d3_config = config.get('d3_config', {})
            elif diagram_type.lower() == 'css':
                diagram.html_content = config.get('html_content', '')
            
            diagrams.append(diagram)
            
        except json.JSONDecodeError as e:
            # Fallback to simple diagram if JSON parsing fails
            logging.warning(f"Failed to parse diagram JSON: {e}")
            diagrams.append(DiagramElement(
                title=title.strip(),
                description=f"Visual representation for {title.strip()}",
                diagram_type="svg",
                svg_config={
                    "width": 400,
                    "height": 200,
                    "elements": [
                        {"type": "rect", "x": 50, "y": 50, "width": 300, "height": 100, "fill": "#3b82f6", "rx": 5},
                        {"type": "text", "x": 200, "y": 105, "text": title.strip(), "fill": "white", "textAnchor": "middle", "fontSize": 16}
                    ]
                }
            ))
    
    # Remove diagram sections from response for other parsing
    clean_response = re.sub(diagram_pattern, '', response, flags=re.DOTALL)
    
    # Enhanced parsing for the detailed response format
    sections = clean_response.split('\n\n')
    
    explanation = ""
    key_points = []
    exam_tips = []
    answer_structure = []
    marks_breakdown = {}
    time_allocation = ""
    
    current_section = "explanation"
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        # Identify section headers
        section_upper = section.upper()
        if any(header in section_upper for header in ["DETAILED EXPLANATION", "1. DETAILED", "COMPREHENSIVE EXPLANATION"]):
            current_section = "explanation"
            continue
        elif any(header in section_upper for header in ["MEMORY TECHNIQUES", "5. MEMORY", "KEY POINTS"]):
            current_section = "key_points"
            continue
        elif any(header in section_upper for header in ["EXAM STRATEGY", "6. EXAM", "EXAM TIPS"]):
            current_section = "exam_tips"
            continue
        elif any(header in section_upper for header in ["POINTWISE ANSWER", "4. POINTWISE", "ANSWER STRUCTURE"]):
            current_section = "answer_structure"
            continue
        elif any(header in section_upper for header in ["MARKS DISTRIBUTION", "3. MARKS", "MARKS BREAKDOWN"]):
            current_section = "marks_breakdown"
            # Extract marks information
            lines = section.split('\n')
            for line in lines:
                if 'marks' in line.lower() and ':' in line:
                    parts = line.split(':')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        try:
                            value = int(re.search(r'\d+', parts[1]).group())
                            marks_breakdown[key] = value
                        except:
                            pass
            continue
        elif "TIME ALLOCATION" in section_upper:
            time_allocation = section
            continue
        
        # Process content based on current section
        if current_section == "explanation":
            explanation += section + "\n\n"
        elif current_section == "key_points":
            # Extract bullet points and numbered items
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line[0:2].replace('.', '').isdigit()):
                    clean_line = line.lstrip('- •0123456789. ').strip()
                    if clean_line and len(clean_line) > 10:
                        key_points.append(clean_line)
        elif current_section == "exam_tips":
            # Extract bullet points and numbered items
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line[0:2].replace('.', '').isdigit()):
                    clean_line = line.lstrip('- •0123456789. ').strip()
                    if clean_line and len(clean_line) > 10:
                        exam_tips.append(clean_line)
        elif current_section == "answer_structure":
            # Extract answer structure points
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line[0:3].replace('.', '').replace(')', '').isalnum()):
                    clean_line = line.lstrip('- •0123456789.() ').strip()
                    if clean_line and len(clean_line) > 5:
                        answer_structure.append(clean_line)
    
    # Fallback if parsing fails
    if not explanation:
        explanation = clean_response
    if not key_points:
        key_points = [
            "Break down complex concepts into smaller parts",
            "Create visual representations or diagrams", 
            "Practice with similar questions regularly",
            "Connect new concepts to previously learned material",
            "Use active recall techniques for better retention"
        ]
    if not exam_tips:
        exam_tips = [
            "Read the question carefully and identify key requirements",
            "Plan your answer structure before writing",
            "Allocate time based on marks weightage", 
            "Use clear headings and bullet points",
            "Review your answer for completeness and accuracy"
        ]
    
    return ExplanationResponse(
        question=question,
        explanation=explanation.strip(),
        key_points=key_points[:8],  # Increased to 8 points
        exam_tips=exam_tips[:8],     # Increased to 8 tips
        diagrams=diagrams,
        marks_breakdown=marks_breakdown if marks_breakdown else None,
        time_allocation=time_allocation if time_allocation else None,
        answer_structure=answer_structure[:6] if answer_structure else []
    )

def _generate_sample_diagrams(question: str, subject: str) -> str:
    """
    Generate sample diagrams for common question types using modern diagram formats
    """
    question_lower = question.lower()
    
    # Sample diagrams based on question type
    if any(word in question_lower for word in ['process', 'steps', 'procedure', 'method']):
        return """
DIAGRAM_START: mermaid - Process Flow
{
  "mermaid_code": "flowchart TD\\n    A[Start Process] --> B{Decision Point}\\n    B -->|Yes| C[Execute Step 1]\\n    B -->|No| D[Alternative Path]\\n    C --> E[Execute Step 2]\\n    D --> E\\n    E --> F[Validation]\\n    F --> G[End Process]\\n    \\n    style A fill:#e1f5fe\\n    style G fill:#c8e6c9\\n    style B fill:#fff3e0"
}
DIAGRAM_END
"""
    
    elif any(word in question_lower for word in ['structure', 'organization', 'hierarchy']):
        return """
DIAGRAM_START: d3 - Organizational Structure
{
  "d3_config": {
    "type": "tree",
    "width": 500,
    "height": 400,
    "data": {
      "name": "Main Topic",
      "children": [
        {
          "name": "Category A",
          "children": [
            {"name": "Subtopic A1"},
            {"name": "Subtopic A2"}
          ]
        },
        {
          "name": "Category B", 
          "children": [
            {"name": "Subtopic B1"},
            {"name": "Subtopic B2"},
            {"name": "Subtopic B3"}
          ]
        },
        {
          "name": "Category C",
          "children": [
            {"name": "Subtopic C1"}
          ]
        }
      ]
    }
  }
}
DIAGRAM_END
"""
    
    elif any(word in question_lower for word in ['cycle', 'circular', 'loop']):
        return """
DIAGRAM_START: svg - Circular Process
{
  "svg_config": {
    "width": 400,
    "height": 400,
    "elements": [
      {"type": "circle", "cx": 200, "cy": 200, "r": 120, "fill": "none", "stroke": "#3b82f6", "strokeWidth": 3},
      {"type": "circle", "cx": 200, "cy": 80, "r": 30, "fill": "#3b82f6"},
      {"type": "text", "x": 200, "y": 85, "text": "Phase 1", "fill": "white", "textAnchor": "middle", "fontSize": 12},
      {"type": "circle", "cx": 320, "cy": 200, "r": 30, "fill": "#10b981"},
      {"type": "text", "x": 320, "y": 205, "text": "Phase 2", "fill": "white", "textAnchor": "middle", "fontSize": 12},
      {"type": "circle", "cx": 200, "cy": 320, "r": 30, "fill": "#f59e0b"},
      {"type": "text", "x": 200, "y": 325, "text": "Phase 3", "fill": "white", "textAnchor": "middle", "fontSize": 12},
      {"type": "circle", "cx": 80, "cy": 200, "r": 30, "fill": "#ef4444"},
      {"type": "text", "x": 80, "y": 205, "text": "Phase 4", "fill": "white", "textAnchor": "middle", "fontSize": 12},
      {"type": "path", "d": "M 220 100 Q 300 120 300 180", "fill": "none", "stroke": "#6b7280", "strokeWidth": 2},
      {"type": "path", "d": "M 300 220 Q 280 300 220 300", "fill": "none", "stroke": "#6b7280", "strokeWidth": 2},
      {"type": "path", "d": "M 180 300 Q 100 280 100 220", "fill": "none", "stroke": "#6b7280", "strokeWidth": 2},
      {"type": "path", "d": "M 100 180 Q 120 100 180 100", "fill": "none", "stroke": "#6b7280", "strokeWidth": 2}
    ]
  }
}
DIAGRAM_END
"""
    
    elif any(word in question_lower for word in ['compare', 'difference', 'vs', 'versus']):
        return """
DIAGRAM_START: chart - Comparison Analysis
{
  "chart_config": {
    "type": "bar",
    "data": {
      "labels": ["Feature 1", "Feature 2", "Feature 3", "Feature 4", "Feature 5"],
      "datasets": [
        {
          "label": "Option A",
          "data": [85, 70, 90, 65, 80],
          "backgroundColor": "#3b82f6",
          "borderColor": "#1e40af",
          "borderWidth": 1
        },
        {
          "label": "Option B", 
          "data": [75, 85, 70, 90, 75],
          "backgroundColor": "#10b981",
          "borderColor": "#059669",
          "borderWidth": 1
        }
      ]
    },
    "options": {
      "responsive": true,
      "plugins": {
        "title": {
          "display": true,
          "text": "Comparative Analysis"
        },
        "legend": {
          "position": "top"
        }
      },
      "scales": {
        "y": {
          "beginAtZero": true,
          "max": 100
        }
      }
    }
  }
}
DIAGRAM_END
"""
    
    else:
        # Generic concept map
        return """
DIAGRAM_START: mermaid - Concept Map
{
  "mermaid_code": "graph TD\\n    A[Main Concept] --> B[Sub-concept 1]\\n    A --> C[Sub-concept 2]\\n    A --> D[Sub-concept 3]\\n    B --> E[Detail 1A]\\n    B --> F[Detail 1B]\\n    C --> G[Detail 2A]\\n    C --> H[Detail 2B]\\n    D --> I[Detail 3A]\\n    D --> J[Detail 3B]\\n    \\n    style A fill:#e1f5fe,stroke:#01579b,stroke-width:3px\\n    style B fill:#f3e5f5,stroke:#4a148c\\n    style C fill:#e8f5e8,stroke:#1b5e20\\n    style D fill:#fff3e0,stroke:#e65100"
}
DIAGRAM_END
"""

def _generate_fallback_response(prompt: str) -> str:
    """
    Generate a fallback response when OpenAI API is not available
    """
    # Extract question and subject from prompt
    question_match = re.search(r'Question: "(.*?)"', prompt)
    subject_match = re.search(r'expert (.*?) tutor', prompt)
    
    question = question_match.group(1) if question_match else "sample question"
    subject = subject_match.group(1) if subject_match else "General"
    
    sample_diagrams = _generate_sample_diagrams(question, subject)
    
    return f"""
1. COMPREHENSIVE EXPLANATION:

This is a comprehensive explanation for the question: "{question}"

To provide a thorough understanding, let's break down this {subject} topic:

• The question asks about fundamental concepts that are essential for understanding
• Key principles involve systematic analysis and application of theoretical knowledge
• Practical examples help illustrate the concepts in real-world scenarios
• Step-by-step approach ensures complete coverage of all important aspects

{sample_diagrams}

2. MEMORY TECHNIQUES & KEY POINTS:

• Create visual associations with the main concepts
• Use acronyms to remember key sequences or processes
• Practice active recall by explaining concepts in your own words
• Connect new information to previously learned material
• Review regularly using spaced repetition techniques

3. EXAM STRATEGY & SCORING TIPS:

• Read the question carefully and identify all parts
• Plan your answer structure before writing
• Use clear headings and bullet points for organization
• Include relevant examples and applications
• Allocate time based on marks weightage
• Review your answer for completeness and accuracy

Note: For AI-powered explanations, please set up your OpenAI API key in the .env file.
"""