import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./User.css";

const User = () => {
    const [userData, setUserData] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const storedUser = localStorage.getItem("user_info");
        if (storedUser) {
            const user = JSON.parse(storedUser);
            setUserData(user);
        } else {
            navigate("/login");
        }
    }, [navigate]);

    return userData ? (
        <div className="user-container">
            <h2>Welcome, {userData.FirstName} {userData.LastName}</h2>
            <div className="user-details">
                <p><strong>Email:</strong> {userData.Email}</p>
            </div>
        </div>
    ) : null;
};

export default User;
