# 💰 Price Intelligent Tracker

An AI-powered price intelligence assistant that analyzes product prices, historical trends, and product information to help users make smarter purchase decisions.

The application combines **Generative AI, RAG, tool calling, vector search, FastAPI, Streamlit, Docker, and SQLite** into an end-to-end production-style application.

---

## 🚀 Live Application

**Live Demo:** https://price-intelligence-ui.onrender.com/

---

## 📌 Project Overview

Price Intelligent Tracker allows users to select a product and ask natural-language questions such as:

* Should I buy this product now?
* Is the current price a good deal?
* How has the price changed historically?
* Should I wait before purchasing?
* What does the historical price trend look like?
* Is this product suitable for my requirements?

Instead of relying only on predefined rules, the application uses an **LLM-powered agent** to understand the user's question, retrieve relevant product information, use available tools when required, and generate a natural-language response.

---

## 🎯 Key Features

### 1. 🤖 GenAI-Powered Assistant

Users can interact with the application using natural-language questions.

The LLM interprets the user's intent and generates a contextual response based on available product information.

### 2. 🔎 Retrieval-Augmented Generation (RAG)

Product knowledge is converted into embeddings and stored in a vector database.

When a user asks a question:

```text
User Question
      ↓
Embedding
      ↓
Vector Search
      ↓
Relevant Documents
      ↓
LLM
      ↓
Grounded Response
```

This helps the LLM generate responses based on the application's product knowledge rather than relying entirely on its pretrained knowledge.

### 3. 🛠️ Tool Calling

The agent can use application tools to retrieve structured information such as:

* Current product price
* Historical price information
* Product details
* Purchase-related information

This allows the system to combine **LLM reasoning with deterministic application logic**.

### 4. 📊 Price Intelligence

The application maintains product and historical pricing information.

This enables questions involving:

* Current price
* Historical price
* Price trends
* Price comparisons
* Buy/wait recommendations

### 5. 🔌 FastAPI Backend

The GenAI functionality is exposed through a REST API using FastAPI.

Example flow:

```text
Streamlit
    ↓
POST /api/v1/query
    ↓
FastAPI
    ↓
AI Agent
    ↓
RAG + Tools
    ↓
Groq LLM
    ↓
Response
```

### 6. 🖥️ Streamlit Frontend

The Streamlit application provides a simple interface for:

* Selecting products
* Entering natural-language questions
* Viewing AI-generated recommendations
* Viewing agent execution details

### 7. 🐳 Dockerized Application

The application is containerized using Docker.

Separate containers are used for:

* FastAPI backend
* Streamlit frontend

This provides a consistent runtime environment and makes the application easier to deploy.

### 8. ☁️ Cloud Deployment

The application is deployed using Render.

The deployment demonstrates an end-to-end workflow:

```text
GitHub
   ↓
Docker Build
   ↓
Render
   ↓
Backend + Frontend
   ↓
Live Application
```

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Streamlit Frontend  │
                         └──────────┬──────────┘
                                    │
                              HTTP Request
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   FastAPI Backend   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    AI Agent / LLM   │
                         └──────┬───────┬──────┘
                                │       │
                       ┌────────┘       └─────────┐
                       ▼                          ▼
              ┌─────────────────┐        ┌─────────────────┐
              │   RAG Pipeline  │        │  Application    │
              │                 │        │     Tools       │
              └────────┬────────┘        └────────┬────────┘
                       │                          │
                       ▼                          ▼
              ┌─────────────────┐        ┌─────────────────┐
              │ Vector Database │        │ SQLite Database │
              └─────────────────┘        └─────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Relevant Context│
              └────────┬────────┘
                       │
                       └──────────────┐
                                      ▼
                              ┌───────────────┐
                              │   Groq LLM    │
                              └───────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │ AI Response   │
                              └───────────────┘
```

---

## 🔄 Application Workflow

### Step 1 — Product Selection

The user selects a product from the Streamlit interface.

### Step 2 — User Question

The user enters a natural-language question.

For example:

```text
Should I buy this product now?
```

### Step 3 — API Request

The frontend sends the product ID and question to the FastAPI backend.

```text
POST /api/v1/query
```

### Step 4 — Agent Processing

The backend passes the request to the AI/agent layer.

The agent determines what information is required to answer the question.

### Step 5 — Retrieval

Relevant product information is retrieved from the vector database using semantic similarity search.

### Step 6 — Tool Execution

If structured information is required, the agent can invoke application tools to obtain data from SQLite.

### Step 7 — LLM Generation

The retrieved context and tool results are provided to the LLM.

The LLM generates the final response.

### Step 8 — Response

FastAPI returns the response to Streamlit.

The user sees the recommendation along with execution information such as:

* LLM calls
* Tool calls
* Tools used
* Execution status

---

## 🛠️ Technology Stack

### AI / GenAI

* Python
* LangChain
* LLM
* RAG
* Embeddings
* Vector Search
* Tool Calling
* AI Agents

### Backend

* FastAPI
* Uvicorn
* REST API

### Frontend

* Streamlit

### Database

* SQLite
* Chroma Vector Database

### LLM Provider

* Groq

### Embedding Model

* `sentence-transformers/all-MiniLM-L6-v2`

### DevOps / Deployment

* Docker
* Docker Compose
* GitHub
* Render

---

## 📂 Project Structure

```text
price-intelligent-tracker/
│
├── app.py
├── api.py
├── config.py
├── database.py
├── rag.py
├── tools.py
├── generate_database.py
│
├── price_intelligence.db
│
├── data/
│   └── product_knowledge.csv
│
├── chroma_db/
│
├── requirements.txt
│
├── Dockerfile
├── Dockerfile.api
├── docker-compose.yml
│
└── README.md
```

> Note: `.env` containing API credentials should not be committed to GitHub.

---

## ⚙️ Local Setup

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>

cd price-intelligent-tracker
```

