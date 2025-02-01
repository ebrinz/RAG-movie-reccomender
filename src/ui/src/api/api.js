
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
                fullResponse += chunk;
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

export const fetchSimilarMovies = async (text, num_neighbors = 10) => {
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

export const fetchMoviesWithPagination = async (params = {}) => {
    const { limit = 10, offset = 0, title = "" } = params;
    try {
        const queryParams = new URLSearchParams({
            limit: limit.toString(),
            offset: offset.toString(),
            ...(title && { title })
        }).toString();
        const response = await fetch(`http://localhost:5000/movies?${queryParams}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });
        if (!response.ok) {
            throw new Error(`Movies API error: ${response.statusText}`);
        }

        const decoder = new TextDecoder();
        const reader = response.body.getReader();
        let buffer = '';
        let result = { movies: [], total_count: 0 };
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });
            try {
                result = JSON.parse(buffer);
                buffer = '';
            } catch {
                continue;
            }
        }
        buffer += decoder.decode();
        if (buffer) {
            try {
                result = JSON.parse(buffer);
            } catch (e) {
                console.error('Error parsing final buffer:', e);
            }
        }
        console.log('Parsed movies result:', result);
        return {
            results: result.movies || [],
            total_count: result.total_count || 0
        };
    } catch (error) {
        console.error("Error fetching movies:", error);
        throw error;
    }
};

export const fetchSimilarMoviesEnhanced = async (params = {}) => {
    const {
        text,
        num_neighbors = 15,
        metric = 'cosine',
    } = params;

    try {
        const response = await fetch("http://localhost:5000/vector_search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text,
                num_neighbors,
                metric
            }),
        });

        if (!response.ok) {
            throw new Error(`Vector search API error: ${response.statusText}`);
        }
        
        const data = await response.json();
        return {
            results: data.results,
            query: data.query,
            metric: data.metric,
            numResults: data.num_results
        };
    } catch (error) {
        console.error("Error in enhanced similar movies search:", error);
        throw error;
    }
};

export const performHybridSearch = async (params = {}) => {
    const {
        text,
        text_query = "",
        num_neighbors = 5,
        metric = 'cosine',
        use_normalized = true,
        embedding_weight = 0.7,
        min_similarity = 0.0
    } = params;

    try {
        const response = await fetch("http://localhost:5000/hybrid_search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text,
                text_query,
                num_neighbors,
                metric,
                use_normalized,
                embedding_weight,
                min_similarity
            }),
        });

        if (!response.ok) {
            throw new Error(`Hybrid search API error: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error in hybrid search:", error);
        throw error;
    }
};