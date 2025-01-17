import React, { useState } from "react";
import { sendPrompt, fetchSimilarMovies } from "./api";

const App = () => {
    const [prompt, setPrompt] = useState("");
    const [responses, setResponses] = useState([]);
    const [loading, setLoading] = useState(false);
    const [similarMovies, setSimilarMovies] = useState([]);

    const handleSubmit = async () => {
        if (!prompt) return;
        setLoading(true);

        const currentPrompt = prompt;
        setPrompt("");
        setSimilarMovies([]);

        let currentResponse = "";
        let buffer = "";

        setResponses((prev) => [
            ...prev,
            { prompt: currentPrompt, response: "" }
        ]);

        try {
            await sendPrompt(currentPrompt, (chunk) => {
                buffer += chunk;
                let lines = buffer.split("\n");
                buffer = lines.pop();
                for (let line of lines) {
                    if (!line.trim()) continue;
                    try {
                        const parsed = JSON.parse(line);
                        if (parsed.response) {
                            currentResponse += parsed.response;
                            setResponses((prev) => {
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
            const similarityData = await fetchSimilarMovies(currentResponse, 5);
            console.log(similarityData.results)
            setSimilarMovies(similarityData.results || []);
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred. Check the console for details.");
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
                        <p>
                            <strong>Prompt:</strong> {entry.prompt}
                        </p>
                        <div style={{ whiteSpace: "pre-wrap" }}>
                            <strong>Response:</strong> {entry.response}
                        </div>
                    </div>
                ))}
            </div>
            <div>
                <h2>Similar Movies</h2>
                {similarMovies.length === 0 ? (
                    <p>No similar movies found yet.</p>
                ) : (
                    similarMovies.map((movie, idx) => (
                        <div
                            key={idx}
                            style={{
                                marginBottom: "20px",
                                padding: "10px",
                                border: "1px solid #ccc",
                                borderRadius: "4px",
                            }}
                        >
                            <h3>{movie.title}</h3>
                            <p>
                                <strong>Release Date:</strong> {movie.release_year}
                            </p>
                            <p>
                                <strong>Plot Summary:</strong> {movie.plot}
                            </p>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default App;
