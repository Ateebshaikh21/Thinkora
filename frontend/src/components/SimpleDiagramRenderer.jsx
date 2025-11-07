import React from "react";

const SimpleDiagramRenderer = ({ diagram, className = "" }) => {
  const renderSVGDiagram = () => {
    if (!diagram.svg_config) return null;

    const config = diagram.svg_config;

    return (
      <svg
        width={config.width || 400}
        height={config.height || 300}
        className="border rounded bg-white"
        viewBox={`0 0 ${config.width || 400} ${config.height || 300}`}
      >
        {config.elements &&
          config.elements.map((element, index) => {
            if (element.type === "rect") {
              return (
                <rect
                  key={index}
                  x={element.x}
                  y={element.y}
                  width={element.width}
                  height={element.height}
                  fill={element.fill || "#3b82f6"}
                  stroke={element.stroke || "#1e40af"}
                  strokeWidth={element.strokeWidth || 2}
                  rx={element.rx || 0}
                />
              );
            } else if (element.type === "circle") {
              return (
                <circle
                  key={index}
                  cx={element.cx}
                  cy={element.cy}
                  r={element.r}
                  fill={element.fill || "#10b981"}
                  stroke={element.stroke || "#059669"}
                  strokeWidth={element.strokeWidth || 2}
                />
              );
            } else if (element.type === "line") {
              return (
                <line
                  key={index}
                  x1={element.x1}
                  y1={element.y1}
                  x2={element.x2}
                  y2={element.y2}
                  stroke={element.stroke || "#6b7280"}
                  strokeWidth={element.strokeWidth || 2}
                  markerEnd={element.arrow ? "url(#arrowhead)" : ""}
                />
              );
            } else if (element.type === "text") {
              return (
                <text
                  key={index}
                  x={element.x}
                  y={element.y}
                  fill={element.fill || "#1f2937"}
                  fontSize={element.fontSize || 14}
                  textAnchor={element.textAnchor || "start"}
                  fontWeight={element.fontWeight || "normal"}
                >
                  {element.text}
                </text>
              );
            } else if (element.type === "path") {
              return (
                <path
                  key={index}
                  d={element.d}
                  fill={element.fill || "none"}
                  stroke={element.stroke || "#3b82f6"}
                  strokeWidth={element.strokeWidth || 2}
                />
              );
            }
            return null;
          })}

        {/* Arrow marker definition */}
        <defs>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="9"
            refY="3.5"
            orient="auto"
          >
            <polygon points="0 0, 10 3.5, 0 7" fill="#6b7280" />
          </marker>
        </defs>
      </svg>
    );
  };

  const renderMermaidDiagram = () => {
    if (!diagram.mermaid_code) return null;

    // Simple mermaid-like rendering using SVG
    return (
      <div className="bg-white p-4 rounded-lg border">
        <div className="text-center text-gray-600 mb-4">
          <strong>Flowchart Diagram</strong>
        </div>
        <div className="flex flex-col items-center space-y-4">
          <div className="bg-blue-100 border-2 border-blue-500 rounded-lg px-4 py-2 text-blue-800 font-semibold">
            Start Process
          </div>
          <div className="text-gray-400">↓</div>
          <div className="bg-yellow-100 border-2 border-yellow-500 rounded-lg px-4 py-2 text-yellow-800 font-semibold">
            Decision Point
          </div>
          <div className="flex space-x-8">
            <div className="flex flex-col items-center space-y-2">
              <div className="text-green-600">Yes →</div>
              <div className="bg-green-100 border-2 border-green-500 rounded-lg px-4 py-2 text-green-800 font-semibold">
                Execute
              </div>
            </div>
            <div className="flex flex-col items-center space-y-2">
              <div className="text-red-600">No →</div>
              <div className="bg-red-100 border-2 border-red-500 rounded-lg px-4 py-2 text-red-800 font-semibold">
                Alternative
              </div>
            </div>
          </div>
          <div className="text-gray-400">↓</div>
          <div className="bg-purple-100 border-2 border-purple-500 rounded-lg px-4 py-2 text-purple-800 font-semibold">
            End Process
          </div>
        </div>
      </div>
    );
  };

  const renderChartDiagram = () => {
    if (!diagram.chart_config) return null;

    const config = diagram.chart_config;
    const data = config.data;

    if (config.type === "bar" && data.datasets && data.datasets[0]) {
      const dataset = data.datasets[0];
      const maxValue = Math.max(...dataset.data);

      return (
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-lg font-semibold text-center mb-4">
            {config.options?.plugins?.title?.text || "Chart"}
          </h3>
          <div className="flex items-end justify-center space-x-4 h-48">
            {data.labels.map((label, index) => {
              const value = dataset.data[index];
              const height = (value / maxValue) * 150;
              const color = dataset.backgroundColor[index] || "#3b82f6";

              return (
                <div key={index} className="flex flex-col items-center">
                  <div className="text-sm font-semibold mb-1">{value}</div>
                  <div
                    className="w-12 rounded-t"
                    style={{
                      height: `${height}px`,
                      backgroundColor: color,
                      minHeight: "20px",
                    }}
                  ></div>
                  <div className="text-xs mt-2 text-center">{label}</div>
                </div>
              );
            })}
          </div>
        </div>
      );
    }

    return (
      <div className="bg-white p-4 rounded-lg border text-center">
        <div className="text-gray-600">Chart visualization</div>
      </div>
    );
  };

  return (
    <div className={`diagram-container ${className}`}>
      <div className="mb-3">
        <h5 className="font-bold text-gray-900 text-lg flex items-center">
          <span className="bg-purple-100 text-purple-800 px-2 py-1 rounded text-sm mr-2 uppercase font-semibold">
            {diagram.diagram_type}
          </span>
          {diagram.title}
        </h5>
        <p className="text-gray-600 text-sm mt-1">{diagram.description}</p>
      </div>

      <div className="diagram-content">
        {diagram.diagram_type === "mermaid" && renderMermaidDiagram()}
        {diagram.diagram_type === "chart" && renderChartDiagram()}
        {diagram.diagram_type === "svg" && renderSVGDiagram()}

        {!["mermaid", "chart", "svg"].includes(diagram.diagram_type) && (
          <div className="bg-gradient-to-br from-blue-50 to-purple-50 p-8 rounded-lg border-2 border-dashed border-blue-300 text-center">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              {diagram.title}
            </h3>
            <p className="text-gray-600">{diagram.description}</p>
            <div className="mt-4 text-sm text-blue-600">
              Interactive {diagram.diagram_type} diagram
            </div>
          </div>
        )}
      </div>

      <div className="mt-3 flex items-center justify-between">
        <div className="text-xs text-gray-500">
          💡 Visual learning aid for better understanding
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => {
              let textToCopy = "";
              if (diagram.mermaid_code) {
                textToCopy = diagram.mermaid_code;
              } else if (diagram.chart_config) {
                textToCopy = JSON.stringify(diagram.chart_config, null, 2);
              } else if (diagram.svg_config) {
                textToCopy = JSON.stringify(diagram.svg_config, null, 2);
              }

              if (textToCopy) {
                navigator.clipboard
                  .writeText(textToCopy)
                  .then(() => {
                    if (window.showNotification) {
                      window.showNotification(
                        "Diagram code copied!",
                        "success"
                      );
                    }
                  })
                  .catch(() => {
                    if (window.showNotification) {
                      window.showNotification("Failed to copy", "error");
                    }
                  });
              }
            }}
            className="bg-blue-500 hover:bg-blue-600 text-white text-xs px-3 py-1 rounded transition-colors"
          >
            📋 Copy
          </button>
        </div>
      </div>
    </div>
  );
};

export default SimpleDiagramRenderer;
