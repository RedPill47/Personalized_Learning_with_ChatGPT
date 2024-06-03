import React, { useState, useEffect } from 'react';
import './style/Quiz.css';
import Chatbot from './Chatbot';
import useAxios from '../utils/useAxios';
import jwtDecode from 'jwt-decode';
const swal = require('sweetalert2');

const Quiz = () => {
    const api = useAxios();
    const token = localStorage.getItem("authTokens");
    const decoded = jwtDecode(token);
    const user_id = decoded.user_id;

    const [quizData, setQuizData] = useState([]);
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [userAnswers, setUserAnswers] = useState([]);
    const [showResults, setShowResults] = useState(false);

    useEffect(() => {
        const fetchQuizData = async () => {
            try {
                const response = await api.get('/quiz-data/');
                setQuizData(response.data);
            } catch (error) {
                console.error('Error fetching quiz data:', error);
            }
        };

        fetchQuizData();
    }, [api]);

    const handleAnswer = (index) => {
        const newAnswers = [...userAnswers];
        newAnswers[currentQuestion] = index;
        setUserAnswers(newAnswers);
    };

    const handlePrevQuestion = () => {
        if (currentQuestion > 0) {
            setCurrentQuestion(currentQuestion - 1);
        }
    };

    const handleNextQuestion = () => {
        const selectedOption = document.querySelector('input[name="quiz"]:checked');
        if (selectedOption) {
            const updatedAnswers = [...userAnswers];
            updatedAnswers[currentQuestion] = parseInt(selectedOption.value);
            setUserAnswers(updatedAnswers);
    
            if (currentQuestion < quizData.length - 1) {
                setCurrentQuestion(currentQuestion + 1);
            } else {
                const correctAnswers = updatedAnswers.filter((answer, i) => answer === quizData[i].correct).length;
                const score = (correctAnswers / quizData.length) * 100;
    
                // Store quiz results
                api.post('/submit-quiz-result/', {
                    quiz_data: quizData,
                    score: score
                }).then(response => {
                    console.log('Quiz results saved successfully:', response.data);
                    setShowResults(true);
                }).catch(error => {
                    console.error('Error saving quiz results:', error);
                });
            }
        } else {
            swal.fire({
                title: "Please select an option.",
                icon: "error",
                toast: true,
                timer: 4000,
                position: 'top-right',
                timerProgressBar: false,
                showConfirmButton: true,
                showCancelButton: false,
            });
        }
    };

    const restartQuiz = () => {
        setCurrentQuestion(0);
        setUserAnswers([]);
        setShowResults(false);
    };

    if (showResults) {
        const correctAnswers = userAnswers.filter((answer, i) => answer === quizData[i].correct).length;
        return (
            <div className="container">
                <div className="main-content">
                    <div className="quiz-section">
                        <div className="quiz-container">
                            <div className="results-container">
                                <h2>Your Results</h2>
                                <p>You scored {correctAnswers} out of {quizData.length} questions.</p>
                                <ul>
                                    {quizData.map((question, i) => (
                                        <li key={i} className={userAnswers[i] === question.correct ? 'correct' : 'incorrect'}>
                                            <p>Question: {question.question}</p>
                                            <p>Your Answer: {question.options[userAnswers[i]]}</p>
                                            <p>Correct Answer: {question.options[question.correct]}</p>
                                        </li>
                                    ))}
                                </ul>
                                <button onClick={restartQuiz}>Take quiz again</button>
                            </div>
                        </div>
                    </div>
                    <Chatbot />
                </div>
            </div>
        );
    }

    return (
        <div className="container">
            <div className="main-content">
                <div className="quiz-section">
                    <div className="quiz-container">
                        <h2>Quiz</h2>
                        {quizData.length > 0 ? (
                            <>
                                <p className="question">Question: <span id="question-text">{quizData[currentQuestion].question}</span></p>
                                <form id="quizForm">
                                    {quizData[currentQuestion].options.map((option, i) => (
                                        <div key={i} className="quiz-option">
                                            <input type="radio" id={`option${i}`} name="quiz" value={i} checked={userAnswers[currentQuestion] === i} onChange={() => handleAnswer(i)} />
                                            <label htmlFor={`option${i}`}>{option}</label>
                                        </div>
                                    ))}
                                </form>
                                <div className="quiz-footer">
                                    <button type="button" id="prevQuestion" className="quiz-nav" onClick={handlePrevQuestion} disabled={currentQuestion === 0}>Previous Question</button>
                                    <button type="button" id="nextQuestion" className="quiz-nav" onClick={handleNextQuestion}>
                                        {currentQuestion === quizData.length - 1 ? 'Submit' : 'Next Question'}
                                    </button>
                                </div>
                                <p className="quiz-progress">Question <span id="current-question">{currentQuestion + 1}</span> of <span id="total-questions">{quizData.length}</span></p>
                            </>
                        ) : (
                            <p>Loading quiz...</p>
                        )}
                    </div>
                </div>
            </div>
            <Chatbot />
        </div>
    );
};

export default Quiz;