import React from "react";
import EllipsisLoader from "./EllipsisLoader"
import '../styles/EllipsisLoader.css';
import "../styles/terminal.css";

{/* <div className="blinking-cursor" style={{fontSize: '2em'}}></div> */}


const PromptInput = ({ prompt, setPrompt, handleSubmit, loading }) => {
    return (
        <div className="terminal-container">
            <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Type your prompt here..."
                rows="5"
                className="terminal-textarea"
            />
            <div className="terminal-button" disabled={loading} onClick={handleSubmit}>
                {loading ? <EllipsisLoader /> : "Submit"}
            </div>
        </div>
    );
};

export default PromptInput;



