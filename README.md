# Tutor AI

Tutor AI is a web application designed to enhance learning experiences by providing personalized educational content, quizzes, and flashcards.

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Python
- Node.js and npm
- MikTeX

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/RedPill47/Personalized_Learning_with_ChatGPT.git
    ```
    ```sh
    cd Personalized_Learning_with_ChatGPT
    ```

2. **Setup Environment Variables:**

    - Rename the `.env-example` file to `.env`.
    - Open the `.env` file and add your API keys for OpenAI, Serper, and Browserless:


    ```
    OPENAI_API_KEY=your_openai_api_key
    SERPER_API_KEY=your_serper_api_key
    BROWSERLESS_API_KEY=your_browserless_api_key
    ```

3. **Backend Setup:**

    Open a terminal and run the following commands:

    **For Windows users:**

    ```sh
    env\Scripts\activate
    ```
    ```sh
    cd backend
    ```
    ```sh
    python manage.py runserver
    ```

    **For macOS/Linux users:**

    ```sh
    source env/bin/activate
    ```
    ```sh
    cd backend
    ```
    ```sh
    python manage.py runserver
    ```

4. **Frontend Setup:**

    Open another terminal and run the following commands:

    ```sh
    cd frontend
    ```
    ```sh
    npm install
    ```
    ```sh
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

## Screenshots

### Homepage
![Homepage](media/Homepage.png)

### Chatbot Interface
![Chatbot Interface](media/Chatbot%20interface%20(ask%20question).png)

### Create Page with Upload File Field
![Create Page](media/Create%20page%20with%20upload%20file%20field.png)

### Flashcards Page
![Flashcards Page](media/Flashcards%20page%20with%20content.png)

### Quiz Page
![Quiz Page](media/Quiz%20page%20with%20content.png)

## Contributing

Feel free to fork the project, make improvements, and submit pull requests.
