import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Home from "./pages/Home";
import SubjectSetup from "./pages/SubjectSetup";
import DocumentUpload from "./pages/DocumentUpload";
import QuestionAnalysis from "./pages/QuestionAnalysis";
import History from "./pages/History";
import Quiz from "./pages/Quiz";
import QuizResult from "./pages/QuizResult";
import NotificationSystem from "./components/NotificationSystem";
import "./App.css";

function App() {
  const [currentSubject, setCurrentSubject] = useState(null);
  const [studySession, setStudySession] = useState(null);

  return (
    <Router
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route
              path="/setup"
              element={<SubjectSetup onSubjectSetup={setCurrentSubject} />}
            />
            <Route
              path="/upload"
              element={
                <DocumentUpload
                  subject={currentSubject}
                  onSessionCreated={setStudySession}
                />
              }
            />
            <Route
              path="/analysis"
              element={<QuestionAnalysis session={studySession} />}
            />
            <Route path="/history" element={<History />} />
            <Route path="/quiz" element={<Quiz />} />
            <Route path="/quiz-result" element={<QuizResult />} />
          </Routes>
        </main>
        <NotificationSystem />
      </div>
    </Router>
  );
}

export default App;
