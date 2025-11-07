from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum
import uuid

class QuestionCategory(str, Enum):
    FREQUENT = "frequent"
    MODERATE = "moderate"
    IMPORTANT = "important"
    PREDICTED = "predicted"

class SubjectRequest(BaseModel):
    subject_name: str = Field(..., min_length=1, max_length=100)
    user_id: Optional[str] = None

class UploadedDocument(BaseModel):
    filename: str
    content: str
    document_type: str  # "pyq", "notes", "syllabus"

class Question(BaseModel):
    id: Optional[str] = None
    text: str
    category: QuestionCategory
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    source: Optional[str] = None
    marks_weightage: Optional[int] = 5  # Estimated marks for the question

class QuestionSet(BaseModel):
    frequent_questions: List[Question] = []
    moderate_questions: List[Question] = []
    important_questions: List[Question] = []
    predicted_questions: List[Question] = []

class ExplanationRequest(BaseModel):
    question: str
    subject: str
    explanation_type: str = "detailed"  # "detailed" or "short"
    marks_weightage: Optional[int] = 5  # Default 5 marks

class DiagramElement(BaseModel):
    title: str
    description: str
    diagram_type: str  # "mermaid", "chart", "svg", "d3", "css"
    mermaid_code: Optional[str] = None  # For Mermaid.js diagrams
    chart_config: Optional[Dict] = None  # For Chart.js configurations
    svg_config: Optional[Dict] = None   # For SVG elements
    d3_config: Optional[Dict] = None    # For D3.js configurations
    html_content: Optional[str] = None  # For CSS-based diagrams

class ExplanationResponse(BaseModel):
    question: str
    explanation: str
    key_points: List[str]
    exam_tips: List[str]
    diagrams: List[DiagramElement] = []
    marks_breakdown: Optional[Dict[str, int]] = None
    time_allocation: Optional[str] = None
    answer_structure: Optional[List[str]] = []

class StudySession(BaseModel):
    id: Optional[str] = None
    display_name: Optional[str] = None  # Human-readable session name
    user_id: Optional[str] = None
    subject: str
    documents: List[UploadedDocument] = []
    question_set: Optional[QuestionSet] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)