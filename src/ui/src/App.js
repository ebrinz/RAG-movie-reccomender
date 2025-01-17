import React, { useState } from "react";
import { sendPrompt } from "./api";

const App = () => {
    const [prompt, setPrompt] = useState("");
    const [responses, setResponses] = useState([]);
    const [loading, setLoading] = useState(false);
  
    const handleSubmit = async () => {
      if (!prompt) return;
      setLoading(true);
  
      const currentPrompt = prompt;
      setPrompt(""); // Clear input field
  
      let currentResponse = "";
      let buffer = "";  // Buffer to accumulate partial data
  
      // Add a placeholder for the new response
      setResponses(prev => [...prev, { prompt: currentPrompt, response: "" }]);
  
      try {
        await sendPrompt(currentPrompt, (chunk) => {
          // Append the new chunk to the buffer
          buffer += chunk;
  
          // Split the buffer by newline characters
          let lines = buffer.split("\n");
          // Keep the last partial line in the buffer
          buffer = lines.pop();
  
          // Process each complete line
          for (let line of lines) {
            if (!line.trim()) continue;  // Skip empty lines
            try {
              const parsed = JSON.parse(line);
              // Extract only the "response" field
              if (parsed.response) {
                currentResponse += parsed.response;
  
                // Update the last response entry reactively
                setResponses(prev => {
                  const updatedResponses = [...prev];
                  updatedResponses[updatedResponses.length - 1] = {
                    prompt: currentPrompt,
                    response: currentResponse
                  };
                  return updatedResponses;
                });
              }
            } catch (e) {
              console.error("JSON parse error:", e, "Line:", line);
            }
          }
        });
      } catch (error) {
        console.error("Error fetching RAG response:", error);
        alert("Failed to fetch response. Check the console for details.");
      } finally {
        setLoading(false);
      }
    };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>RAG Prompt UI</h1>
      <div style={{ marginBottom: "20px" }}>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Type your prompt here..."
          rows="5"
          style={{ width: "100%", padding: "10px", fontSize: "16px" }}
        />
        <button
          onClick={handleSubmit}
          disabled={loading}
          style={{
            marginTop: "10px",
            padding: "10px 20px",
            fontSize: "16px",
            cursor: "pointer",
            background: loading ? "#ddd" : "#007BFF",
            color: "#fff",
            border: "none",
            borderRadius: "4px",
          }}
        >
          {loading ? "Submitting..." : "Submit"}
        </button>
      </div>
      <div>
        <h2>Responses</h2>
        {responses.length === 0 && <p>No responses yet.</p>}
        {responses.map((entry, index) => (
          <div
            key={index}
            style={{
              marginBottom: "20px",
              padding: "10px",
              border: "1px solid #ddd",
              borderRadius: "4px",
            }}
          >
            <p><strong>Prompt:</strong> {entry.prompt}</p>
            <div style={{ whiteSpace: 'pre-wrap' }}>
              <strong>Response:</strong> {entry.response}
            </div>

          </div>
        ))}
      </div>
    </div>
  );
};

export default App;

