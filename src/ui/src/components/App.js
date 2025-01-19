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
    const [loadingSimilarMovies, setLoadingSimilarMovies] = useState(false); // testing
    const { loading, responses, similarMovies, handleSubmit } = useSubmitHandler();

    const handleSubmitWrapper = async () => {
        const currentPrompt = prompt;
        setPrompt("");
        await handleSubmit(currentPrompt);
    };

    return (
        <div className="terminal">
            <div>
                {/* animated banner here  */}
                <TopBilling />
            </div>
            <PromptInput
                prompt={prompt}
                setPrompt={setPrompt}
                handleSubmit={() => handleSubmit(prompt)}
                loading={loading}
            />
            <ResponseList responses={responses} />
            
            <div>
                {loadingSimilarMovies ? 
                (
                    <EllipsisLoader />
                ) : (
                    <SimilarMovies similarMovies={similarMovies} />
                )}
            </div>
        </div>
    );

};

export default App;
