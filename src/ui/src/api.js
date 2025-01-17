
export const sendPrompt = async (prompt, onChunk) => {
    try {
        const response = await fetch("http://localhost:5000/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                prompt: prompt,
                num_ctx: 2048,
            }),
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let done = false;
        let fullResponse = "";

        while (!done) {
            const { value, done: streamDone } = await reader.read();
            done = streamDone;
            if (value) {
                const chunk = decoder.decode(value, { stream: true });
                console.log("Received chunk:", chunk);
                fullResponse += chunk;  // Simply accumulate chunk
                if (onChunk) {
                    onChunk(chunk);
                }
            }
        }
        return fullResponse;
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
};

export const fetchSimilarMovies = async (text, num_neighbors = 5) => {
    try {
        const vectorResponse = await fetch("http://localhost:5000/vector_search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text,
                num_neighbors,
            }),
        });
        if (!vectorResponse.ok) {
            throw new Error(`Vector search API error: ${vectorResponse.statusText}`);
        }
        return await vectorResponse.json();
    } catch (error) {
        console.error("Error in fetchSimilarMovies:", error);
        throw error;
    }
};

  
  