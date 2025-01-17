import React from "react";

const PromptInput = ({ prompt, setPrompt, handleSubmit, loading }) => {
    return (
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
    );
};

export default PromptInput;
