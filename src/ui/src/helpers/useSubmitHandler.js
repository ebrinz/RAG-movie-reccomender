import { useState } from "react";
import { sendPrompt, fetchSimilarMoviesEnhanced, fetchMoviesWithPagination } from "../api/api";

const useSubmitHandler = () => {
    const [loading, setLoading] = useState(false);
    const [loadingSimilar, setLoadingSimilar] = useState(false);
    const [responses, setResponses] = useState([]);
    const [similarMovies, setSimilarMovies] = useState([]);
    const [currentResponse, setCurrentResponse] = useState("");

    const handleSubmit = async (prompt, setPrompt) => {
        if (!prompt) return;
        setLoading(true);
        // setSimilarMovies([]);
        let buffer = "";
        setCurrentResponse("");
        
        setPrompt("");
        setResponses(prev => [...prev, { prompt, response: "" }]);
    
        try {
            await sendPrompt(prompt, (chunk) => {
                buffer += chunk;
                let lines = buffer.split("\n");
                buffer = lines.pop();
                
                for (let line of lines) {
                    if (!line.trim()) continue;
                    try {
                        const parsed = JSON.parse(line);
                        if (parsed.message) {
                            const newContent = parsed.message.content;
                            setCurrentResponse(prev => prev + newContent);
                            setPrompt(prev => prev + newContent);
                        }
                    } catch (e) {
                        console.error("JSON parse error:", e, "Line:", line);
                    }
                }
            });
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred. Check the console for details.");
        } finally {
            setLoading(false);
        }
    };

    const handleSimilarMovies = async (prompt) => {
        if (!prompt) return;
        setLoadingSimilar(true);
        setSimilarMovies([]);
        try {
            const similarityData = await fetchSimilarMoviesEnhanced({ 
                text: prompt, 
                num_neighbors: 10, 
                metric: 'cosine' 
            });
            console.log('similarityData', similarityData)
            setSimilarMovies(similarityData.results || []);
        } catch (error) {
            console.error("Error fetching similar movies:", error);
            alert("Error fetching similar movies. Check console for details.");
        } finally {
            setLoadingSimilar(false);
        }
    };

    const handleMovieSelect = (movie) => {
        return `${movie.plot_summary}`;
    };

    return {
        loading,
        loadingSimilar,
        responses,
        similarMovies,
        handleSubmit,
        handleSimilarMovies,
        handleMovieSelect
    };
};

export default useSubmitHandler;