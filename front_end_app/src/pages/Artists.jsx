import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Artists.css";

const Artists = () => {
    const [artists, setArtists] = useState([]);
    const [message, setMessage] = useState("");

    useEffect(() => {
        const fetchDailyArtistRecommendation = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/artists/daily-artist-recommendation");
                setArtists(response.data);
            } catch (error) {
                console.error("Error fetching daily artist recommendation:", error);
                setMessage("Failed to fetch daily artist recommendations.");
            }
        };

        fetchDailyArtistRecommendation();
    }, []);

    return (
        <div className="artists-page">
            <h1>Daily Artist Recommendation</h1>
            <div className="artists-container">
                {artists.map((artist) => (
                    <div key={artist.artist_id} className="artist-card">
                        <h2>{artist.name}</h2>
                    </div>
                ))}
            </div>
            {message && <p className="message">{message}</p>}
        </div>
    );
};

export default Artists;
