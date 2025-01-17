import React from "react";

const SimilarMovies = ({ similarMovies }) => {
    return (
        <div>
            {/* <h2>Similar Movies</h2> */}
            {similarMovies.length === 0 ? (
                ""
            ) : (
                similarMovies.map((movie, idx) => (
                    <div
                        key={idx}
                        style={{
                            marginBottom: "20px",
                            padding: "10px",
                            border: "1px solid #ccc",
                            borderRadius: "4px",
                        }}
                    >
                        <h3>{movie.title} ({movie.release_year})</h3>
                        <p>{movie.plot_summary}</p>
                    </div>
                ))
            )}
        </div>
    );
};

export default SimilarMovies;