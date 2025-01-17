import React, { useState } from "react";
import { sendPrompt, fetchSimilarMovies } from "./api";
import PromptInput from "./PromptInput";
import ResponseList from "./ResponseList";
import SimilarMovies from "./SimilarMovies";

import "./index.css";

const App = () => {
    const [prompt, setPrompt] = useState("");
    const [responses, setResponses] = useState([]);
    const [loading, setLoading] = useState(false);
    const [similarMovies, setSimilarMovies] = useState([]);

    const [loadingSimilarMovies, setLoadingSimilarMovies] = useState(false); // testing

    const handleSubmit = async () => {
        if (!prompt) return;
        setLoading(true);
        setLoadingSimilarMovies(false);

        const currentPrompt = prompt;
        setPrompt("");
        setSimilarMovies([]);

        let currentResponse = "";
        let buffer = "";

        // setResponses((prev) => [
        //     ...prev,
        //     { prompt: currentPrompt, response: "" }
        // ]);
        setResponses(() => [
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

            setLoadingSimilarMovies(true);

            const similarityData = await fetchSimilarMovies(currentResponse, 5);
            console.log(similarityData.results)
            setSimilarMovies(similarityData.results || []);

            setLoadingSimilarMovies(false);

        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred. Check the console for details.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
            <h1>Movie Recco</h1>
            <PromptInput
                prompt={prompt}
                setPrompt={setPrompt}
                handleSubmit={handleSubmit}
                loading={loading}
            />
            <ResponseList responses={responses} />
            
            <div>
                {loadingSimilarMovies ? (
                    <div className="spinner"></div>
                ) : (
                    <SimilarMovies similarMovies={similarMovies} />
                )}
            </div>
        </div>
    );

};

export default App;
