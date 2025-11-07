import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="max-w-4xl mx-auto text-center">
      {/* Hero Section */}
      <div className="mb-12">
        <div className="flex justify-center mb-8">
          <img
            src="/thinkora-logo.png"
            alt="Thinkora Logo"
            className="h-32 w-auto"
            onError={(e) => (e.target.style.display = "none")}
          />
        </div>
        <h1 className="text-5xl font-bold gradient-text mb-6">
          Welcome to Thinkora
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Your AI-powered smart study assistant that transforms how you prepare
          for exams with intelligent analysis, personalized quizzes, and
          comprehensive learning insights.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link to="/setup" className="btn-primary text-lg px-8 py-4">
            Start Studying Smart
          </Link>
          <Link to="/history" className="btn-secondary text-lg px-8 py-4">
            View Study History
          </Link>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <div className="card card-hover text-center">
          <div className="w-12 h-12 gradient-bg rounded-lg mx-auto mb-4 flex items-center justify-center">
            <span className="text-white text-xl">📚</span>
          </div>
          <h3 className="text-lg font-semibold mb-2">Smart Analysis</h3>
          <p className="text-gray-600 text-sm">
            AI-powered analysis of your PYQs, notes, and syllabus
          </p>
        </div>

        <div className="card card-hover text-center">
          <div className="w-12 h-12 gradient-bg rounded-lg mx-auto mb-4 flex items-center justify-center">
            <span className="text-white text-xl">🎯</span>
          </div>
          <h3 className="text-lg font-semibold mb-2">Question Categories</h3>
          <p className="text-gray-600 text-sm">
            Frequent, Moderate, Important, and Predicted questions
          </p>
        </div>

        <div className="card card-hover text-center">
          <div className="w-12 h-12 gradient-bg rounded-lg mx-auto mb-4 flex items-center justify-center">
            <span className="text-white text-xl">💡</span>
          </div>
          <h3 className="text-lg font-semibold mb-2">AI Explanations</h3>
          <p className="text-gray-600 text-sm">
            Detailed explanations and study tips for each question
          </p>
        </div>

        <div className="card card-hover text-center">
          <div className="w-12 h-12 gradient-bg rounded-lg mx-auto mb-4 flex items-center justify-center">
            <span className="text-white text-xl">📊</span>
          </div>
          <h3 className="text-lg font-semibold mb-2">Progress Tracking</h3>
          <p className="text-gray-600 text-sm">
            Track your study progress and focus areas
          </p>
        </div>
      </div>

      {/* How it Works */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-6">How Thinkora Works</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-8 h-8 gradient-bg rounded-full mx-auto mb-3 flex items-center justify-center text-white font-bold">
              1
            </div>
            <h3 className="font-semibold mb-2">Setup Subject</h3>
            <p className="text-gray-600 text-sm">
              Choose your subject and let our AI understand your study context
            </p>
          </div>
          <div className="text-center">
            <div className="w-8 h-8 gradient-bg rounded-full mx-auto mb-3 flex items-center justify-center text-white font-bold">
              2
            </div>
            <h3 className="font-semibold mb-2">Upload Materials</h3>
            <p className="text-gray-600 text-sm">
              Upload your PYQs, notes, and syllabus for comprehensive analysis
            </p>
          </div>
          <div className="text-center">
            <div className="w-8 h-8 gradient-bg rounded-full mx-auto mb-3 flex items-center justify-center text-white font-bold">
              3
            </div>
            <h3 className="font-semibold mb-2">Get Smart Questions</h3>
            <p className="text-gray-600 text-sm">
              Receive categorized questions with AI-powered explanations
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
