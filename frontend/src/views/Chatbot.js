import React, { useState, useContext } from 'react';
import './style/Chatbot.css';
import useAxios from '../utils/useAxios';
import AuthContext from '../context/AuthContext';

const Chatbot = () => {
    const { authTokens } = useContext(AuthContext);
    const api = useAxios();

    const [messages, setMessages] = useState([
        { type: 'bot', text: "Hi there 👋" },
        { type: 'bot', text: "I'm the Tutor AI assistant" },
        { type: 'bot', text: "How can I help you today?" }
    ]);
    const [userMessage, setUserMessage] = useState('');
    const [isVisible, setIsVisible] = useState(false);

    const [isProvidingFeedback, setIsProvidingFeedback] = useState(false);
    const [selectedAgent, setSelectedAgent] = useState(null);
    const [taskType, setTaskType] = useState(null);
    const [isAskingQuestion, setIsAskingQuestion] = useState(false);

    const lessonId = localStorage.getItem('lessonId');  // Retrieve the lessonId from local storage

    const handleSendMessage = async () => {
        if (userMessage.trim() !== '') {
            setMessages([...messages, { type: 'user', text: userMessage }]);
            setUserMessage('');

            setMessages(prevMessages => [...prevMessages, { type: 'bot', text: "Thank you for your feedback! Your request has been considered." }]);

            try {
                let response;
                if (isProvidingFeedback) {
                    const quizResults = await api.get('/fetch-quiz-results/');
                    response = await api.post('/chatbot-response/', {
                        message: userMessage,
                        lesson_id: lessonId,
                        agent_key: selectedAgent,
                        task_type: taskType,
                        quiz_results: quizResults.data  // Pass quiz results to the backend
                    });
                    
                    // Conditionally hide the agent's answer
                    if (!(selectedAgent === 'practical_tutor' && taskType === 'create_exercise') && !(selectedAgent === 'learning_path_tutor')) {
                        setMessages(prevMessages => [...prevMessages, { type: 'bot', text: response.data.response }]);
                    }
                } else {
                    response = await api.post('/chatbot-response/', {
                        message: userMessage,
                        lesson_id: lessonId,
                    });
                    setMessages(prevMessages => [...prevMessages, { type: 'bot', text: response.data.response }]);
                }
            } catch (error) {
                console.error("Error sending message to chatbot:", error.response.data);
            }
        }
    };

    const handleNewChat = () => {
        setMessages([
            { type: 'bot', text: "Hi there 👋" },
            { type: 'bot', text: "I'm the Tutor AI assistant" },
            { type: 'bot', text: "How can I help you today?" }
        ]);
        setIsProvidingFeedback(false);
        setSelectedAgent(null);
        setTaskType(null);
        setIsAskingQuestion(false);
    };

    const startProvidingFeedback = () => {
        setIsProvidingFeedback(true);
        setIsAskingQuestion(false);
    };

    const selectAgent = (agent) => {
        setSelectedAgent(agent);
    };

    const selectTaskType = (task) => {
        setTaskType(task);
    };

    const startAskingQuestion = () => {
        setIsAskingQuestion(true);
        setIsProvidingFeedback(false);
    };

    return (
        <div>
            <div className="chatbot-container" id="chatbotContainer" style={{ display: isVisible ? 'flex' : 'none' }}>
                <div className="chatbot-header">
                    <h2>Chat with Tutor AI</h2>
                    <button id="newChat" onClick={handleNewChat}>New chat</button>
                </div>
                <div className="chat-window">
                    {messages.map((message, index) => (
                        <div key={index} className={`message ${message.type}-message`}>
                            <p>{message.text}</p>
                        </div>
                    ))}
                </div>
                <div className="chat-input">
                    {!isProvidingFeedback && !isAskingQuestion && (
                        <>
                            <button onClick={startAskingQuestion}>Ask a Question</button>
                            <button onClick={startProvidingFeedback}>Provide Feedback</button>
                        </>
                    )}
                    {isProvidingFeedback && !selectedAgent && (
                        <>
                            <p>Please select the option you want to proceed with:</p>
                            <button onClick={() => selectAgent('practical_tutor')}>Quiz</button>
                            <button onClick={() => selectAgent('learning_path_tutor')}>Course</button>
                            {/* Add more agents as needed */}
                        </>
                    )}
                    {isProvidingFeedback && selectedAgent === 'practical_tutor' && !taskType && (
                        <>
                            <p>Please select an action:</p>
                            <button onClick={() => selectTaskType('create_exercise')}>Edit Quiz</button>
                            <button onClick={() => selectTaskType('correct_exercise')}>Get Feedback</button>
                        </>
                    )}
                    {(isAskingQuestion || (isProvidingFeedback && selectedAgent && (selectedAgent !== 'practical_tutor' || taskType))) && (
                        <>
                            <input
                                type="text"
                                id="userMessage"
                                value={userMessage}
                                onChange={(e) => setUserMessage(e.target.value)}
                                placeholder="Type your message here..."
                            />
                            <button id="sendMessage" onClick={handleSendMessage}>Send</button>
                        </>
                    )}
                </div>
            </div>
            <button id="chatbotButton" className="chatbot-button" onClick={() => setIsVisible(!isVisible)}>🤖</button>
        </div>
    );
};

export default Chatbot;