### 2. Create a Virtual Environment

```bash
python -m venv venv_price
```

Activate it on Windows:

```bash
venv_price\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
groq_api_key=YOUR_GROQ_API_KEY
groq_model=openai/gpt-oss-120b
```

Do not commit `.env` to GitHub.

Add it to `.gitignore`:

```text
.env
venv_price/
__pycache__/
```

---

## ▶️ Running the Application Locally

### Start the FastAPI Backend

```bash
uvicorn api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Start the Streamlit Frontend

Open another terminal:

```bash
streamlit run app.py
```

The Streamlit application will then open in your browser.

---

## 🐳 Running with Docker

Build and start the application using Docker Compose:

```bash
docker compose up --build
```

The application consists of two services:

```text
price-intelligence-api
price-intelligence-ui
```

FastAPI:

```text
http://localhost:8000
```

Streamlit:

```text
http://localhost:8501
```

To stop the containers:

```bash
docker compose down
```

---

## 🔐 Environment Variables

The application uses environment variables for sensitive configuration.

| Variable                     | Description                         |
| ---------------------------- | ----------------------------------- |
| `groq_api_key`               | API key used to access the Groq LLM |
| `groq_model`                 | LLM model used by the application   |
| `PRICE_INTELLIGENCE_API_URL` | URL of the FastAPI backend          |

Example:

```env
groq_api_key=YOUR_API_KEY
groq_model=openai/gpt-oss-120b
PRICE_INTELLIGENCE_API_URL=http://127.0.0.1:8000
```

API keys should never be committed to source control.

---

## 🧪 Example Queries

After selecting a product, try questions such as:

```text
Should I buy this product now?
```

```text
Is the current price a good deal?
```

```text
How has the price changed historically?
```

```text
Should I wait for a better price?
```

```text
What is the current price compared to its historical prices?
```

```text
What would you recommend if I can wait for one month?
```

The application combines retrieved information, structured product data, and LLM reasoning to generate the response.

---

## 📈 Example Architecture Decision

A key design decision in this project is separating the frontend from the GenAI backend.

```text
Frontend
   │
   │ HTTP
   ▼
FastAPI
   │
   ├── Agent
   ├── RAG
   ├── Tools
   ├── Vector Database
   └── LLM
```

This separation provides several benefits:

* Independent frontend and backend deployment
* Easier API testing
* Better separation of responsibilities
* Ability to replace the frontend later
* Easier backend scaling
* Cleaner GenAI architecture

---

## ⚠️ Challenges Solved During Development

The project also involved solving several real-world engineering problems.

### Environment and API Configuration

Handled API credentials through environment variables instead of hardcoding secrets.

### Dockerization

Created separate Docker configurations for the FastAPI backend and Streamlit frontend.

### Frontend/Backend Communication

Connected the Streamlit frontend to the FastAPI backend through REST APIs.

### Database Availability

Ensured the SQLite database containing product information is available to the deployed application.

### LLM Integration

Integrated a Groq-hosted LLM into the agent workflow.

### Deployment Debugging

Resolved deployment issues involving:

* Missing environment variables
* Container startup failures
* Database availability
* Backend HTTP 500 errors
* Frontend/backend connectivity

These issues helped validate the application beyond a purely local development environment.

---

## 🔮 Future Improvements

The current version focuses on demonstrating the complete GenAI workflow. Possible improvements include:

### 1. 📊 Price Trend Visualization

Add interactive charts showing historical price movement.

### 2. 🧪 Automated GenAI Evaluation

Create an evaluation dataset to measure:

* Answer correctness
* Retrieval quality
* Tool selection
* Hallucination rate
* Response latency

### 3. 🔍 Improved Retrieval

Experiment with:

* Chunking strategies
* Top-K retrieval
* Similarity score thresholds
* Hybrid search
* Reranking

### 4. 👀 LLM Observability

Integrate LangSmith to monitor:

* LLM calls
* Prompts
* Retrieval
* Tool calls
* Latency
* Errors

### 5. 🗄️ Production Database

Replace SQLite with a production-grade database such as PostgreSQL.

### 6. ☁️ Scalable Vector Storage

Move from a local vector database to a managed vector database when scaling the application.

### 7. 🔐 Security Improvements

Add:

* API authentication
* Rate limiting
* Input validation
* Prompt injection protection
* Secure secret management

### 8. 📡 Real-Time Price Data

Integrate external product/price APIs to replace the current sample price dataset with continuously updated pricing information.


---

## 📄 License

This project is intended for learning, experimentation, and portfolio demonstration.
