import React, { useEffect, useState } from "react";
import axios from "axios";

const Recommendations = () => {
    const [recommendations, setRecommendations] = useState([]);

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/recommendations/", {
                    params: { user_id: 1 }, // Replace with logged-in user ID
                });
                setRecommendations(response.data);
            } catch (error) {
                console.error("Error fetching recommendations:", error);
            }
        };
        fetchRecommendations();
    }, []);

    return (
        <div>
            <h2>Recommended Playlists</h2>
            {recommendations.length > 0 ? (
                <ul>
                    {recommendations.map((rec) => (
                        <li key={rec.PlaylistID}>
                            <h3>{rec.Title}</h3>
                            <p>{rec.Description}</p>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No recommendations available.</p>
            )}
        </div>
    );
};

export default Recommendations;
