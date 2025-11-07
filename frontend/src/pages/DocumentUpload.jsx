import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const DocumentUpload = ({ subject, onSessionCreated }) => {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFileSelect = (selectedFiles) => {
    const supportedExtensions = [
      ".txt",
      ".pdf",
      ".docx",
      ".xlsx",
      ".csv",
      ".md",
      ".rtf",
    ];
    const newFiles = Array.from(selectedFiles).filter((file) => {
      const extension = file.name
        .toLowerCase()
        .substring(file.name.lastIndexOf("."));
      return supportedExtensions.includes(extension);
    });

    if (newFiles.length !== selectedFiles.length) {
      setError("Supported formats: PDF, DOCX, XLSX, TXT, CSV, MD, RTF");
    } else {
      setError("");
    }

    setFiles((prev) => [...prev, ...newFiles]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFileSelect(e.dataTransfer.files);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const removeFile = (index) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      setError("Please select at least one file");
      return;
    }

    if (!subject) {
      setError("Please setup a subject first");
      return;
    }

    setUploading(true);
    setError("");

    try {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append("files", file);
      });

      const response = await axios.post(
        `http://localhost:8000/api/analysis/upload-documents?subject_id=${subject.subject_id}&user_id=demo_user`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      onSessionCreated(response.data);
      navigate("/analysis");
    } catch (err) {
      setError("Failed to upload documents. Please try again.");
      console.error("Upload error:", err);
    } finally {
      setUploading(false);
    }
  };

  if (!subject) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="card text-center">
          <h2 className="text-2xl font-bold mb-4">No Subject Selected</h2>
          <p className="text-gray-600 mb-6">
            Please setup a subject first before uploading documents.
          </p>
          <button onClick={() => navigate("/setup")} className="btn-primary">
            Setup Subject
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="card">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold gradient-text mb-4">
            Upload Study Materials
          </h1>
          <p className="text-gray-600">
            Upload your PYQs, notes, and syllabus for{" "}
            <strong>{subject.subject_name}</strong>. Our AI will analyze them to
            generate smart question sets.
          </p>
        </div>

        {/* Upload Area */}
        <div
          className={`upload-area ${dragOver ? "dragover" : ""}`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="text-center">
            <div className="w-16 h-16 gradient-bg rounded-full mx-auto mb-4 flex items-center justify-center">
              <span className="text-white text-2xl">📁</span>
            </div>
            <h3 className="text-lg font-semibold mb-2">
              Drop files here or click to browse
            </h3>
            <p className="text-gray-500 text-sm">
              Supported formats: PDF, DOCX, XLSX, TXT, CSV, MD, RTF
            </p>
          </div>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".txt,.pdf,.docx,.xlsx,.csv,.md,.rtf"
          onChange={(e) => handleFileSelect(e.target.files)}
          className="hidden"
        />

        {/* File List */}
        {files.length > 0 && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-4">
              Selected Files ({files.length})
            </h3>
            <div className="space-y-2">
              {files.map((file, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between bg-gray-50 p-3 rounded-lg"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-blue-500">📄</span>
                    <div>
                      <p className="font-medium">{file.name}</p>
                      <p className="text-sm text-gray-500">
                        {(file.size / 1024).toFixed(1)} KB
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => removeFile(index)}
                    className="text-red-500 hover:text-red-700 p-1"
                    disabled={uploading}
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {/* Action Buttons */}
        <div className="mt-8 flex space-x-4">
          <button
            onClick={handleUpload}
            disabled={uploading || files.length === 0}
            className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {uploading ? "Uploading & Analyzing..." : "Upload & Analyze"}
          </button>
          <button
            onClick={() => navigate("/setup")}
            className="btn-secondary"
            disabled={uploading}
          >
            Back
          </button>
        </div>

        {/* Document Types Info */}
        <div className="mt-8 pt-6 border-t border-gray-200">
          <h3 className="text-sm font-medium text-gray-700 mb-3">
            Document Types:
          </h3>
          <div className="grid md:grid-cols-3 gap-4 text-sm mb-6">
            <div className="bg-green-50 p-3 rounded-lg">
              <h4 className="font-medium text-green-800">
                PYQs (Previous Year Questions)
              </h4>
              <p className="text-green-600">
                Past exam questions for pattern analysis
              </p>
            </div>
            <div className="bg-blue-50 p-3 rounded-lg">
              <h4 className="font-medium text-blue-800">Notes</h4>
              <p className="text-blue-600">Study notes and lecture materials</p>
            </div>
            <div className="bg-purple-50 p-3 rounded-lg">
              <h4 className="font-medium text-purple-800">Syllabus</h4>
              <p className="text-purple-600">Course outline and curriculum</p>
            </div>
          </div>

          {/* Supported File Formats */}
          <h3 className="text-sm font-medium text-gray-700 mb-3">
            Supported File Formats:
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
            <div className="bg-gray-50 p-2 rounded text-center">
              <span className="font-medium text-red-600">📄 PDF</span>
              <p className="text-gray-600">Portable Documents</p>
            </div>
            <div className="bg-gray-50 p-2 rounded text-center">
              <span className="font-medium text-blue-600">📝 DOCX</span>
              <p className="text-gray-600">Word Documents</p>
            </div>
            <div className="bg-gray-50 p-2 rounded text-center">
              <span className="font-medium text-green-600">📊 XLSX</span>
              <p className="text-gray-600">Excel Spreadsheets</p>
            </div>
            <div className="bg-gray-50 p-2 rounded text-center">
              <span className="font-medium text-gray-600">📄 TXT</span>
              <p className="text-gray-600">Plain Text</p>
            </div>
            <div className="bg-gray-50 p-2 rounded text-center">
              <span className="font-medium text-orange-600">📋 CSV</span>
              <p className="text-gray-600">Data Tables</p>
            </div>
            <div className="bg-gray-50 p-2 rounded text-center">
              <span className="font-medium text-purple-600">📝 MD</span>
              <p className="text-gray-600">Markdown</p>
            </div>
            <div className="bg-gray-50 p-2 rounded text-center">
              <span className="font-medium text-indigo-600">📄 RTF</span>
              <p className="text-gray-600">Rich Text</p>
            </div>
            <div className="bg-gray-50 p-2 rounded text-center">
              <span className="font-medium text-gray-400">+ More</span>
              <p className="text-gray-600">Coming Soon</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentUpload;
