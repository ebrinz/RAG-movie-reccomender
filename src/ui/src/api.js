export const sendPrompt = async (prompt) => {
    try {
      const response = await fetch("http://localhost:5000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: prompt || "What is the capital of France?",
          num_ctx: 2048,
        }),
      });
  
      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }
  
      // Process the streaming response
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let result = '';
      let done = false;
  
      while (!done) {
        const { value, done: streamDone } = await reader.read();
        done = streamDone;
        if (value) {
          // Decode the current chunk and append it to result
          result += decoder.decode(value, { stream: true });
          // Optionally: process partial data here (e.g., update UI)
          console.log("Received chunk:", result);
        }
      }
      // At this point, `result` should contain the entire response from the stream
      console.log("Final result:", result);
  
      // Attempt to parse the complete result as JSON if it's valid
      let data;
      try {
        data = JSON.parse(result);
      } catch (jsonError) {
        console.error("Failed to parse final JSON:", jsonError);
        data = { response: result }; // fallback handling if needed
      }
  
      return data.response || "No response received.";
    } catch (error) {
      console.error("Error:", error);
      throw error;
    }
  };
  
  
  