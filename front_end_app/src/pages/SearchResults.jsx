import React, { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom"; // 引入 Link
import './SearchResults.css';

const SearchResults = () => {
  const [searchParams] = useSearchParams();
  const query = searchParams.get("q");
  const [results, setResults] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:5000/songs/search?q=${query}`)
        .then((res) => {
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then((data) => setResults(data))
        .catch((err) => console.error(err));
  }, [query]);

  return (
    <div className="search-results-container">
      <h1 className="search-title">Search Results for: "{query}"</h1>
      <div className="search-results">
        {results.map((song) => (
          <div key={song.SongID} className="song-card">
            <h2>
              <Link to={`/ratings/song/${song.SongID}`}>{song.Title}</Link>
            </h2>
            <p>Genre: {song.Genre}</p>
            <p>Average Rating: {song.AverageRating || "No ratings yet"}</p>
            <audio controls src={`/path-to-song-files/${song.SongID}.mp3`}>
              Your browser does not support audio playback.
            </audio>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchResults;
