import { useState } from "react";
import { sendPrompt, 
    fetchSimilarMovies, 
    fetchSimilarMoviesEnhanced, 
    fetchMoviesWithPagination,
    performHybridSearch
 } from "../api/api";

const useSubmitHandler = () => {
    const [loading, setLoading] = useState(false);
    const [responses, setResponses] = useState([]);
    const [similarMovies, setSimilarMovies] = useState([]);

    // const [loadingSimilarMovies, setLoadingSimilarMovies] = useState(false); // testing


    const handleSubmit = async (prompt, setPrompt) => {
        if (!prompt) return;
        setLoading(true);
        setSimilarMovies([]);

        console.log('prompt', prompt)
        console.log('setPrompt', setPrompt)
    
        let currentResponse = "";
        let buffer = "";
    
        setResponses(prev => [...prev, { prompt, response: "" }]);
    
        try {
          // 2. This function streams the response from the server
          await sendPrompt(prompt, (chunk) => {
            buffer += chunk;
            let lines = buffer.split("\n");
            buffer = lines.pop();
            for (let line of lines) {
              if (!line.trim()) continue;
              try {
                const parsed = JSON.parse(line);
                if (parsed.message) {
                  currentResponse += parsed.message.content;
                  
                  // 3. Update the parent's prompt with the streaming text
                  //    so <textarea> displays the output in real time
                  if (setPrompt) {
                    setPrompt(currentResponse);
                  }
    
                  setResponses((prev) => {
                    const updatedResponses = [...prev];
                    updatedResponses[updatedResponses.length - 1] = {
                      prompt: prompt,
                      response: currentResponse,
                    };
                    return updatedResponses;
                  });
                }
              } catch (e) {
                console.error("JSON parse error:", e, "Line:", line);
              }
            }
          });
    
          const similarityData = await fetchSimilarMoviesEnhanced({ text: currentResponse, num_neighbors: 15, metric: 'cosine' });
          setSimilarMovies(similarityData.results || []);

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