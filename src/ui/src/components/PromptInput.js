import React from "react";
import EllipsisLoader from "./EllipsisLoader";
import SearchMovies from './SearchMovies';
import '../styles/EllipsisLoader.css';
import "../styles/terminal.css";

const PromptInput = ({ prompt, setPrompt, handleSubmit, handleSimilarMovies, handleMovieSelect, loading, loadingSimilar }) => {
  const onSubmit = () => handleSubmit(prompt, setPrompt);
  const onSimilarMovies = () => handleSimilarMovies(prompt);
  
  const onMovieSelect = (movie) => {
    const newPrompt = handleMovieSelect(movie);
    setPrompt(newPrompt);
  };

  return (
    <div className="terminal-container">
      <SearchMovies onMovieSelect={onMovieSelect} />
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Type your prompt here..."
        rows="5"
        className="terminal-textarea"
      />
      
      <div className="terminal-buttons">
        <button
          className="terminal-button"
          disabled={loading}
          onClick={onSubmit}
        >
          {loading ? <EllipsisLoader /> : "Generate Plot Summary"}
        </button>

        <button
          className="terminal-button"
          disabled={loadingSimilar}
          onClick={onSimilarMovies}
        >
          {loadingSimilar ? <EllipsisLoader /> : "Find Similar Movies"}
        </button>
      </div>
    </div>
  );
};

export default PromptInput;

