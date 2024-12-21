import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Subscription.css"

const Subscription = () => {
    const [plans, setPlans] = useState([]);
    const [selectedPlan, setSelectedPlan] = useState("");
    const [startDate, setStartDate] = useState("");
    const [message, setMessage] = useState("");

    useEffect(() => {
        const fetchPlans = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/subscriptions/plans");
                setPlans(response.data);
            } catch (error) {
                setMessage("Failed to load subscription plans.");
            }
        };
        fetchPlans();
    }, []);

    const handleSubscribe = async () => {
        const userInfo = JSON.parse(localStorage.getItem("user_info"));
        if (!userInfo?.UserID) {
            setMessage("Please log in.");
            return;
        }
    
        if (!selectedPlan) {
            setMessage("Please select a subscription plan.");
            return;
        }
    
        if (!startDate || !/^\d{4}-\d{2}-\d{2}$/.test(startDate)) {
            setMessage("Invalid date. Please select a valid start date.");
            return;
        }
    
        const payload = {
            user_id: userInfo.UserID,  
            plan_type: selectedPlan,
            start_date: startDate,
        };
    
        console.log("Payload being sent:", payload);
    
        try {
            const response = await axios.post(
                "http://127.0.0.1:5000/subscriptions/subscribe",
                payload,
                {
                    headers: { "Content-Type": "application/json" },
                }
            );
            setMessage(response.data.message);
        } catch (error) {
            setMessage(error.response?.data?.error || "Subscription failed");
        }
    };
    

    return (
        <div className="subscription-page">
            <h1>Choose a Subscription Plan</h1>
            <div className="plans-container">
                {plans.map((plan) => (
                    <div key={plan.PlanType} className="plan-card">
                        <h2>{plan.PlanType}</h2>
                        <p>Price: ${plan.Price.toFixed(2)}</p>
                        <button onClick={() => setSelectedPlan(plan.PlanType)}>
                            Select {plan.PlanType}
                        </button>
                    </div>
                ))}
            </div>
            {selectedPlan && (
                <div className="subscription-form">
                    <h2>Selected Plan: {selectedPlan}</h2>
                    <label>
                        Start Date:
                        <input
                            type="date"
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                        />
                    </label>
                    <button onClick={handleSubscribe}>Subscribe</button>
                </div>
            )}
            {message && <p className="message">{message}</p>}
        </div>
    );
};

export default Subscription;
