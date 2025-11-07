import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const SubjectSetup = ({ onSubjectSetup }) => {
  const [subjectName, setSubjectName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!subjectName.trim()) {
      setError("Please enter a subject name");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await axios.post(
        "http://localhost:8000/api/subjects/setup",
        {
          subject_name: subjectName,
          user_id: "demo_user", // In a real app, this would come from authentication
        }
      );

      onSubjectSetup(response.data);
      navigate("/upload");
    } catch (err) {
      setError("Failed to setup subject. Please try again.");
      console.error("Subject setup error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="card">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold gradient-text mb-4">
            Setup Your Subject
          </h1>
          <p className="text-gray-600">
            Let's start by setting up the subject you want to study. Our AI will
            customize the experience based on your chosen subject.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label
              htmlFor="subject"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Subject Name
            </label>
            <input
              type="text"
              id="subject"
              value={subjectName}
              onChange={(e) => setSubjectName(e.target.value)}
              placeholder="e.g., Mathematics, Physics, Computer Science"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={loading}
            />
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div className="flex space-x-4">
            <button
              type="submit"
              disabled={loading}
              className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Setting up..." : "Setup Subject"}
            </button>
            <button
              type="button"
              onClick={() => navigate("/")}
              className="btn-secondary"
            >
              Back
            </button>
          </div>
        </form>

        {/* Popular Subjects */}
        <div className="mt-8 pt-6 border-t border-gray-200">
          <h3 className="text-sm font-medium text-gray-700 mb-3">
            Popular Subjects:
          </h3>
          <div className="flex flex-wrap gap-2">
            {[
              "Mathematics",
              "Physics",
              "Chemistry",
              "Computer Science",
              "Biology",
              "History",
              "Economics",
              "English",
            ].map((subject) => (
              <button
                key={subject}
                onClick={() => setSubjectName(subject)}
                className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-blue-100 hover:text-blue-700 transition-colors"
                disabled={loading}
              >
                {subject}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubjectSetup;
