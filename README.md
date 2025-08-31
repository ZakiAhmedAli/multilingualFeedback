# **Multilingual Customer Feedback Analyzer 🗣️**

A full-stack web application designed to collect, analyze, and visualize customer feedback from multiple languages. This tool leverages the power of Google's Gemini AI to provide real-time insights into customer sentiment, breaking down language barriers.

The entire application is containerized with Docker Compose for a seamless one-command setup and deployment.

## **✨ Features**

* **Multilingual Input**: Accepts customer feedback in any language.  
* **AI-Powered Analysis**: Automatically performs:  
  * Language Detection  
  * Translation to English  
  * Sentiment Analysis (Positive, Negative, Neutral)  
* **Real-time Dashboard**: Visualizes sentiment statistics as feedback is submitted.  
* **Feedback Management**: Displays all recent feedback in a clear, filterable table.  
* **Easy Setup**: Fully containerized with Docker, running the entire stack with a single command.

## **🛠️ Tech Stack Overview**

| Component | Technology |
| :---- | :---- |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) (Python) |
| **Frontend** | [React](https://reactjs.org/) (JavaScript) |
| **Database** | [PostgreSQL](https://www.postgresql.org/) |
| **AI Integration** | [Google Gemini API](https://ai.google.dev/) |
| **Containerization** | [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) |

## **🚀 Getting Started & How to Run**

Follow these steps to get the project running on your local machine or in a cloud development environment.

### **Prerequisites**

* **Docker Desktop**: Make sure you have Docker and Docker Compose installed and running.  
* **Git**: For cloning the repository.  
* **Gemini API Key**: You need a valid API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### **Installation & Setup**

1. **Clone the repository:**  
   git clone \<your-repository-url\>  
   cd multilingual-feedback

2. Create the environment file:  
   Create a file named .env in the root of the project directory and add the following content.  
   File: .env  
   DATABASE\_URL=postgresql://user:password@db:5432/feedback\_db  
   GEMINI\_API\_KEY="PASTE\_YOUR\_GEMINI\_API\_KEY\_HERE"

3. Add your Gemini API Key:  
   Replace PASTE\_YOUR\_GEMINI\_API\_KEY\_HERE in the .env file with your actual key.  
4. Build and Run with Docker Compose:  
   From the root directory, run the following command. This will build the container images and start all the services.  
   docker-compose up \--build
   Once the process is complete, a prompt will appear to open the frontend (port 3000) in a new browser tab. Your application will function as if it were running locally on your machine.

### **Accessing the Application**

* **Frontend Application**: Open your browser and navigate to http://localhost:3000  
* **Backend API Docs**: The auto-generated FastAPI documentation is available at http://localhost:8000/docs

# Top Recommendations

## How to Get Started with GitHub Codespaces

This is the most direct way to continue with the project structure I provided earlier.

### Launch the Codespace

1. On your repository's main page, click the green `< > Code` button.
2. Go to the **"Codespaces"** tab.
3. Click **"Create codespace on main"**.

### Develop Online

After a minute or two, a complete VS Code environment will open in your browser. This is your virtual development machine.

### Run the Project

1. Open the integrated terminal in the online VS Code editor (`Ctrl+` or `Cmd+`).
2. Create your .env file and add your Gemini API key as previously instructed, or use the existing one provided in the project.
3. Run the same command you would have run locally:

   ```bash
   docker-compose up --build
### Codespaces will automatically detect the running services and provide you with a forwarded port.
You'll see a pop-up to open the frontend (port 3000) in a new browser tab.
Your application will work exactly as if it were running on your own machine.


## **🏗️ Architecture Overview**

The application is composed of three main services orchestrated by Docker Compose.

* **Frontend (React)**: A Single-Page Application (SPA) that provides the user interface for submitting and viewing feedback. It is served by an Nginx web server, which also proxies API requests to the backend to avoid CORS issues.  
* **Backend (FastAPI)**: The core of the application. It exposes a REST API to:  
  * Receive new feedback.  
  * Communicate with the Gemini API for analysis.  
  * Perform CRUD operations on the PostgreSQL database.  
  * It uses **SQLAlchemy** as an ORM for database interaction and **Pydantic** for data validation.  
* **Database (PostgreSQL)**: A relational database used to store all feedback entries. Data persistence is guaranteed through a Docker volume.

## **⚙️ API Routes and Usage**

The backend provides the following endpoints:

| Method | Route | Description | Request Body | Response |
| :---- | :---- | :---- | :---- | :---- |
| POST | /api/feedback | Submits new feedback, triggers AI analysis, and saves it to the database. | {"text": "string", "product": "string (optional)"} | A JSON object of the newly created feedback entry. |
| GET | /api/feedback | Retrieves a list of all feedback entries. Can be filtered. | None. Query params: ?product=... or ?language=... | A JSON array of all matching feedback objects. |
| GET | /api/stats | Calculates and returns the sentiment statistics for all feedback. | None | A JSON object with overall statistics. |

## **Schemas**

### **Data Schema (PostgreSQL)**

The feedback table stores all the necessary information.

| Column | Data Type | Description |
| :---- | :---- | :---- |
| id | INTEGER | Primary Key, auto-incrementing. |
| original\_text | TEXT | The original feedback submitted by the user. |
| translated\_text | TEXT | The English translation from Gemini. |
| sentiment | VARCHAR(50) | The sentiment (positive, negative, neutral). |
| language | VARCHAR(50) | The language detected by Gemini. |
| product | VARCHAR(100) | The optional product name. |

## **🤖 Gemini Studio Integration**

The integration with Gemini is handled by the backend in the analyze\_text\_with\_gemini function.

1. A carefully crafted **prompt** is sent to the gemini-1.5-flash-latest model.  
2. The prompt instructs the model to perform three tasks: detect the language, translate the text to English, and classify the sentiment.  
3. Crucially, the prompt asks the model to return its response as a **structured JSON object**.  
4. The backend then parses this JSON to extract the analysis results.  
5. A fallback mechanism is in place to handle potential API errors, ensuring the application remains stable.

## **⚠️ Limitations & Known Issues**

* **API Rate Limiting**: The application uses the free tier of the Gemini API, which has rate limits. A high volume of submissions in a short period may lead to temporary analysis failures.  
* **Analysis Accuracy**: While powerful, AI analysis is not infallible. Complex slang, sarcasm, or mixed-language sentences may occasionally result in incorrect sentiment or language detection.  
* **No User Authentication**: The API is public and does not have any authentication or authorization layers.  
* **Basic Filtering**: The filtering capabilities on the "Recent Feedback" table are basic and do not support advanced queries like date ranges or full-text search.
