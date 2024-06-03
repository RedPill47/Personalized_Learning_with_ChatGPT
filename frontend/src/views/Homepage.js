import React from 'react';
import { Link } from 'react-router-dom';
import './style/HomePage.css';

const HomePage = () => {
    return (
        <div className="home-container">
            <div className="home-header">
                <h1>Tutor AI</h1>
                <p>Your personal AI-powered tutor</p>
            </div>
            <div className="home-content">
                <div className="home-presentation">
                    <h2>About Tutor AI</h2>
                    <p>Tutor AI helps you create quizzes from your notes effortlessly, summarize your notes, and even provide tutoring sessions through an AI-powered chatbot. Join us to enhance your learning experience!</p>
                </div>
                <div className="home-actions">
                    <Link to="/login" className="home-button">Login</Link>
                    <Link to="/register" className="home-button">Register</Link>
                </div>
            </div>
        </div>
    );
}

export default HomePage;