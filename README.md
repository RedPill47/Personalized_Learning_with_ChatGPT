# Tutor AI

Tutor AI is a web application designed to enhance learning experiences by providing personalized educational content, quizzes, and flashcards.

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Python
- Node.js and npm

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/RedPill47/Personalized_Learning_with_ChatGPT.git
    cd Personalized_Learning_with_ChatGPT
    ```

2. **Backend Setup:**

    Open a terminal and run the following commands:

    **For Windows users:**

    ```sh
    env\Scripts\activate
    cd backend
    python manage.py runserver
    ```

    **For macOS/Linux users:**

    ```sh
    source env/bin/activate
    cd backend
    python manage.py runserver
    ```

4. **Frontend Setup:**

    Open another terminal and run the following commands:

    ```sh
    cd frontend
    npm install
    npm start
    ```

### Running the Application

- The backend server will run on `http://127.0.0.1:8000/`.
- The frontend server will run on `http://localhost:3000/`.

Open your web browser and navigate to `http://localhost:3000/` to access the application.

## Features

- Create personalized educational content
- Take quizzes to assess knowledge
- Use flashcards for efficient learning
- Chatbot for interactive learning assistance

## Contributing

Feel free to fork the project, make improvements, and submit pull requests.
