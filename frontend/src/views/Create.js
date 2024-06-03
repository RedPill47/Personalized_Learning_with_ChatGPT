import React, { useState, useEffect, useContext } from 'react';
import './style/Styles.css';
import Chatbot from './Chatbot';
import PdfViewer from './PdfViewer';
import AuthContext from '../context/AuthContext';
import useAxios from '../utils/useAxios';

const Create = () => {
    const { authTokens } = useContext(AuthContext);
    const axiosInstance = useAxios();

    const [file, setFile] = useState(null);
    const [fileName, setFileName] = useState('');
    const [charCount, setCharCount] = useState(0);
    const [activeTab, setActiveTab] = useState('pasteText');
    const [lessonText, setLessonText] = useState('');
    const [pdfUrl, setPdfUrl] = useState(localStorage.getItem('pdfUrl')); // Initialize with localStorage value if exists
    const [lessonId, setLessonId] = useState(localStorage.getItem('lessonId') || null);
    const [isLoading, setIsLoading] = useState(false); // New loading state

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (file.type === 'application/pdf') {
            setFile(file);
            setFileName(file.name);
            setLessonText(''); // Clear any text input
        } else {
            alert('Please upload a PDF file.');
        }
    };

    const handleTextareaChange = (event) => {
        const text = event.target.value;
        setLessonText(text);
        setCharCount(text.length);
        setFile(null); // Clear any file input
        setFileName('');
    };

    const startMagic = async () => {
        // Clear previous session's data
        setPdfUrl(null);
        localStorage.removeItem('pdfUrl');
        setIsLoading(true); // Set loading state to true

        if (lessonText || file) {
            const formData = new FormData();
            if (lessonText) {
                formData.append('lesson_text', lessonText);
            }
            if (file) {
                formData.append('lesson_pdf', file);
            }
            try {
                const response = await axiosInstance.post('/submit-lesson/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    }
                });
                const pdfPath = response.data.pdf_path;
                const lessonId = response.data.lesson_id;
                console.log('Lesson ID:', lessonId); // Log the lesson ID to the console
                setLessonId(lessonId);
                localStorage.setItem('lessonId', lessonId); // Save the lesson ID to localStorage

                // Save the PDF URL to localStorage
                const fullPdfUrl = `http://localhost:8000${pdfPath}`;
                localStorage.setItem('pdfUrl', fullPdfUrl);

                // Delay the display of the PDF by 1 minute (60000 ms)
                setTimeout(() => {
                    setPdfUrl(fullPdfUrl);
                    setIsLoading(false); // Set loading state to false
                }, 60000);

            } catch (error) {
                console.error("Error in submitLesson:", error.response.data);
                setIsLoading(false); // Set loading state to false in case of error
            }
        } else {
            alert('Please provide either text or a PDF file.');
            setIsLoading(false); // Set loading state to false in case of missing input
        }
    };

    const closePdfViewer = () => {
        setPdfUrl(null);
        localStorage.removeItem('pdfUrl');
    };

    useEffect(() => {
        const darkModeToggle = document.getElementById('darkModeToggle');
        if (darkModeToggle) {
            darkModeToggle.addEventListener('click', () => {
                document.body.classList.toggle('light-mode');
                darkModeToggle.textContent = document.body.classList.contains('light-mode') ? '☀️' : '🌙';
            });
        }
    }, []);

    return (
        <div className="container">
            <div className="main-content">
                <div className="create-section">
                    <h2>Create with Tutor AI</h2>
                    <div className="tabs">
                        <button className={`tablinks ${activeTab === 'pasteText' ? 'active' : ''}`} onClick={() => setActiveTab('pasteText')}>Paste text</button>
                        <button className={`tablinks ${activeTab === 'uploadFile' ? 'active' : ''}`} onClick={() => setActiveTab('uploadFile')}>Upload a file</button>
                    </div>
                    <div id="pasteText" className={`tabcontent ${activeTab === 'pasteText' ? 'active' : ''}`}>
                        <textarea placeholder="Share your notes. We'll work our magic!" rows="10" onChange={handleTextareaChange} value={lessonText}></textarea>
                        <div className="char-counter">{charCount} / 50,000 Characters</div>
                    </div>
                    <div id="uploadFile" className={`tabcontent ${activeTab === 'uploadFile' ? 'active' : ''}`}>
                        <div className="upload-area">
                            <input type="file" id="fileUpload" onChange={handleFileUpload} />
                            <label htmlFor="fileUpload">{fileName || 'Drop a file here'}</label>
                        </div>
                    </div>
                    <button id="startMagic" onClick={startMagic}>Start</button>
                    
                    {isLoading && <p>Loading... Please wait while we process your PDF.</p>}
                </div>
                {pdfUrl && !isLoading && (
                    <div>
                        <button id="startMagic" onClick={closePdfViewer}>Close PDF</button>
                        <PdfViewer pdfUrl={pdfUrl} />
                    </div>
                )}
            </div>
            <Chatbot lessonId={lessonId} />
        </div>
    );
};

export default Create;