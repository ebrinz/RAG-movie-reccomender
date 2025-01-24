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
    const [
        loadingSimilarMovies, 
        setLoadingSimilarMovies
    ] = useState(false); // testing
    const {
        loading,
        similarMovies,
        handleSubmit
    } = useSubmitHandler();

    const handleSubmitWrapper = async () => {
        await handleSubmit(prompt, setPrompt);
        console.log('similarMovies', similarMovies)
    };

    return (
        <div className="terminal">
            {/* <TopBilling /> */}
            <PromptInput
                prompt={prompt}
                setPrompt={setPrompt}
                handleSubmit={handleSubmitWrapper}
                loading={loading}
            />
            <div>
                {loadingSimilarMovies ? 
                (
                    <EllipsisLoader />
                ) : (
                    <SimilarMovies similarMovies={similarMovies} />
                )}
            </div>
            <SimilarMovies similarMovies={similarMovies} />  
        </div>
    );

};

export default App;
