import React, { useState } from "react";
import TopBilling from "./TopBilling"
import PromptInput from "./PromptInput";
import ResponseList from "./ResponseList";
import SimilarMovies from "./SimilarMovies";
import EllipsisLoader from "./EllipsisLoader"

import useSubmitHandler from "../helpers/useSubmitHandler";
import "../styles/terminal.css";

const App = () => {   
    const [prompt, setPrompt] = useState("");
    const {
        loading,
        loadingSimilar,
        similarMovies,
        handleSubmit,
        handleSimilarMovies
    } = useSubmitHandler();

    const handleSubmitWrapper = async () => {
        await handleSubmit(prompt, setPrompt);
        console.log('similarMovies', similarMovies)
    };

    return (
        <div className="terminal">
            <TopBilling />
            <PromptInput
                prompt={prompt}
                setPrompt={setPrompt}
                handleSubmit={handleSubmitWrapper}
                handleSimilarMovies={handleSimilarMovies} 
                loading={loading}
                similarMovies={similarMovies}
                loadingSimilar={loadingSimilar}
            />
            <SimilarMovies similarMovies={similarMovies} />  
        </div>
    );

};

export default App;
