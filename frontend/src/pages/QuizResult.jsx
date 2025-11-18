import { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import axios from "axios";
import API_URL from "../config/api";

const QuizResult = () => {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get("session");
  const navigate = useNavigate();

  const [result, setResult] = useState(null);
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    const storedResult = sessionStorage.getItem(`quiz_result_${sessionId}`);
    if (storedResult) {
      setResult(JSON.parse(storedResult));
      fetchHistory();
    } else {
      setLoading(false);
    }
  }, [sessionId]);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/quiz/quiz/history/${sessionId}?user_id=demo_user`
      );
      setHistory(response.data);
    } catch (err) {
      console.error("Failed to fetch quiz history:", err);
    } finally {
      setLoading(false);
    }
  };

  const getGradeColor = (grade) => {
    const colors = {
      "A+": "text-green-600 bg-green-100",
      A: "text-green-600 bg-green-100",
      B: "text-blue-600 bg-blue-100",
      C: "text-yellow-600 bg-yellow-100",
      D: "text-orange-600 bg-orange-100",
      F: "text-red-600 bg-red-100",
    };
    return colors[grade] || "text-gray-600 bg-gray-100";
  };

  const getMasteryColor = (level) => {
    const colors = {
      Expert: "text-purple-600",
      Advanced: "text-green-600",
      Intermediate: "text-blue-600",
      Beginner: "text-yellow-600",
      Novice: "text-orange-600",
      "Needs Improvement": "text-red-600",
    };
    return colors[level] || "text-gray-600";
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
  };

  const formatDate = (dateString) => {
    try {
      return new Date(dateString).toLocaleString();
    } catch {
      return "Unknown";
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card text-center">
          <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold mb-2">Loading Results</h2>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card text-center">
          <h2 className="text-xl font-semibold mb-2">No Results Found</h2>
          <button
            onClick={() => navigate("/history")}
            className="btn-primary mt-4"
          >
            Back to History
          </button>
        </div>
      </div>
    );
  }

  const feedback = result.ai_feedback || {};

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="card text-center">
        <div className="w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center text-4xl bg-gradient-to-br from-blue-500 to-purple-500">
          {result.percentage >= 75
            ? "🎉"
            : result.percentage >= 50
            ? "📚"
            : "💪"}
        </div>
        <h1 className="text-3xl font-bold mb-2">Quiz Completed!</h1>
        <p className="text-gray-600">Here's how you performed</p>
      </div>

      {/* Score Card */}
      <div className="card">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">
              {result.percentage}%
            </div>
            <div className="text-sm text-gray-600">Score</div>
          </div>
          <div className="text-center">
            <div
              className={`text-3xl font-bold px-4 py-2 rounded-lg inline-block ${getGradeColor(
                result.grade
              )}`}
            >
              {result.grade}
            </div>
            <div className="text-sm text-gray-600 mt-1">Grade</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">
              {result.correct_answers}/{result.total_questions}
            </div>
            <div className="text-sm text-gray-600">Correct</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">
              {formatTime(result.time_taken)}
            </div>
            <div className="text-sm text-gray-600">Time</div>
          </div>
        </div>

        {/* Learning Status */}
        <div
          className={`p-4 rounded-lg ${
            result.percentage >= 75
              ? "bg-green-50 border border-green-200"
              : result.percentage >= 60
              ? "bg-yellow-50 border border-yellow-200"
              : "bg-red-50 border border-red-200"
          }`}
        >
          <div className="text-lg font-semibold mb-2">
            {feedback.learning_status}
          </div>
          <p className="text-gray-700">{feedback.learning_message}</p>
        </div>
      </div>

      {/* AI Feedback */}
      <div className="card">
        <h2 className="text-xl font-bold mb-4">🤖 AI Assessment</h2>

        <div className="space-y-4">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold">Mastery Level:</span>
              <span
                className={`font-bold ${getMasteryColor(
                  feedback.mastery_level
                )}`}
              >
                {feedback.mastery_level}
              </span>
            </div>
            <p className="text-gray-700 bg-gray-50 p-3 rounded">
              {feedback.overall_assessment}
            </p>
          </div>

          <div>
            <div className="font-semibold mb-2">Recommendation:</div>
            <p className="text-gray-700 bg-blue-50 p-3 rounded border-l-4 border-blue-500">
              {feedback.recommendation}
            </p>
          </div>

          {feedback.time_feedback && (
            <div>
              <div className="font-semibold mb-2">Time Management:</div>
              <p className="text-gray-700">{feedback.time_feedback}</p>
            </div>
          )}

          {feedback.suggestions && feedback.suggestions.length > 0 && (
            <div>
              <div className="font-semibold mb-2">
                Suggestions for Improvement:
              </div>
              <ul className="list-disc list-inside space-y-1">
                {feedback.suggestions.map((suggestion, index) => (
                  <li key={index} className="text-gray-700">
                    {suggestion}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* Performance by Topic */}
      {result.topic_performance &&
        Object.keys(result.topic_performance).length > 0 && (
          <div className="card">
            <h2 className="text-xl font-bold mb-4">📊 Performance by Topic</h2>
            <div className="space-y-3">
              {Object.entries(result.topic_performance).map(([topic, perf]) => {
                const percentage = ((perf.correct / perf.total) * 100).toFixed(
                  0
                );
                return (
                  <div key={topic}>
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-medium">{topic}</span>
                      <span className="text-sm text-gray-600">
                        {perf.correct}/{perf.total} ({percentage}%)
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          percentage >= 80
                            ? "bg-green-500"
                            : percentage >= 60
                            ? "bg-yellow-500"
                            : "bg-red-500"
                        }`}
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>

            {(result.weak_areas?.length > 0 ||
              result.strong_areas?.length > 0) && (
              <div className="mt-4 grid grid-cols-2 gap-4">
                {result.strong_areas?.length > 0 && (
                  <div className="bg-green-50 p-3 rounded">
                    <div className="font-semibold text-green-800 mb-2">
                      ✓ Strong Areas
                    </div>
                    <ul className="text-sm text-green-700 space-y-1">
                      {result.strong_areas.map((area, index) => (
                        <li key={index}>• {area}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {result.weak_areas?.length > 0 && (
                  <div className="bg-red-50 p-3 rounded">
                    <div className="font-semibold text-red-800 mb-2">
                      ⚠ Needs Improvement
                    </div>
                    <ul className="text-sm text-red-700 space-y-1">
                      {result.weak_areas.map((area, index) => (
                        <li key={index}>• {area}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

      {/* Quiz History */}
      {history && history.total_attempts > 0 && (
        <div className="card">
          <h2 className="text-xl font-bold mb-4">📈 Quiz History</h2>
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="bg-gray-50 p-3 rounded text-center">
              <div className="text-2xl font-bold text-blue-600">
                {history.total_attempts}
              </div>
              <div className="text-sm text-gray-600">Total Attempts</div>
            </div>
            <div className="bg-gray-50 p-3 rounded text-center">
              <div className="text-2xl font-bold text-green-600">
                {history.best_score}%
              </div>
              <div className="text-sm text-gray-600">Best Score</div>
            </div>
            <div className="bg-gray-50 p-3 rounded text-center">
              <div className="text-2xl font-bold text-purple-600">
                {history.average_score}%
              </div>
              <div className="text-sm text-gray-600">Average Score</div>
            </div>
          </div>

          {history.improvement_trend !== 0 && (
            <div
              className={`p-3 rounded ${
                history.improvement_trend > 0
                  ? "bg-green-50 text-green-700"
                  : "bg-red-50 text-red-700"
              }`}
            >
              {history.improvement_trend > 0 ? "📈" : "📉"} Your score{" "}
              {history.improvement_trend > 0 ? "improved" : "decreased"} by{" "}
              {Math.abs(history.improvement_trend)}% compared to previous
              attempts
            </div>
          )}

          <button
            onClick={() => setShowDetails(!showDetails)}
            className="mt-4 text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            {showDetails ? "Hide" : "Show"} Previous Attempts
          </button>

          {showDetails && (
            <div className="mt-4 space-y-2">
              {history.quiz_attempts.slice(0, 5).map((attempt, index) => (
                <div
                  key={index}
                  className="bg-gray-50 p-3 rounded flex justify-between items-center"
                >
                  <div>
                    <div className="font-medium">
                      Attempt #{history.total_attempts - index}
                    </div>
                    <div className="text-sm text-gray-600">
                      {formatDate(attempt.completed_at)}
                    </div>
                  </div>
                  <div className="text-right">
                    <div
                      className={`font-bold ${getGradeColor(
                        attempt.grade
                      )} px-3 py-1 rounded`}
                    >
                      {attempt.percentage}% ({attempt.grade})
                    </div>
                    <div className="text-sm text-gray-600">
                      {formatTime(attempt.time_taken)}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4 flex-wrap gap-2">
        <button
          onClick={() => navigate(`/quiz?session=${sessionId}`)}
          className="btn-primary"
        >
          🔄 Retake Quiz (New Questions)
        </button>
        <button
          onClick={() => {
            window.open(
              `${API_URL}/quiz/quiz/download/${sessionId}`,
              "_blank"
            );
          }}
          className="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg transition-colors font-medium"
        >
          📥 Download Questions (CSV)
        </button>
        <button onClick={() => navigate("/history")} className="btn-secondary">
          ← Back to History
        </button>
      </div>
    </div>
  );
};

export default QuizResult;
