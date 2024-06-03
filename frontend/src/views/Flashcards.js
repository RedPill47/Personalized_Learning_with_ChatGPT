import React from 'react';
import './style/Flashcards.css';

const Flashcards = ({ flashcard, flip, isFlipped }) => {
    if (!flashcard) {
        return <p>No flashcard available</p>;
    }

    return (
        <div className={`flashcard ${isFlipped ? 'flip' : ''}`} onClick={flip}>
            <div className="flashcard-content front">{flashcard.front}</div>
            <div className="flashcard-content back">{flashcard.back}</div>
        </div>
    );
};

export default Flashcards;