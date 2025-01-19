import { useState } from "react";
import { sendPrompt, fetchSimilarMovies } from "../api/api";

const useSubmitHandler = () => {
    const [loading, setLoading] = useState(false);
    const [responses, setResponses] = useState([]);
    const [similarMovies, setSimilarMovies] = useState([]);

    const [loadingSimilarMovies, setLoadingSimilarMovies] = useState(false); // testing


    const handleSubmit = async (prompt) => {
        if (!prompt) return;
        setLoading(true);
        setLoadingSimilarMovies(false);

        const currentPrompt = prompt;
        console.log(currentPrompt)
        setSimilarMovies([]);

        let currentResponse = "";
        let buffer = "";

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
                        if (parsed.message) {
                            currentResponse += parsed.message.content;
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

    return {
        loading,
        responses,
        similarMovies,
        handleSubmit
    };
    
};

export default useSubmitHandler;