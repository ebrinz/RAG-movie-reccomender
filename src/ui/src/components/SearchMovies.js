import React, { useState, useEffect } from 'react';
import { fetchMoviesWithPagination } from '../api/api';
import '../styles/SearchMovies.css';

const SearchMovies = ({ onMovieSelect, placeholder = "Search movies..." }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [showResults, setShowResults] = useState(false);
  const [totalCount, setTotalCount] = useState(0);
  
  const resultsPerPage = 5;

  useEffect(() => {
    const getMovies = async () => {
      if (query.length < 2) {
        setResults([]);
        setTotalCount(0);
        return;
      }
      
      setLoading(true);
      try {
        const offset = (currentPage - 1) * resultsPerPage;
        const response = await fetchMoviesWithPagination({
          limit: resultsPerPage,
          offset: offset,
          title: query
        });
        
        setResults(response.results.movies || []);
        setTotalCount(response.results.total_count || 0);
      } catch (error) {
        console.error('Search error:', error);
        setResults([]);
        setTotalCount(0);
      } finally {
        setLoading(false);
      }
    };

    const debounce = setTimeout(getMovies, 300);
    return () => clearTimeout(debounce);
  }, [query, currentPage]);

  const totalPages = Math.ceil(totalCount / resultsPerPage);

  const handleItemClick = (movie) => {
    onMovieSelect(movie);
    setQuery('');
    setShowResults(false);
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (!event.target.closest('.search-container')) {
        setShowResults(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="search-container">
      <div className="terminal-container">
        <div className="search-box">
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setCurrentPage(1);
              setShowResults(true);
            }}
            onFocus={() => setShowResults(true)}
            className="search-input terminal-textarea"
            placeholder={placeholder}
          />
        </div>

        {showResults && (query.length >= 2) && (loading || results.length > 0) && (
          <div className="search-results">
            {loading ? (
              <div className="search-loading">
                Searching<span className="blinking-cursor" />
              </div>
            ) : (
              <>
                <div className="results-table-container">
                  <table className="results-table">
                    <thead className="results-header">
                      <tr className="results-header-row">
                        <th className="results-header-cell w-1/2">Title</th>
                        <th className="results-header-cell w-1/4">Year</th>
                        <th className="results-header-cell w-1/4">Director</th>
                      </tr>
                    </thead>
                    <tbody>
                      {results.map((movie) => (
                        <tr
                          key={movie.id}
                          onClick={() => handleItemClick(movie)}
                          className="results-row"
                        >
                          <td className="results-cell results-cell-title">{movie.title}</td>
                          <td className="results-cell">{movie.release_year}</td>
                          <td className="results-cell">{movie.director}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {results.length === 0 && (
                  <div className="no-results">
                    No movies found
                  </div>
                )}
                
                {totalPages > 1 && (
                    <div className="pagination">
                        <div className="pagination-controls">
                        <button
                            onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                            disabled={currentPage === 1}
                            className="terminal-button pagination-button"
                        >
                            Prev
                        </button>
                        </div>
                        <span className="pagination-text">
                        Page {currentPage} of {totalPages}
                        </span>
                        <div className="pagination-controls">
                        <button
                            onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                            disabled={currentPage === totalPages}
                            className="terminal-button pagination-button"
                        >
                            Next
                        </button>
                        </div>
                    </div>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchMovies;