import React, { useEffect, useRef, useState } from "react";
import mermaid from "mermaid";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  LineElement,
  PointElement,
} from "chart.js";
import { Bar, Pie, Line } from "react-chartjs-2";
import * as d3 from "d3";

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  LineElement,
  PointElement
);

// Initialize Mermaid
mermaid.initialize({
  startOnLoad: true,
  theme: "default",
  securityLevel: "loose",
  fontFamily: "Arial, sans-serif",
  fontSize: 14,
  flowchart: {
    useMaxWidth: true,
    htmlLabels: true,
    curve: "basis",
  },
});

const DiagramRenderer = ({ diagram, className = "" }) => {
  const mermaidRef = useRef(null);
  const svgRef = useRef(null);
  const [mermaidSvg, setMermaidSvg] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (diagram.diagram_type === "mermaid" && diagram.mermaid_code) {
      renderMermaidDiagram();
    } else if (diagram.diagram_type === "d3" && diagram.d3_config) {
      renderD3Diagram();
    }
  }, [diagram]);

  const renderMermaidDiagram = async () => {
    try {
      const { svg } = await mermaid.render(
        "mermaid-diagram-" + Date.now(),
        diagram.mermaid_code
      );
      setMermaidSvg(svg);
      setError("");
    } catch (err) {
      console.error("Mermaid rendering error:", err);
      setError("Failed to render diagram");
    }
  };

  const renderD3Diagram = () => {
    if (!svgRef.current || !diagram.d3_config) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove(); // Clear previous content

    const config = diagram.d3_config;
    const width = config.width || 400;
    const height = config.height || 300;

    svg.attr("width", width).attr("height", height);

    if (config.type === "tree") {
      renderD3Tree(svg, config, width, height);
    } else if (config.type === "network") {
      renderD3Network(svg, config, width, height);
    } else if (config.type === "hierarchy") {
      renderD3Hierarchy(svg, config, width, height);
    }
  };

  const renderD3Tree = (svg, config, width, height) => {
    const data = config.data;
    const root = d3.hierarchy(data);
    const treeLayout = d3.tree().size([width - 100, height - 100]);
    treeLayout(root);

    // Links
    svg
      .selectAll(".link")
      .data(root.links())
      .enter()
      .append("path")
      .attr("class", "link")
      .attr(
        "d",
        d3
          .linkVertical()
          .x((d) => d.x + 50)
          .y((d) => d.y + 50)
      )
      .attr("fill", "none")
      .attr("stroke", "#3b82f6")
      .attr("stroke-width", 2);

    // Nodes
    const nodes = svg
      .selectAll(".node")
      .data(root.descendants())
      .enter()
      .append("g")
      .attr("class", "node")
      .attr("transform", (d) => `translate(${d.x + 50}, ${d.y + 50})`);

    nodes
      .append("circle")
      .attr("r", 20)
      .attr("fill", "#3b82f6")
      .attr("stroke", "#1e40af")
      .attr("stroke-width", 2);

    nodes
      .append("text")
      .attr("dy", 5)
      .attr("text-anchor", "middle")
      .attr("fill", "white")
      .attr("font-size", "12px")
      .text((d) => d.data.name);
  };

  const renderD3Network = (svg, config, width, height) => {
    const { nodes, links } = config.data;

    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(links)
          .id((d) => d.id)
          .distance(100)
      )
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));

    // Links
    const link = svg
      .selectAll(".link")
      .data(links)
      .enter()
      .append("line")
      .attr("class", "link")
      .attr("stroke", "#6b7280")
      .attr("stroke-width", 2);

    // Nodes
    const node = svg
      .selectAll(".node")
      .data(nodes)
      .enter()
      .append("g")
      .attr("class", "node");

    node
      .append("circle")
      .attr("r", 15)
      .attr("fill", "#10b981")
      .attr("stroke", "#059669")
      .attr("stroke-width", 2);

    node
      .append("text")
      .attr("dy", 5)
      .attr("text-anchor", "middle")
      .attr("fill", "white")
      .attr("font-size", "10px")
      .text((d) => d.name);

    simulation.on("tick", () => {
      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      node.attr("transform", (d) => `translate(${d.x}, ${d.y})`);
    });
  };

  const renderD3Hierarchy = (svg, config, width, height) => {
    const data = config.data;
    const root = d3.hierarchy(data);
    const partition = d3.partition().size([width, height]);
    partition(root);

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    svg
      .selectAll("rect")
      .data(root.descendants())
      .enter()
      .append("rect")
      .attr("x", (d) => d.x0)
      .attr("y", (d) => d.y0)
      .attr("width", (d) => d.x1 - d.x0)
      .attr("height", (d) => d.y1 - d.y0)
      .attr("fill", (d, i) => color(i))
      .attr("stroke", "white")
      .attr("stroke-width", 1);

    svg
      .selectAll("text")
      .data(root.descendants().filter((d) => d.x1 - d.x0 > 50))
      .enter()
      .append("text")
      .attr("x", (d) => (d.x0 + d.x1) / 2)
      .attr("y", (d) => (d.y0 + d.y1) / 2)
      .attr("text-anchor", "middle")
      .attr("dy", 5)
      .attr("font-size", "12px")
      .attr("fill", "white")
      .text((d) => d.data.name);
  };

  const renderChartJSDiagram = () => {
    const config = diagram.chart_config;

    if (config.type === "bar") {
      return <Bar data={config.data} options={config.options} />;
    } else if (config.type === "pie") {
      return <Pie data={config.data} options={config.options} />;
    } else if (config.type === "line") {
      return <Line data={config.data} options={config.options} />;
    }
    return null;
  };

  const renderSVGDiagram = () => {
    const config = diagram.svg_config;

    return (
      <svg
        width={config.width || 400}
        height={config.height || 300}
        className="border rounded"
      >
        {config.elements.map((element, index) => {
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

      <div className="diagram-content bg-white p-4 rounded-lg border shadow-sm">
        {error && (
          <div className="text-red-600 text-sm mb-2">Error: {error}</div>
        )}

        {diagram.diagram_type === "mermaid" && (
          <div
            ref={mermaidRef}
            dangerouslySetInnerHTML={{ __html: mermaidSvg }}
            className="mermaid-diagram"
          />
        )}

        {diagram.diagram_type === "d3" && (
          <svg ref={svgRef} className="d3-diagram"></svg>
        )}

        {diagram.diagram_type === "chart" && renderChartJSDiagram()}

        {diagram.diagram_type === "svg" && renderSVGDiagram()}

        {diagram.diagram_type === "css" && (
          <div
            className="css-diagram"
            dangerouslySetInnerHTML={{ __html: diagram.html_content }}
          />
        )}
      </div>

      <div className="mt-3 flex items-center justify-between">
        <div className="text-xs text-gray-500">
          💡 Interactive diagram - hover and click to explore
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
              } else if (diagram.d3_config) {
                textToCopy = JSON.stringify(diagram.d3_config, null, 2);
              } else if (diagram.html_content) {
                textToCopy = diagram.html_content;
              }

              navigator.clipboard
                .writeText(textToCopy)
                .then(() => {
                  if (window.showNotification) {
                    window.showNotification(
                      "Diagram code copied to clipboard!",
                      "success"
                    );
                  }
                })
                .catch(() => {
                  if (window.showNotification) {
                    window.showNotification(
                      "Failed to copy diagram code",
                      "error"
                    );
                  }
                });
            }}
            className="interactive-button text-xs px-3 py-1"
          >
            📋 Copy Code
          </button>
          <button
            onClick={() => {
              // Export as image functionality could be added here
              if (window.showNotification) {
                window.showNotification("Export feature coming soon!", "info");
              }
            }}
            className="text-xs text-purple-600 hover:text-purple-800 font-medium px-3 py-1 border border-purple-200 rounded hover:bg-purple-50 transition-colors"
          >
            📥 Export
          </button>
        </div>
      </div>
    </div>
  );
};

export default DiagramRenderer;
