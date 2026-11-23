# 🤖 Local AI Chatbot

A privacy-focused AI chatbot built using **Python, Streamlit, and Ollama**. It runs AI models locally on your computer, allowing you to interact with an AI assistant without depending on external AI APIs.

The application provides a modern chat interface with conversation management, customizable AI settings, Dark and Light themes, and persistent chat history.

## ✨ Features

### 💬 AI Chat
- Interact with locally running AI models using Ollama.
- Supports switching between installed Ollama models.
- Maintains context throughout the current conversation.
- Beginner-friendly AI responses with Markdown formatting.
- Customizable AI system instructions.
- Regenerate previous AI responses.
- Copy AI responses to the clipboard.

### 🗂️ Conversation Management
- Create multiple conversations.
- Switch between previous conversations.
- Automatically generate conversation titles from the first user message.
- Rename conversations.
- Delete individual conversations.
- Clear the current conversation.
- Automatically save conversation history.
- Export conversations as Markdown files.

### 🎨 Modern User Interface
- Clean and modern Streamlit interface.
- Dark and Light theme options.
- Custom chat message styling.
- Separate visual styles for user and AI messages.
- Sidebar conversation history.
- Improved chat input and buttons.
- Responsive wide-screen layout.

### ⚙️ AI Configuration
Customize how the AI assistant responds:

| Setting | Description |
|---|---|
| AI Model | Select from installed Ollama models |
| Temperature | Control response creativity |
| Maximum Tokens | Configure the maximum response length |
| System Prompt | Customize the AI assistant's behavior |

### 🔒 Privacy and Local Processing
- AI inference runs locally through Ollama.
- No external AI API key required.
- Conversations are stored locally on your computer.
- Chat history is saved in a JSON file.
- Your prompts are sent to your local Ollama service for processing.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web-based user interface |
| Ollama | Local AI model execution |
| Qwen 3 1.7B | Default conversational AI model |
| JSON | Persistent conversation storage |
| HTML, CSS and JavaScript | UI styling and clipboard functionality |

## 📁 Project Structure

```text
Local-AI-Chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── chat_history.json       # Generated locally
│
└── venv/                   # Python virtual environment
```

**Note:** `chat_history.json` and `venv/` are local application files and should not be committed to GitHub.

## 💻 System Requirements

- Windows, Linux, or macOS.
- Python 3.10 or later.
- Ollama installed.
- At least one Ollama model downloaded.
- Sufficient RAM and storage for the selected AI model.

The default model is Qwen 3 1.7B, which is suitable for lightweight local experimentation.

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/PrudhviRaavi/Local-AI-Chatbot.git
```

### 2. Navigate to the project directory

```bash
cd Local-AI-Chatbot
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Install Ollama

Download and install Ollama from:

https://ollama.com/download

### 7. Download the AI model

```bash
ollama pull qwen3:1.7b
```

You can also download other compatible models through Ollama.

### 8. Start Ollama

Make sure the Ollama service is running.

Check the installation:

```bash
ollama --version
```

### 9. Run the application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

http://localhost:8501

## 📦 Dependencies

The project uses the following Python packages:

```text
streamlit
ollama
```

Install them using:

```bash
pip install -r requirements.txt
```

## 🧠 Default AI Model

The application is configured to use:

**Qwen 3 1.7B**

```python
DEFAULT_MODEL = "qwen3:1.7b"
```

The application automatically retrieves the installed Ollama models and allows you to switch between them through the sidebar.

## 📸 Application Features

The application interface includes:

- Conversation history and management in the sidebar.
- AI model selection and advanced generation settings.
- Dark and Light appearance modes.
- Chat interface with copy and regenerate controls.
- Markdown conversation export.

*Add your actual application screenshots here as the project UI evolves.*

## 🔮 Future Enhancements

Planned improvements for future versions:

- PDF document upload and text extraction.
- Retrieval-Augmented Generation (RAG).
- Local document embeddings and semantic search.
- Document-based question answering.
- Streaming AI responses.
- Improved conversation search.
- Additional local AI model support.
- Enhanced UI customization.

## 🔐 Privacy

This project is designed for local AI experimentation.

The application communicates with Ollama running on your computer and stores conversation history locally. It does not require an external AI API key.

Privacy also depends on the configuration of Ollama, the selected model, and any other software running on your computer.

## 👨‍💻 Author

**Prudhvi Raavi**

- GitHub: https://github.com/PrudhviRaavi

## 📄 License

This project is open source. A license has not yet been specified.

---

⭐ If you find this project interesting, consider giving the repository a star!