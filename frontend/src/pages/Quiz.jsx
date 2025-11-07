import { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import axios from "axios";

const Quiz = () => {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get("session");
  const navigate = useNavigate();

  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [quizStarted, setQuizStarted] = useState(false);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [timeLeft, setTimeLeft] = useState(1800); // 30 minutes

  useEffect(() => {
    if (sessionId) {
      fetchSession();
    } else {
      setError("No session ID provided");
      setLoading(false);
    }
  }, [sessionId]);

  useEffect(() => {
    let timer;
    if (quizStarted && timeLeft > 0) {
      timer = setInterval(() => {
        setTimeLeft((prev) => prev - 1);
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [quizStarted, timeLeft]);

  const fetchSession = async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        `http://localhost:8000/api/analysis/session/${sessionId}`
      );
      setSession(response.data);
    } catch (err) {
      setError("Failed to load session");
      console.error("Session fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  const generateQuizQuestions = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        `http://localhost:8000/api/quiz/quiz/generate/${sessionId}?question_count=20`
      );
      return response.data.questions;
    } catch (err) {
      console.error("Failed to generate quiz questions:", err);
      setError("Failed to generate quiz questions. Please try again.");
      return [];
    } finally {
      setLoading(false);
    }
  };

  const startQuiz = async () => {
    const questions = await generateQuizQuestions();
    if (questions.length > 0) {
      setQuizQuestions(questions);
      setQuizStarted(true);
      setCurrentQuestionIndex(0);
      setAnswers({});
      setTimeLeft(1800); // Reset timer
    }
  };

  const handleAnswerSelect = (questionId, answerIndex) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: answerIndex,
    }));
  };

  const nextQuestion = () => {
    if (currentQuestionIndex < quizQuestions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
    }
  };

  const previousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
    }
  };

  const submitQuiz = async () => {
    try {
      const timeTaken = 1800 - timeLeft; // Calculate actual time taken

      const quizData = {
        session_id: sessionId,
        user_id: "demo_user",
        answers: answers,
        questions: quizQuestions,
        time_taken: timeTaken,
      };

      const response = await axios.post(
        "http://localhost:8000/api/quiz/quiz/submit",
        quizData
      );

      const result = response.data;

      // Store result in session storage for the results page
      sessionStorage.setItem(
        `quiz_result_${sessionId}`,
        JSON.stringify(result)
      );

      // Navigate to results page
      navigate(`/quiz-result?session=${sessionId}`);
    } catch (err) {
      console.error("Failed to submit quiz:", err);
      setError("Failed to submit quiz. Please try again.");
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card text-center">
          <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold mb-2">Loading Quiz</h2>
          <p className="text-gray-600">Preparing your quiz...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card text-center">
          <div className="w-16 h-16 bg-red-100 rounded-full mx-auto mb-4 flex items-center justify-center">
            <span className="text-red-500 text-2xl">⚠️</span>
          </div>
          <h2 className="text-xl font-semibold mb-2 text-red-600">Error</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button onClick={() => navigate("/history")} className="btn-primary">
            Back to History
          </button>
        </div>
      </div>
    );
  }

  if (!quizStarted) {
    const questionCount = session?.question_set
      ? (session.question_set.frequent_questions?.length || 0) +
        (session.question_set.moderate_questions?.length || 0) +
        (session.question_set.important_questions?.length || 0) +
        (session.question_set.predicted_questions?.length || 0)
      : 0;

    return (
      <div className="max-w-4xl mx-auto">
        <div className="card text-center">
          <div className="w-16 h-16 gradient-bg rounded-full mx-auto mb-4 flex items-center justify-center">
            <span className="text-white text-2xl">🧠</span>
          </div>
          <h1 className="text-2xl font-bold mb-2">
            Quiz: {session?.display_name || session?.subject}
          </h1>
          <p className="text-gray-600 mb-2">
            Test your knowledge with AI-generated questions from this session
          </p>
          <p className="text-sm text-blue-600 mb-6">
            💡 Each quiz attempt will have different questions and options
          </p>

          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <div className="font-medium text-gray-700">Questions</div>
                <div className="text-lg font-bold text-blue-600">20</div>
              </div>
              <div>
                <div className="font-medium text-gray-700">Time Limit</div>
                <div className="text-lg font-bold text-blue-600">30 min</div>
              </div>
              <div>
                <div className="font-medium text-gray-700">
                  Available Questions
                </div>
                <div className="text-lg font-bold text-blue-600">
                  {questionCount}
                </div>
              </div>
              <div>
                <div className="font-medium text-gray-700">Question Types</div>
                <div className="text-lg font-bold text-blue-600">Mixed</div>
              </div>
            </div>
          </div>

          {questionCount >= 20 ? (
            <div className="space-y-4">
              <button
                onClick={startQuiz}
                className="btn-primary text-lg px-8 py-3"
              >
                Start Quiz
              </button>
              <div>
                <button
                  onClick={() => navigate("/history")}
                  className="text-gray-500 hover:text-gray-700"
                >
                  Back to History
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <p className="text-red-600">
                Not enough questions available. Need at least 20 questions to
                start a quiz.
              </p>
              <button
                onClick={() => navigate("/history")}
                className="btn-secondary"
              >
                Back to History
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  const currentQuestion = quizQuestions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / quizQuestions.length) * 100;

  return (
    <div className="max-w-4xl mx-auto">
      {/* Quiz Header */}
      <div className="card mb-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-xl font-bold">
            Quiz: {session?.display_name || session?.subject}
          </h1>
          <div className="text-lg font-mono text-red-600">
            ⏰ {formatTime(timeLeft)}
          </div>
        </div>

        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-gray-600">
            Question {currentQuestionIndex + 1} of {quizQuestions.length}
          </span>
          <span className="text-sm text-gray-600">
            {Math.round(progress)}% Complete
          </span>
        </div>

        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-500 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>

      {/* Question Card */}
      <div className="card mb-6">
        <div className="mb-4">
          <div className="flex justify-between items-start mb-3">
            <h2 className="text-lg font-semibold">
              Question {currentQuestion.id}
            </h2>
            <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
              {currentQuestion.marks || 1} mark
              {(currentQuestion.marks || 1) !== 1 ? "s" : ""}
            </span>
          </div>
          <p className="text-gray-800 leading-relaxed">
            {currentQuestion.text}
          </p>
        </div>

        <div className="space-y-3">
          {currentQuestion.options.map((option, index) => (
            <label
              key={index}
              className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${
                answers[currentQuestion.id] === index
                  ? "border-blue-500 bg-blue-50"
                  : "border-gray-200 hover:border-gray-300"
              }`}
            >
              <input
                type="radio"
                name={`question-${currentQuestion.id}`}
                value={index}
                checked={answers[currentQuestion.id] === index}
                onChange={() => handleAnswerSelect(currentQuestion.id, index)}
                className="mr-3"
              />
              <span className="flex-1">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center">
        <button
          onClick={previousQuestion}
          disabled={currentQuestionIndex === 0}
          className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ← Previous
        </button>

        <div className="flex space-x-2">
          {quizQuestions.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentQuestionIndex(index)}
              className={`w-8 h-8 rounded text-xs font-medium ${
                index === currentQuestionIndex
                  ? "bg-blue-500 text-white"
                  : answers[quizQuestions[index].id] !== undefined
                  ? "bg-green-100 text-green-800"
                  : "bg-gray-100 text-gray-600"
              }`}
            >
              {index + 1}
            </button>
          ))}
        </div>

        {currentQuestionIndex === quizQuestions.length - 1 ? (
          <button onClick={submitQuiz} className="btn-primary">
            Submit Quiz
          </button>
        ) : (
          <button onClick={nextQuestion} className="btn-primary">
            Next →
          </button>
        )}
      </div>
    </div>
  );
};

export default Quiz;
