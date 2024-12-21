import React, { useState } from "react";
import axios from "axios";
import "./ResetPassword.css";

const ResetPassword = () => {
    const [email, setEmail] = useState("");
    const [newPassword, setNewPassword] = useState("");

    const handleResetPassword = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://127.0.0.1:5000/users/reset-password", {
                email,
                new_password: newPassword,
            });
            alert(response.data.message);
            window.location.href = "/login";
        } catch (error) {
            alert("Error: " + (error.response?.data?.error || "Password reset failed"));
        }
    };

    return (
        <div className="reset-password-page">
            <div className="reset-password-card">
                <h1 className="reset-password-title">Reset Password</h1>
                <form className="reset-password-form" onSubmit={handleResetPassword}>
                    <input
                        type="email"
                        placeholder="Enter your email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Enter new password"
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                        required
                    />
                    <button type="submit" className="reset-password-btn">Reset Password</button>
                </form>
            </div>
        </div>
    );
};

export default ResetPassword;
