import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./Login.css";

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://127.0.0.1:5000/users/login", { email, password });
            console.log("Login response:", response.data); 
    
            const { user } = response.data;
            localStorage.setItem("user_info", JSON.stringify(user));
            setMessage("Login successful!");
            navigate("/user");
        } catch (error) {
            setMessage(error.response?.data?.error || "Login failed");
        }
    };
    

    return (
        <div className="login-page">
            <div className="login-card">
                <h1 className="login-title">Welcome Back</h1>
                <form onSubmit={handleLogin}>
                    <input
                        type="email"
                        placeholder="Email"
                        className="login-input"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        className="login-input"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <button type="submit" className="login-btn">Log In</button>
                </form>
                {message && <p className="message">{message}</p>}
            </div>
        </div>
    );
};

export default Login;
