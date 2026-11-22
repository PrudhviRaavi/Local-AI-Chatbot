# 🤖 Local AI Chatbot

A locally running AI chatbot built using **Streamlit, Ollama, and Qwen 3 1.7B**. This project provides a simple conversational interface powered by a locally hosted Large Language Model (LLM).

## ✨ Features

- **Local AI Inference:** Generate responses using Ollama without relying on cloud-based AI APIs.
- **Interactive Chat Interface:** Chat through a clean Streamlit interface.
- **Conversation History:** Maintains conversation context during the session.
- **Custom System Prompt:** Configures the assistant's behavior and response style.
- **Coding Assistance:** Helps explain programming concepts, generate code, and troubleshoot errors.
- **Privacy-Friendly:** Prompts are processed locally by the model.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Chatbot user interface |
| Ollama | Local LLM runtime |
| Qwen 3 1.7B | AI language model |
| Ollama Python Client | Python integration with Ollama |

## ⚙️ Prerequisites

- Python 3.10 or later
- [Ollama](https://ollama.com/)
- Git

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/PrudhviRaavi/Local-AI-Chatbot.git
cd Local-AI-Chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the AI model

Make sure Ollama is installed and running, then execute:

```bash
ollama pull qwen3:1.7b
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

`http://localhost:8501`

## 📁 Project Structure

```text
Local-AI-Chatbot/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 🧠 Model Information

This project currently uses **Qwen 3 1.7B**, a lightweight language model running locally through Ollama.

The model handles general conversations, programming questions, code generation, and technical explanations.

## 🔮 Future Improvements

- Streaming AI responses
- Improved chat interface and user experience
- Chat history persistence
- Model selection
- Chat export functionality

## 👨‍💻 Author

**Prudhvi Raavi**

GitHub: [@PrudhviRaavi](https://github.com/PrudhviRaavi)

---

⭐ If you find this project interesting, consider giving the repository a star!