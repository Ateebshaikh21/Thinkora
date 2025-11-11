import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Header = () => {
  const { user, signOut, isAuthenticated } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const location = useLocation();

  const handleSignOut = async () => {
    try {
      await signOut();
      setShowUserMenu(false);
    } catch (error) {
      console.error("Sign out error:", error);
    }
  };

  // Don't show header on login page
  if (location.pathname === "/login") {
    return null;
  }

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

          <div className="flex items-center space-x-6">
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

            {/* User Profile */}
            {isAuthenticated && user && (
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center space-x-2 bg-white/10 hover:bg-white/20 rounded-full px-3 py-2 transition-colors"
                >
                  {user.photoURL ? (
                    <img
                      src={user.photoURL}
                      alt={user.displayName}
                      className="w-8 h-8 rounded-full border-2 border-white"
                    />
                  ) : (
                    <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center">
                      <span className="text-blue-600 font-bold">
                        {user.displayName?.[0] || user.email?.[0] || "U"}
                      </span>
                    </div>
                  )}
                  <span className="text-white text-sm hidden md:block">
                    {user.displayName || user.email}
                  </span>
                  <svg
                    className="w-4 h-4 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 9l-7 7-7-7"
                    />
                  </svg>
                </button>

                {/* Dropdown Menu */}
                {showUserMenu && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2 z-50">
                    <div className="px-4 py-2 border-b border-gray-200">
                      <p className="text-sm font-semibold text-gray-800">
                        {user.displayName}
                      </p>
                      <p className="text-xs text-gray-500">{user.email}</p>
                    </div>
                    <button
                      onClick={handleSignOut}
                      className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                    >
                      Sign Out
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
