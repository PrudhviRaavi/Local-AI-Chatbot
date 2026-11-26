<div align="center">

# 🤖 Local AI Chatbot

**A privacy-first AI assistant that runs entirely on your machine.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com/)
[![License](https://img.shields.io/badge/License-Open_Source-22c55e?style=for-the-badge)](#-license)

<br>

Built with **Python**, **Streamlit**, and **Ollama** — no external AI APIs, no data leaving your computer.

A modern dark-themed chat interface with conversation management, customizable AI settings, and persistent chat history.

<br>

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 💬 AI Chat

- 🔄 Interact with locally running AI models via Ollama
- 🔀 Switch between installed Ollama models
- 🧠 Maintain context throughout the current conversation
- 📝 Beginner-friendly responses with Markdown formatting
- ⚙️ Customize AI system instructions
- 🔁 Regenerate previous AI responses
- 📋 Copy AI responses to the clipboard

</td>
<td width="50%">

### 🗂️ Conversation Management

- ➕ Create multiple conversations
- 🔄 Switch between previous conversations
- ✏️ Auto-generate titles from first user message
- 📝 Rename conversations
- 🗑️ Delete individual conversations
- 🧹 Clear the current conversation
- 💾 Automatically save conversation history
- 📥 Export conversations as Markdown files

</td>
</tr>
<tr>
<td width="50%">

### 🎨 Modern User Interface

- 🖥️ Clean and modern Streamlit interface
- 🌙 Dark-only appearance
- 💬 Custom chat message styling
- 👤 Separate visual styles for user and AI messages
- 📜 Sidebar conversation history
- 🎯 Styled chat input, buttons, and UI elements
- 📐 Responsive wide-screen layout

</td>
<td width="50%">

### 🔒 Privacy & Local Processing

- 🏠 AI inference runs locally through Ollama
- 🔑 No external AI API key required
- 💻 Conversations stored locally on your computer
- 📄 Chat history saved in a JSON file
- 🛡️ Prompts sent only to your local Ollama service

</td>
</tr>
</table>

---

## ⚙️ AI Configuration

> Customize how the AI assistant responds through the sidebar settings panel.

| Setting | Description | Default |
|:---|:---|:---:|
| 🤖 **AI Model** | Select from installed Ollama models | `qwen3:1.7b` |
| 🌡️ **Temperature** | Control response creativity (0.0 – 1.0) | `0.3` |
| 📏 **Maximum Tokens** | Configure the maximum response length | `512` |
| 📋 **System Prompt** | Customize the AI assistant's behavior | Built-in |

---

## 🛠️ Technology Stack

<div align="center">

| Technology | Purpose |
|:---:|:---|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Application logic |
| ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) | Web-based user interface |
| ![Ollama](https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white) | Local AI model execution |
| ![Qwen](https://img.shields.io/badge/Qwen_3-1.7B-6366f1?style=flat-square) | Default conversational AI model |
| ![JSON](https://img.shields.io/badge/JSON-292929?style=flat-square&logo=json&logoColor=white) | Persistent conversation storage |
| ![HTML/CSS/JS](https://img.shields.io/badge/HTML%2FCSS%2FJS-E34F26?style=flat-square&logo=html5&logoColor=white) | UI styling and clipboard functionality |

</div>

---

## 📁 Project Structure

```
Local-AI-Chatbot/
│
├── 📄 app.py                  # Main application
├── 📄 requirements.txt        # Python dependencies
├── 📄 README.md               # Project documentation
├── 📄 .gitignore              # Git ignore rules
│
├── 💾 chat_history.json       # Generated locally (not committed)
│
└── 📂 venv/                   # Python virtual environment (not committed)
```

> [!NOTE]
> `chat_history.json` and `venv/` are local application files and are excluded from version control via `.gitignore`.

---

## 💻 System Requirements

| Requirement | Details |
|:---|:---|
| **OS** | Windows, Linux, or macOS |
| **Python** | 3.10 or later |
| **Ollama** | Installed and running |
| **AI Model** | At least one Ollama model downloaded |
| **Hardware** | Sufficient RAM and storage for the selected AI model |

> [!TIP]
> The default model is **Qwen 3 1.7B**, which is lightweight and suitable for local experimentation on most hardware.

---

## 🚀 Installation and Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/PrudhviRaavi/Local-AI-Chatbot.git
```

### 2️⃣ Navigate to the project directory

```bash
cd Local-AI-Chatbot
```

### 3️⃣ Create a virtual environment

```bash
python -m venv venv
```

### 4️⃣ Activate the virtual environment

<details>
<summary><b>Windows PowerShell</b></summary>

```powershell
venv\Scripts\Activate.ps1
```

</details>

<details>
<summary><b>Windows Command Prompt</b></summary>

```cmd
venv\Scripts\activate
```

</details>

<details>
<summary><b>Linux / macOS</b></summary>

```bash
source venv/bin/activate
```

</details>

### 5️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 6️⃣ Install Ollama

Download and install Ollama from the official site:

[![Download Ollama](https://img.shields.io/badge/Download-Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com/download)

### 7️⃣ Download the AI model

```bash
ollama pull qwen3:1.7b
```

> You can also download other compatible models through Ollama.

### 8️⃣ Verify Ollama installation

```bash
ollama --version
```

> [!IMPORTANT]
> Make sure the Ollama service is running before starting the application.

### 9️⃣ Run the application

```bash
streamlit run app.py
```

The application will open in your browser at: **http://localhost:8501**

---

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

---

## 🧠 Default AI Model

<div align="center">

The application is configured to use:

**Qwen 3 1.7B**

```python
DEFAULT_MODEL = "qwen3:1.7b"
```

</div>

The application automatically retrieves installed Ollama models and allows you to switch between them through the sidebar.

---

## 📸 Application Features

The application interface includes:

- 🌙 Dark-themed chatbot interface
- 📜 Conversation history and management in the sidebar
- 🤖 AI model selection and advanced generation settings
- 💬 Chat interface with copy and regenerate controls
- 📥 Markdown conversation export

> *Add actual application screenshots here as the project UI evolves.*

---

## 🔮 Future Enhancements

> Planned improvements for future versions:

- [ ] 📄 PDF document upload and text extraction
- [ ] 🔍 Retrieval-Augmented Generation (RAG)
- [ ] 📚 Local document embeddings and semantic search
- [ ] ❓ Document-based question answering
- [ ] ⚡ Streaming AI responses
- [ ] 🔎 Improved conversation search
- [ ] 🤖 Additional local AI model support
- [ ] 🎨 Further UI refinements

---

## 🔐 Privacy

> [!CAUTION]
> This project is designed for **local AI experimentation** only.

The application communicates with Ollama running on your computer and stores conversation history locally. It does **not** require an external AI API key.

Privacy also depends on the configuration of Ollama, the selected model, and any other software running on your computer.

---

## 👨‍💻 Author

<div align="center">

**Prudhvi Raavi**

[![GitHub](https://img.shields.io/badge/GitHub-PrudhviRaavi-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PrudhviRaavi)

</div>

---

## 📄 License

This project is open source. A license has not yet been specified.

---

<div align="center">

⭐ **If you find this project interesting, consider giving the repository a star!** ⭐

<br>

![Made with ❤️](https://img.shields.io/badge/Made_with-❤️-e11d48?style=for-the-badge)
![Runs Locally](https://img.shields.io/badge/Runs-Locally-22c55e?style=for-the-badge)
![No API Key](https://img.shields.io/badge/No_API-Key_Required-6366f1?style=for-the-badge)

</div>
