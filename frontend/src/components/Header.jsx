import React from "react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <header className="gradient-bg shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3">
            <img
              src="/thinkora-logo.png"
              alt="Thinkora Logo"
              className="h-12 w-auto"
              onError={(e) => {
                // Fallback if logo image is not found
                e.target.style.display = "none";
                e.target.nextSibling.style.display = "flex";
              }}
            />
            <div className="w-10 h-10 bg-white rounded-lg items-center justify-center hidden">
              <span className="text-blue-600 font-bold text-xl">T</span>
            </div>
            <div>
              <h1 className="text-white text-2xl font-bold">Thinkora</h1>
              <p className="text-blue-100 text-sm">
                AI-Powered Smart Study Assistant
              </p>
            </div>
          </Link>

          <nav className="hidden md:flex space-x-6">
            <Link
              to="/"
              className="text-white hover:text-blue-200 transition-colors"
            >
              Home
            </Link>
            <Link
              to="/setup"
              className="text-white hover:text-blue-200 transition-colors"
            >
              Setup Subject
            </Link>
            <Link
              to="/upload"
              className="text-white hover:text-blue-200 transition-colors"
            >
              Upload Documents
            </Link>
            <Link
              to="/analysis"
              className="text-white hover:text-blue-200 transition-colors"
            >
              Analysis
            </Link>
            <Link
              to="/history"
              className="text-white hover:text-blue-200 transition-colors"
            >
              History
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
