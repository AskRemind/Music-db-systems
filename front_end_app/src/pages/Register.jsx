import React, { useState } from "react";
import axios from "axios";
import "./Register.css"; 
import Modal from "react-modal";

Modal.setAppElement("#root");

const Register = () => {
    const [formData, setFormData] = useState({
        FirstName: "",
        LastName: "",
        Email: "",
        Age: "",
        Country: "",
        Gender: "",
        Password: "",
    });

    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [modalMessage, setModalMessage] = useState("");

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleRegister = async (e) => {
        e.preventDefault(); 
        try {
            const response = await axios.post("http://127.0.0.1:5000/users/register", {
                FirstName: formData.FirstName,
                LastName: formData.LastName,
                Email: formData.Email,
                Age: formData.Age,
                Country: formData.Country,
                Gender: formData.Gender,
                Password: formData.Password,
            });
            setModalMessage(response.data.message);
            setModalIsOpen(true);
        } catch (error) {
            setModalMessage(error.response?.data?.error || "Registration failed");
            setModalIsOpen(true);
        }
    };

    const closeModal = () => {
        setModalIsOpen(false);
    };

    return (
        <div className="register-page">
            <div className="register-card">
                <h1 className="register-title">Create an Account</h1>
                <form className="register-form" onSubmit={handleRegister}>
                    <input
                        type="text"
                        name="FirstName"
                        placeholder="First Name"
                        value={formData.FirstName}
                        onChange={handleInputChange}
                        required
                    />
                    <input
                        type="text"
                        name="LastName"
                        placeholder="Last Name"
                        value={formData.LastName}
                        onChange={handleInputChange}
                        required
                    />
                    <input
                        type="email"
                        name="Email"
                        placeholder="Email"
                        value={formData.Email}
                        onChange={handleInputChange}
                        required
                    />
                    <input
                        type="number"
                        name="Age"
                        placeholder="Age"
                        value={formData.Age}
                        onChange={handleInputChange}
                    />
                    <input
                        type="text"
                        name="Country"
                        placeholder="Country"
                        value={formData.Country}
                        onChange={handleInputChange}
                    />
                    <select
                        name="Gender"
                        value={formData.Gender}
                        onChange={handleInputChange}
                        required
                    >
                        <option value="">Select Gender</option>
                        <option value="M">Male</option>
                        <option value="F">Female</option>
                        <option value="O">Other</option>
                    </select>
                    <input
                        type="password"
                        name="Password"
                        placeholder="Password"
                        value={formData.Password}
                        onChange={handleInputChange}
                        required
                    />
                    <button type="submit" className="register-btn">Register</button>
                </form>
            </div>
            <Modal
                isOpen={modalIsOpen}
                onRequestClose={closeModal}
                contentLabel="Registration Message"
                style={{
                    content: {
                        top: "50%",
                        left: "50%",
                        right: "auto",
                        bottom: "auto",
                        marginRight: "-50%",
                        transform: "translate(-50%, -50%)",
                        backgroundColor: "#292929",
                        color: "#ffffff",
                        borderRadius: "10px",
                        padding: "20px",
                    },
                }}
            >
                <h2>Message</h2>
                <p>{modalMessage}</p>
                <button onClick={closeModal} style={{
                    backgroundColor: "#1db954",
                    color: "#ffffff",
                    border: "none",
                    padding: "10px 20px",
                    borderRadius: "5px",
                    cursor: "pointer"
                }}>
                    Close
                </button>
            </Modal>
        </div>
    );
};

export default Register;