import React, { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import axios from "axios";
import SimpleDiagramRenderer from "../components/SimpleDiagramRenderer";

const QuestionAnalysis = ({ session }) => {
  const [questionSet, setQuestionSet] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [activeTab, setActiveTab] = useState("frequent");
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [sessionData, setSessionData] = useState(session);
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    // Check for session ID in URL parameters (from history)
    const sessionIdFromUrl = searchParams.get("session");

    if (sessionIdFromUrl) {
      setSessionId(sessionIdFromUrl);
      fetchSessionData(sessionIdFromUrl);
      generateQuestions(sessionIdFromUrl);
    } else if (session && session.session_id) {
      setSessionId(session.session_id);
      setSessionData(session);
      generateQuestions(session.session_id);
    }
  }, [session, searchParams]);

  const fetchSessionData = async (sessionId) => {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/analysis/session/${sessionId}`
      );
      setSessionData(response.data);
    } catch (err) {
      console.error("Failed to fetch session data:", err);
    }
  };

  const generateQuestions = async (sessionId) => {
    if (!sessionId) return;

    setLoading(true);
    setError("");

    try {
      const response = await axios.post(
        `http://localhost:8000/api/analysis/generate-questions/${sessionId}`
      );
      setQuestionSet(response.data.question_set);
    } catch (err) {
      setError("Failed to generate questions. Please try again.");
      console.error("Question generation error:", err);
    } finally {
      setLoading(false);
    }
  };

  const getExplanation = async (question) => {
    try {
      const response = await axios.post(
        "http://localhost:8000/api/explanations/generate",
        {
          question: question.text,
          subject: sessionData?.subject || session?.subject || "General",
          explanation_type: "detailed",
          marks_weightage: question.marks_weightage || 5,
        }
      );
      setExplanation(response.data);
      setSelectedQuestion(question);
    } catch (err) {
      console.error("Explanation error:", err);
      setExplanation({
        question: question.text,
        explanation: "Unable to generate explanation at this time.",
        key_points: ["Please try again later"],
        exam_tips: ["Review your study materials"],
      });
      setSelectedQuestion(question);
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      frequent: "green",
      moderate: "yellow",
      important: "orange",
      predicted: "red",
    };
    return colors[category] || "gray";
  };

  const getCategoryQuestions = (category) => {
    if (!questionSet) return [];
    return questionSet[`${category}_questions`] || [];
  };

  if (!sessionData && !sessionId && !loading) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="card text-center">
          <h2 className="text-2xl font-bold mb-4">No Session Found</h2>
          <p className="text-gray-600 mb-6">
            Please upload documents first to analyze questions.
          </p>
          <button onClick={() => navigate("/upload")} className="btn-primary">
            Upload Documents
          </button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card text-center">
          <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold mb-2">
            Analyzing Your Documents
          </h2>
          <p className="text-gray-600">
            Our AI is processing your materials and generating smart
            questions...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold gradient-text mb-4">
          Question Analysis
        </h1>
        <p className="text-gray-600">
          AI-generated questions categorized by importance and frequency
          patterns.
        </p>
      </div>

      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Questions Panel */}
        <div className="lg:col-span-2">
          <div className="card">
            {/* Category Tabs */}
            <div className="flex space-x-1 mb-6 bg-gray-100 p-1 rounded-lg">
              {["frequent", "moderate", "important", "predicted"].map(
                (category) => (
                  <button
                    key={category}
                    onClick={() => setActiveTab(category)}
                    className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                      activeTab === category
                        ? "bg-white shadow-sm text-gray-900"
                        : "text-gray-600 hover:text-gray-900"
                    }`}
                  >
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                    <span className="ml-2 text-xs bg-gray-200 px-2 py-1 rounded-full">
                      {category === "predicted" ? "4" : "6"}
                    </span>
                  </button>
                )
              )}
            </div>

            {/* Questions List */}
            <div className="space-y-6">
              {getCategoryQuestions(activeTab).map((question, index) => (
                <div
                  key={index}
                  className="premium-card rounded-lg border-l-4 border-blue-500 overflow-hidden"
                >
                  {/* Question Header */}
                  <div
                    className={`question-card question-${activeTab} cursor-pointer p-4`}
                    onClick={() => getExplanation(question)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full font-medium">
                            Q{index + 1}
                          </span>
                          <span className={`category-badge badge-${activeTab}`}>
                            {activeTab}
                          </span>
                          {question.marks_weightage && (
                            <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full font-medium">
                              {question.marks_weightage} Marks
                            </span>
                          )}
                        </div>
                        <p className="font-medium text-gray-900 mb-3 text-lg leading-relaxed">
                          {question.text}
                        </p>
                        <div className="flex items-center space-x-4 text-sm text-gray-500">
                          <span>
                            Confidence:{" "}
                            {(question.confidence_score * 100).toFixed(0)}%
                          </span>
                          {question.topic && (
                            <span>Topic: {question.topic}</span>
                          )}
                          {question.difficulty && (
                            <span
                              className={`px-2 py-1 rounded text-xs ${
                                question.difficulty === "Easy"
                                  ? "bg-green-100 text-green-700"
                                  : question.difficulty === "Medium"
                                  ? "bg-yellow-100 text-yellow-700"
                                  : "bg-red-100 text-red-700"
                              }`}
                            >
                              {question.difficulty}
                            </span>
                          )}
                        </div>
                      </div>
                      <button className="text-blue-500 hover:text-blue-700 ml-4 px-4 py-2 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors">
                        Get Detailed Explanation →
                      </button>
                    </div>
                  </div>

                  {/* Comprehensive Explanation Section */}
                  {selectedQuestion &&
                    selectedQuestion.text === question.text &&
                    explanation && (
                      <div className="border-t border-gray-200 bg-gradient-to-br from-blue-50 to-indigo-50">
                        <div className="p-6 space-y-8">
                          {/* Question Info Header */}
                          <div className="bg-white p-4 rounded-lg border-l-4 border-blue-500 shadow-sm">
                            <div className="flex items-center justify-between mb-2">
                              <h3 className="text-lg font-bold text-gray-900">
                                📚 Comprehensive Analysis
                              </h3>
                              <div className="flex items-center space-x-2">
                                {selectedQuestion.marks_weightage && (
                                  <span className="bg-green-100 text-green-800 text-sm px-3 py-1 rounded-full font-semibold">
                                    {selectedQuestion.marks_weightage} Marks
                                  </span>
                                )}
                                <span className="bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full font-semibold">
                                  {selectedQuestion.difficulty || "Medium"}{" "}
                                  Level
                                </span>
                              </div>
                            </div>
                            <p className="text-gray-700 font-medium">
                              {selectedQuestion.text}
                            </p>
                          </div>

                          {/* Detailed Explanation */}
                          <div className="bg-white rounded-lg shadow-sm border">
                            <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4 rounded-t-lg">
                              <h4 className="font-bold text-lg flex items-center">
                                <span className="mr-3">📖</span>
                                Detailed Step-by-Step Explanation
                              </h4>
                            </div>
                            <div className="p-6">
                              <div className="prose prose-lg max-w-none">
                                <div className="text-gray-800 leading-relaxed whitespace-pre-line text-base">
                                  {explanation.explanation}
                                </div>
                              </div>
                            </div>
                          </div>

                          {/* Interactive Diagrams Section */}
                          {explanation.diagrams &&
                            explanation.diagrams.length > 0 && (
                              <div className="bg-white rounded-lg shadow-sm border">
                                <div className="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-4 rounded-t-lg">
                                  <h4 className="font-bold text-lg flex items-center">
                                    <span className="mr-3">📊</span>
                                    Interactive Visual Diagrams
                                  </h4>
                                </div>
                                <div className="p-6 space-y-8">
                                  {explanation.diagrams.map((diagram, idx) => (
                                    <SimpleDiagramRenderer
                                      key={idx}
                                      diagram={diagram}
                                      className="bg-gradient-to-br from-purple-50 to-indigo-50 p-4 rounded-lg border-l-4 border-purple-400"
                                    />
                                  ))}
                                </div>
                              </div>
                            )}

                          {/* Marks Breakdown & Time Allocation */}
                          {(explanation.marks_breakdown ||
                            explanation.time_allocation) && (
                            <div className="grid md:grid-cols-2 gap-6">
                              {explanation.marks_breakdown && (
                                <div className="bg-white rounded-lg shadow-sm border">
                                  <div className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white p-4 rounded-t-lg">
                                    <h4 className="font-bold text-lg flex items-center">
                                      <span className="mr-3">🎯</span>
                                      Marks Distribution
                                    </h4>
                                  </div>
                                  <div className="p-4">
                                    <div className="space-y-2">
                                      {Object.entries(
                                        explanation.marks_breakdown
                                      ).map(([component, marks]) => (
                                        <div
                                          key={component}
                                          className="flex justify-between items-center p-2 bg-yellow-50 rounded"
                                        >
                                          <span className="text-gray-700 font-medium">
                                            {component}
                                          </span>
                                          <span className="bg-yellow-200 text-yellow-800 px-2 py-1 rounded font-bold">
                                            {marks} marks
                                          </span>
                                        </div>
                                      ))}
                                    </div>
                                  </div>
                                </div>
                              )}

                              {explanation.time_allocation && (
                                <div className="bg-white rounded-lg shadow-sm border">
                                  <div className="bg-gradient-to-r from-indigo-500 to-blue-500 text-white p-4 rounded-t-lg">
                                    <h4 className="font-bold text-lg flex items-center">
                                      <span className="mr-3">⏰</span>
                                      Time Management
                                    </h4>
                                  </div>
                                  <div className="p-4">
                                    <div className="bg-indigo-50 p-3 rounded-lg">
                                      <p className="text-gray-800 font-medium">
                                        {explanation.time_allocation}
                                      </p>
                                    </div>
                                  </div>
                                </div>
                              )}
                            </div>
                          )}

                          {/* Answer Structure */}
                          {explanation.answer_structure &&
                            explanation.answer_structure.length > 0 && (
                              <div className="bg-white rounded-lg shadow-sm border">
                                <div className="bg-gradient-to-r from-teal-500 to-cyan-500 text-white p-4 rounded-t-lg">
                                  <h4 className="font-bold text-lg flex items-center">
                                    <span className="mr-3">📝</span>
                                    Perfect Answer Structure
                                  </h4>
                                </div>
                                <div className="p-4">
                                  <ol className="space-y-2">
                                    {explanation.answer_structure.map(
                                      (point, idx) => (
                                        <li
                                          key={idx}
                                          className="flex items-start p-3 bg-teal-50 rounded-lg border-l-4 border-teal-400"
                                        >
                                          <span className="bg-teal-200 text-teal-800 rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">
                                            {idx + 1}
                                          </span>
                                          <span className="text-gray-800 font-medium leading-relaxed">
                                            {point}
                                          </span>
                                        </li>
                                      )
                                    )}
                                  </ol>
                                </div>
                              </div>
                            )}

                          {/* Key Points and Exam Tips Grid */}
                          <div className="grid lg:grid-cols-2 gap-6">
                            {/* Memory Techniques & Key Points */}
                            <div className="bg-white rounded-lg shadow-sm border">
                              <div className="bg-gradient-to-r from-green-500 to-green-600 text-white p-4 rounded-t-lg">
                                <h4 className="font-bold text-lg flex items-center">
                                  <span className="mr-3">🧠</span>
                                  Memory Techniques & Key Points
                                </h4>
                              </div>
                              <div className="p-4">
                                <ul className="space-y-3">
                                  {explanation.key_points.map((point, idx) => (
                                    <li
                                      key={idx}
                                      className="flex items-start p-3 bg-green-50 rounded-lg border-l-4 border-green-400"
                                    >
                                      <span className="text-green-600 mr-3 mt-1 font-bold text-lg">
                                        {idx + 1}.
                                      </span>
                                      <span className="text-gray-800 font-medium leading-relaxed">
                                        {point}
                                      </span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            </div>

                            {/* Exam Strategy & Scoring Tips */}
                            <div className="bg-white rounded-lg shadow-sm border">
                              <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white p-4 rounded-t-lg">
                                <h4 className="font-bold text-lg flex items-center">
                                  <span className="mr-3">🎯</span>
                                  Exam Strategy & Scoring Tips
                                </h4>
                              </div>
                              <div className="p-4">
                                <ul className="space-y-3">
                                  {explanation.exam_tips.map((tip, idx) => (
                                    <li
                                      key={idx}
                                      className="flex items-start p-3 bg-orange-50 rounded-lg border-l-4 border-orange-400"
                                    >
                                      <span className="text-orange-600 mr-3 mt-1 font-bold">
                                        ✓
                                      </span>
                                      <span className="text-gray-800 font-medium leading-relaxed">
                                        {tip}
                                      </span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            </div>
                          </div>

                          {/* Additional Study Resources */}
                          <div className="bg-white rounded-lg shadow-sm border">
                            <div className="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-4 rounded-t-lg">
                              <h4 className="font-bold text-lg flex items-center">
                                <span className="mr-3">📊</span>
                                Visual Learning & Diagrams
                              </h4>
                            </div>
                            <div className="p-4">
                              <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-400">
                                <p className="text-gray-800 font-medium mb-2">
                                  <strong>📈 Recommended Visual Aids:</strong>
                                </p>
                                <ul className="text-gray-700 space-y-1 ml-4">
                                  <li>
                                    • Create flowcharts for process-based
                                    questions
                                  </li>
                                  <li>
                                    • Use mind maps for concept relationships
                                  </li>
                                  <li>
                                    • Draw diagrams with proper labels and
                                    annotations
                                  </li>
                                  <li>
                                    • Include graphs, charts, or tables where
                                    applicable
                                  </li>
                                </ul>
                              </div>
                            </div>
                          </div>

                          {/* Action Buttons */}
                          <div className="flex justify-center space-x-4 pt-4">
                            <button
                              onClick={() => setSelectedQuestion(null)}
                              className="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors font-medium"
                            >
                              Close Explanation
                            </button>
                            <button
                              onClick={() => window.print()}
                              className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors font-medium"
                            >
                              Print/Save
                            </button>
                          </div>
                        </div>
                      </div>
                    )}
                </div>
              ))}

              {getCategoryQuestions(activeTab).length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <p>No {activeTab} questions found.</p>
                  <p className="text-sm">
                    Try uploading more documents or check other categories.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Explanation Panel */}
        <div className="lg:col-span-1">
          <div className="card sticky top-4">
            {selectedQuestion && explanation ? (
              <div>
                <h3 className="text-lg font-semibold mb-4">AI Explanation</h3>

                <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                  <p className="text-sm font-medium text-gray-700">Question:</p>
                  <p className="text-sm">{selectedQuestion.text}</p>
                </div>

                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">
                      Explanation:
                    </h4>
                    <p className="text-sm text-gray-700 leading-relaxed">
                      {explanation.explanation}
                    </p>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">
                      Key Points:
                    </h4>
                    <ul className="text-sm text-gray-700 space-y-1">
                      {explanation.key_points.map((point, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-blue-500 mr-2">•</span>
                          {point}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">
                      Exam Tips:
                    </h4>
                    <ul className="text-sm text-gray-700 space-y-1">
                      {explanation.exam_tips.map((tip, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-green-500 mr-2">✓</span>
                          {tip}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <div className="w-16 h-16 gradient-bg rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span className="text-white text-2xl">💡</span>
                </div>
                <p className="font-medium mb-2">Get AI Explanations</p>
                <p className="text-sm">
                  Click on any question to get detailed explanations and study
                  tips.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="mt-8 flex space-x-4">
        <button onClick={() => navigate("/upload")} className="btn-secondary">
          Upload More Documents
        </button>
        <button onClick={() => navigate("/setup")} className="btn-secondary">
          New Subject
        </button>
      </div>
    </div>
  );
};

export default QuestionAnalysis;
