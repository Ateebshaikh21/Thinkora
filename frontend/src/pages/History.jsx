import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import API_URL from "../config/api";

const History = () => {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [editingSessionId, setEditingSessionId] = useState(null);
  const [editSessionId, setEditSessionId] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        `${API_URL}/analysis/sessions?user_id=demo_user`
      );
      setSessions(response.data.sessions || []);
    } catch (err) {
      setError("Failed to load session history");
      console.error("History fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "Unknown";
    try {
      return new Date(dateString).toLocaleString();
    } catch {
      return "Invalid date";
    }
  };

  const getDocumentCount = (session) => {
    return session.documents ? session.documents.length : 0;
  };

  const getQuestionCount = (session) => {
    if (!session.question_set) return 0;
    const questionSet = session.question_set;
    return (
      (questionSet.frequent_questions?.length || 0) +
      (questionSet.moderate_questions?.length || 0) +
      (questionSet.important_questions?.length || 0) +
      (questionSet.predicted_questions?.length || 0)
    );
  };

  const handleViewSession = (sessionId) => {
    // Navigate to analysis page with the session
    navigate(`/analysis?session=${sessionId}`);
  };

  const handleStartQuiz = (sessionId) => {
    // Navigate to quiz page with the session
    navigate(`/quiz?session=${sessionId}`);
  };

  const handleViewQuizHistory = (sessionId) => {
    // Navigate to quiz result page to see history
    navigate(`/quiz-result?session=${sessionId}`);
  };

  const handleDeleteSession = async (sessionId) => {
    if (!window.confirm("Are you sure you want to delete this session?")) {
      return;
    }

    try {
      await axios.delete(
        `${API_URL}/analysis/session/${sessionId}`
      );
      setSessions(sessions.filter((s) => s.id !== sessionId));
    } catch (err) {
      setError("Failed to delete session");
      console.error("Delete error:", err);
    }
  };

  const handleEditSessionId = (session) => {
    setEditingSessionId(session.id || session._id);
    setEditSessionId(session.id || session._id || "");
  };

  const handleSaveSessionId = async (oldSessionId) => {
    try {
      const response = await axios.put(
        `${API_URL}/analysis/session/${oldSessionId}/rename?new_id=${editSessionId}`
      );

      // Create a clean display name from the new session ID
      const cleanDisplayName = editSessionId
        .split("-")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");

      // Update local state with new ID and display name
      setSessions(
        sessions.map((s) =>
          (s.id || s._id) === oldSessionId
            ? {
                ...s,
                id: response.data.new_id,
                _id: response.data.new_id,
                display_name: cleanDisplayName,
              }
            : s
        )
      );

      setEditingSessionId(null);
      setEditSessionId("");
    } catch (err) {
      if (err.response?.status === 409) {
        setError("Session ID already exists. Please choose a different name.");
      } else {
        setError("Failed to update session ID");
      }
      console.error("Session ID edit error:", err);
    }
  };

  const handleCancelSessionIdEdit = () => {
    setEditingSessionId(null);
    setEditSessionId("");
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="card text-center">
          <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold mb-2">Loading History</h2>
          <p className="text-gray-600">Fetching your study sessions...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold gradient-text mb-4">Study History</h1>
        <p className="text-gray-600">
          View and manage your previous study sessions and analysis results.
        </p>
      </div>

      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {sessions.length === 0 ? (
        <div className="card text-center">
          <div className="w-16 h-16 gradient-bg rounded-full mx-auto mb-4 flex items-center justify-center">
            <span className="text-white text-2xl">📚</span>
          </div>
          <h2 className="text-xl font-semibold mb-2">No Study Sessions Yet</h2>
          <p className="text-gray-600 mb-6">
            Start by creating your first study session to see your history here.
          </p>
          <button onClick={() => navigate("/setup")} className="btn-primary">
            Start New Session
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {sessions.map((session) => (
            <div
              key={session.id || session._id}
              className="card hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {session.display_name ||
                        session.subject ||
                        "Unknown Session"}
                    </h3>
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                      {session.subject || "Study Session"}
                    </span>
                  </div>

                  {/* Session ID Display/Edit */}
                  <div className="mb-3 p-2 bg-gray-50 rounded">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-medium text-gray-500">
                          Session ID:
                        </span>
                        {editingSessionId === (session.id || session._id) ? (
                          <div className="flex items-center space-x-2">
                            <input
                              type="text"
                              value={editSessionId}
                              onChange={(e) => setEditSessionId(e.target.value)}
                              className="text-xs bg-white border border-gray-300 rounded px-2 py-1 w-48"
                              placeholder="Enter session ID"
                            />
                            <button
                              onClick={() =>
                                handleSaveSessionId(session.id || session._id)
                              }
                              className="text-green-600 hover:text-green-800 text-xs px-1"
                            >
                              ✓
                            </button>
                            <button
                              onClick={handleCancelSessionIdEdit}
                              className="text-red-600 hover:text-red-800 text-xs px-1"
                            >
                              ✗
                            </button>
                          </div>
                        ) : (
                          <div className="flex items-center space-x-2">
                            <code className="text-xs bg-white px-2 py-1 rounded border">
                              {session.id || session._id}
                            </code>
                            <button
                              onClick={() => handleEditSessionId(session)}
                              className="text-blue-500 hover:text-blue-700 text-xs"
                              title="Edit session ID"
                            >
                              ✏️
                            </button>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm text-gray-600 mb-4">
                    <div>
                      <span className="font-medium">Documents:</span>
                      <span className="ml-1">{getDocumentCount(session)}</span>
                    </div>
                    <div>
                      <span className="font-medium">Questions:</span>
                      <span className="ml-1">{getQuestionCount(session)}</span>
                    </div>
                    <div>
                      <span className="font-medium">Quiz Status:</span>
                      <span className="ml-1">
                        {session.question_set &&
                        getQuestionCount(session) > 0 ? (
                          <span className="text-green-600">✓ Ready</span>
                        ) : (
                          <span className="text-gray-400">Not Ready</span>
                        )}
                      </span>
                    </div>
                    <div>
                      <span className="font-medium">Created:</span>
                      <span className="ml-1">
                        {formatDate(session.created_at)}
                      </span>
                    </div>
                    <div>
                      <span className="font-medium">Updated:</span>
                      <span className="ml-1">
                        {formatDate(session.updated_at)}
                      </span>
                    </div>
                  </div>

                  {session.documents && session.documents.length > 0 && (
                    <div className="mb-4">
                      <h4 className="text-sm font-medium text-gray-700 mb-2">
                        Documents:
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {session.documents.map((doc, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
                          >
                            📄 {doc.filename}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {session.question_set && (
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                      <div className="bg-green-50 p-2 rounded text-center">
                        <div className="font-medium text-green-800">
                          {session.question_set.frequent_questions?.length || 0}
                        </div>
                        <div className="text-green-600">Frequent</div>
                      </div>
                      <div className="bg-yellow-50 p-2 rounded text-center">
                        <div className="font-medium text-yellow-800">
                          {session.question_set.moderate_questions?.length || 0}
                        </div>
                        <div className="text-yellow-600">Moderate</div>
                      </div>
                      <div className="bg-orange-50 p-2 rounded text-center">
                        <div className="font-medium text-orange-800">
                          {session.question_set.important_questions?.length ||
                            0}
                        </div>
                        <div className="text-orange-600">Important</div>
                      </div>
                      <div className="bg-red-50 p-2 rounded text-center">
                        <div className="font-medium text-red-800">
                          {session.question_set.predicted_questions?.length ||
                            0}
                        </div>
                        <div className="text-red-600">Predicted</div>
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex flex-col space-y-2 ml-4">
                  <button
                    onClick={() => handleViewSession(session.id || session._id)}
                    className="btn-primary text-sm px-4 py-2"
                  >
                    View Analysis
                  </button>
                  <button
                    onClick={() => handleStartQuiz(session.id || session._id)}
                    className="bg-green-500 hover:bg-green-600 text-white text-sm px-4 py-2 rounded-lg transition-colors"
                    disabled={
                      !session.question_set || getQuestionCount(session) === 0
                    }
                  >
                    🧠 Start Quiz
                  </button>
                  <button
                    onClick={() =>
                      handleDeleteSession(session.id || session._id)
                    }
                    className="btn-secondary text-sm px-4 py-2 text-red-600 hover:bg-red-50"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-8 flex justify-center">
        <button onClick={() => navigate("/setup")} className="btn-primary">
          Create New Session
        </button>
      </div>
    </div>
  );
};

export default History;
