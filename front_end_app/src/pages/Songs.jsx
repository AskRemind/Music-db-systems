import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Songs.css";

const Songs = () => {
    const [songs, setSongs] = useState([]);
    const [message, setMessage] = useState("");

    useEffect(() => {
        const fetchDailyRecommendation = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/songs/daily-recommendation");
                setSongs(response.data);
            } catch (error) {
                console.error("Error fetching daily recommendation:", error);
                setMessage("Failed to fetch daily recommendations.");
            }
        };

        fetchDailyRecommendation();
    }, []);

    return (
        <div className="songs-page">
            <h1>Daily Recommendation</h1>
            <div className="songs-container">
                {songs.map((song) => (
                    <div key={song.song_id} className="song-card">
                        <h2>{song.title}</h2>
                        <p>Artist: {song.artist_name}</p>
                    </div>
                ))}
            </div>
            {message && <p className="message">{message}</p>}
        </div>
    );
};

export default Songs;

