import React, { useState } from "react";
import { sendPrompt } from "./api";

const App = () => {
  const [prompt, setPrompt] = useState(""); // Stores user input
  const [responses, setResponses] = useState([]); // Stores API responses
  const [loading, setLoading] = useState(false); // Indicates API request in progress

  const handleSubmit = async () => {
    if (!prompt) return;
    setLoading(true);

    try {
      const response = await sendPrompt(prompt); // Call API
      setResponses((prev) => [...prev, { prompt, response }]); // Update responses
      setPrompt(""); // Clear the input
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
        <h2>terd!</h2>
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
            <p><strong>Response:</strong> {entry.response}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
