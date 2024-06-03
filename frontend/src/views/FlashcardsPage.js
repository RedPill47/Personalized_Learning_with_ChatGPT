import React, { useState, useEffect } from 'react';
import Flashcards from './Flashcards';
import './style/FlashcardsPage.css';
import useAxios from '../utils/useAxios';
import Chatbot from './Chatbot';

const FlashcardsPage = () => {
    const api = useAxios();
    const [flashcardsData, setFlashcardsData] = useState([]);
    const [currentFlashcard, setCurrentFlashcard] = useState(0);
    const [isFlipped, setIsFlipped] = useState(false);

    useEffect(() => {
        const fetchFlashcardsData = async () => {
            try {
                const response = await api.get('/flashcards-data/');
                setFlashcardsData(response.data);
            } catch (error) {
                console.error('Error fetching flashcards data:', error);
            }
        };

        fetchFlashcardsData();
    }, [api]);

    const flipFlashcard = () => {
        setIsFlipped(!isFlipped);
    };

    const nextFlashcard = () => {
        if (currentFlashcard < flashcardsData.length - 1) {
            setCurrentFlashcard(currentFlashcard + 1);
            setIsFlipped(false);
        }
    };

    const prevFlashcard = () => {
        if (currentFlashcard > 0) {
            setCurrentFlashcard(currentFlashcard - 1);
            setIsFlipped(false);
        }
    };

    return (
        <div className="flashcards-section">
            <h2>Flashcards</h2>
            <div className="flashcard-container">
                {flashcardsData.length > 0 ? (
                    <Flashcards
                        flashcard={flashcardsData[currentFlashcard]}
                        flip={flipFlashcard}
                        isFlipped={isFlipped}
                    />
                ) : (
                    <p>Loading flashcards...</p>
                )}
            </div>
            <div className="flashcard-controls">
                <button onClick={prevFlashcard} disabled={currentFlashcard === 0}>
                    Previous
                </button>
                <button onClick={flipFlashcard}>Flip</button>
                <button onClick={nextFlashcard} disabled={currentFlashcard === flashcardsData.length - 1}>
                    Next
                </button>
            </div>
            <Chatbot />
        </div>
    );
};

export default FlashcardsPage;