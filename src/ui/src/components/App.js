import React, { useState } from "react";
import PromptInput from "./PromptInput";
import ResponseList from "./ResponseList";
import SimilarMovies from "./SimilarMovies";

import useSubmitHandler from "../helpers/useSubmitHandler";

import "../styles/index.css";

const App = () => {   
    const [prompt, setPrompt] = useState("");
    const [loadingSimilarMovies, setLoadingSimilarMovies] = useState(false); // testing
    const { loading, responses, similarMovies, handleSubmit } = useSubmitHandler();

    const handleSubmitWrapper = async () => {
        const currentPrompt = prompt;
        setPrompt("");
        await handleSubmit(currentPrompt);
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
