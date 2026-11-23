
import streamlit as st
import ollama
import json
import uuid

from pathlib import Path
from datetime import datetime


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Local AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. APPLICATION CONFIGURATION
# =========================================================

APP_NAME = "Local AI Chatbot"

CHAT_FILE = Path(__file__).parent / "chat_history.json"

DEFAULT_MODEL = "qwen3:1.7b"

DEFAULT_SYSTEM_PROMPT = """
You are a helpful, intelligent and beginner-friendly AI assistant.

GENERAL INSTRUCTIONS:
1. Answer the user's question directly and accurately.
2. Use simple, clear and natural language.
3. Keep answers concise unless more detail is requested.
4. Avoid unnecessary introductions and repeated information.
5. Maintain context from the current conversation.
6. Never invent facts. Admit when you are unsure.
7. Use headings and bullet points when they improve readability.

PROGRAMMING INSTRUCTIONS:
1. Provide complete, executable code when the user requests a program.
2. Always use proper Markdown fenced code blocks.
3. Specify the correct language after the opening code fence.
4. Never put an entire program inside inline code formatting.
5. Preserve correct indentation and line breaks.
6. Include necessary imports and example usage.
7. Explain the code in beginner-friendly language when useful.
8. Include expected output when it helps understanding.
9. Avoid incomplete code and unnecessary placeholders.
10. For debugging, explain the issue and provide the corrected code.

FORMATTING:
- Use **bold** for important terms.
- Use headings for longer explanations.
- Use numbered steps for procedures.
- Use fenced code blocks for programming examples.
- Keep responses readable and well structured.

Be friendly, accurate and professional.
"""


# =========================================================
# 3. HELPER FUNCTIONS
# =========================================================

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_new_chat():
    chat_id = uuid.uuid4().hex[:10]

    return {
        "id": chat_id,
        "title": "New Chat",
        "messages": [],
        "created_at": get_current_time(),
        "updated_at": get_current_time()
    }


def save_chat_data():
    """Save all conversations to a local JSON file."""

    try:
        data = {
            "chats": st.session_state.chats,
            "active_chat_id": st.session_state.active_chat_id
        }

        CHAT_FILE.write_text(
            json.dumps(data, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    except OSError as error:
        st.error(f"Unable to save chat history: {error}")


def load_chat_data():
    """Load conversations from local storage."""

    if not CHAT_FILE.exists():
        return {}, None

    try:
        data = json.loads(
            CHAT_FILE.read_text(encoding="utf-8")
        )

        # Support the earlier version's flat message history.
        if isinstance(data, list):
            chat = create_new_chat()

            chat["messages"] = [
                message for message in data
                if isinstance(message, dict)
                and message.get("role") in ("user", "assistant")
                and isinstance(message.get("content"), str)
            ]

            if chat["messages"]:
                first_message = next(
                    (
                        message["content"]
                        for message in chat["messages"]
                        if message["role"] == "user"
                    ),
                    "Previous Conversation"
                )

                chat["title"] = first_message[:40]

            return {chat["id"]: chat}, chat["id"]

        if not isinstance(data, dict):
            return {}, None

        raw_chats = data.get("chats", {})
        chats = {}

        if isinstance(raw_chats, dict):
            for chat_id, chat in raw_chats.items():

                if not isinstance(chat, dict):
                    continue

                messages = chat.get("messages", [])

                if not isinstance(messages, list):
                    messages = []

                valid_messages = [
                    message for message in messages
                    if isinstance(message, dict)
                    and message.get("role") in ("user", "assistant")
                    and isinstance(message.get("content"), str)
                ]

                chats[chat_id] = {
                    "id": chat_id,
                    "title": str(chat.get("title", "New Chat")),
                    "messages": valid_messages,
                    "created_at": chat.get(
                        "created_at", get_current_time()
                    ),
                    "updated_at": chat.get(
                        "updated_at", get_current_time()
                    )
                }

        active_id = data.get("active_chat_id")

        if active_id not in chats:
            active_id = next(iter(chats), None)

        return chats, active_id

    except (json.JSONDecodeError, OSError, TypeError):
        return {}, None


def get_active_chat():
    return st.session_state.chats[
        st.session_state.active_chat_id
    ]


def update_chat_title(chat, first_message):
    """Generate a simple title from the first user message."""

    if chat["title"] == "New Chat":
        title = first_message.strip().replace("\n", " ")
        chat["title"] = (
            title[:40] + "..."
            if len(title) > 40
            else title
        )


def format_chat_as_markdown(chat):
    """Convert a conversation into a Markdown document."""

    content = f"# {chat['title']}\n\n"

    for message in chat["messages"]:

        role = "You" if message["role"] == "user" else "Assistant"

        content += f"## {role}\n\n"
        content += message["content"] + "\n\n"

    return content


# =========================================================
# 4. LOAD INSTALLED OLLAMA MODELS
# =========================================================

@st.cache_data(ttl=30)
def get_installed_models():

    try:
        result = ollama.list()

        return [
            model.model
            for model in result.models
        ]

    except Exception:
        return []


# =========================================================
# 5. GENERATE AI RESPONSE
# =========================================================

def generate_ai_response(messages, model, system_prompt,
                         temperature, max_tokens):

    request = {
        "model": model,

        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            *messages
        ],

        "options": {
            "temperature": temperature,
            "num_predict": max_tokens
        },

        "stream": False
    }

    # Disable Qwen 3 thinking mode to avoid unnecessary
    # reasoning output in the chat interface.
    if model.lower().startswith("qwen3"):
        request["think"] = False

    response = ollama.chat(**request)

    # Support the Ollama response object.
    answer = response.message.content

    if not answer:
        raise ValueError("The model returned an empty response.")

    return answer


# =========================================================
# 6. INITIALIZE SESSION STATE
# =========================================================

if "initialized" not in st.session_state:

    chats, active_chat_id = load_chat_data()

    if not chats:
        first_chat = create_new_chat()
        chats[first_chat["id"]] = first_chat
        active_chat_id = first_chat["id"]

    st.session_state.chats = chats
    st.session_state.active_chat_id = active_chat_id

    st.session_state.selected_model = DEFAULT_MODEL
    st.session_state.temperature = 0.3
    st.session_state.max_tokens = 512
    st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT

    st.session_state.initialized = True


# =========================================================
# 7. LOAD MODELS AND VALIDATE SELECTION
# =========================================================

available_models = get_installed_models()

if available_models:

    if st.session_state.selected_model not in available_models:

        st.session_state.selected_model = (
            DEFAULT_MODEL
            if DEFAULT_MODEL in available_models
            else available_models[0]
        )


# =========================================================
# 8. SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 Local AI Chatbot")

    st.caption("Your personal local AI assistant")

    st.divider()

    # -----------------------------------------------------
    # NEW CHAT
    # -----------------------------------------------------

    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):

        new_chat = create_new_chat()

        st.session_state.chats[new_chat["id"]] = new_chat
        st.session_state.active_chat_id = new_chat["id"]

        save_chat_data()
        st.rerun()

    # -----------------------------------------------------
    # CONVERSATION HISTORY
    # -----------------------------------------------------

    st.subheader("Your Conversations")

    chat_ids = sorted(
        st.session_state.chats.keys(),
        key=lambda chat_id: (
            st.session_state.chats[chat_id]["updated_at"]
        ),
        reverse=True
    )

    selected_chat_id = st.selectbox(
        "Select a conversation",
        options=chat_ids,
        index=chat_ids.index(
            st.session_state.active_chat_id
        ),
        format_func=lambda chat_id: (
            st.session_state.chats[chat_id]["title"]
        )
    )

    if selected_chat_id != st.session_state.active_chat_id:

        st.session_state.active_chat_id = selected_chat_id

        save_chat_data()
        st.rerun()

    active_chat = get_active_chat()

    # -----------------------------------------------------
    # RENAME CHAT
    # -----------------------------------------------------

    with st.expander("✏️ Rename conversation"):

        with st.form("rename_chat_form"):

            new_title = st.text_input(
                "Conversation name",
                value=active_chat["title"],
                max_chars=60
            )

            rename_submitted = st.form_submit_button(
                "Save name",
                use_container_width=True
            )

            if rename_submitted:

                if new_title.strip():

                    active_chat["title"] = new_title.strip()
                    save_chat_data()
                    st.rerun()

                else:
                    st.warning("Please enter a conversation name.")

    # -----------------------------------------------------
    # DELETE AND CLEAR CHAT
    # -----------------------------------------------------

    st.divider()

    if st.button(
        "🗑️ Clear Current Chat",
        use_container_width=True
    ):

        active_chat["messages"] = []
        active_chat["title"] = "New Chat"
        active_chat["updated_at"] = get_current_time()

        save_chat_data()
        st.rerun()

    if st.button(
        "❌ Delete Current Conversation",
        use_container_width=True
    ):

        del st.session_state.chats[
            st.session_state.active_chat_id
        ]

        if st.session_state.chats:

            next_chat_id = next(
                iter(st.session_state.chats)
            )

        else:

            new_chat = create_new_chat()

            st.session_state.chats[new_chat["id"]] = new_chat
            next_chat_id = new_chat["id"]

        st.session_state.active_chat_id = next_chat_id

        save_chat_data()
        st.rerun()

    # -----------------------------------------------------
    # DOWNLOAD CHAT
    # -----------------------------------------------------

    if active_chat["messages"]:

        st.download_button(
            "📥 Download Current Chat",
            data=format_chat_as_markdown(active_chat),
            file_name="chat_conversation.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.divider()

    # -----------------------------------------------------
    # MODEL SETTINGS
    # -----------------------------------------------------

    st.subheader("⚙️ Model Settings")

    if available_models:

        selected_model = st.selectbox(
            "Choose AI Model",
            options=available_models,
            index=available_models.index(
                st.session_state.selected_model
            )
        )

        st.session_state.selected_model = selected_model

    else:

        st.warning(
            "Ollama is unavailable or no models are installed."
        )

    st.caption(
        f"Current model: {st.session_state.selected_model}"
    )

    # -----------------------------------------------------
    # GENERATION SETTINGS
    # -----------------------------------------------------

    with st.expander("Advanced Generation Settings"):

        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1,
            help="Lower values produce more consistent answers."
        )

        st.session_state.max_tokens = st.slider(
            "Maximum response tokens",
            min_value=128,
            max_value=1024,
            value=st.session_state.max_tokens,
            step=64,
            help="Higher values allow longer responses but may take longer."
        )

        st.caption(
            "These settings affect newly generated responses."
        )

    # -----------------------------------------------------
    # SYSTEM PROMPT
    # -----------------------------------------------------

    with st.expander("Customize AI Instructions"):

        st.session_state.system_prompt = st.text_area(
            "System prompt",
            value=st.session_state.system_prompt,
            height=250,
            help="Instructions that define how the assistant behaves."
        )

        if st.button(
            "Reset Instructions",
            use_container_width=True
        ):

            st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT
            st.rerun()

    st.divider()

    # -----------------------------------------------------
    # APPLICATION INFORMATION
    # -----------------------------------------------------

    st.subheader("About")

    st.markdown("**AI Runtime:** Ollama")
    st.markdown("**Interface:** Streamlit")
    st.markdown("**Storage:** Local JSON")
    st.markdown("**Execution:** Local")

    st.caption(
        "Your conversations are stored on this computer."
    )


# =========================================================
# 9. MAIN CHAT INTERFACE
# =========================================================

st.title("🤖 Local AI Chatbot")

st.caption(
    "Ask questions, write code and explore ideas with your local AI assistant."
)

st.divider()

active_chat = get_active_chat()

st.subheader(active_chat["title"])

# Show current model
st.caption(
    f"Running with {st.session_state.selected_model}"
)


# =========================================================
# 10. HANDLE RESPONSE REGENERATION
# =========================================================

if st.session_state.get("regenerate_response", False):

    messages = active_chat["messages"]

    if messages and messages[-1]["role"] == "assistant":
        messages.pop()

    active_chat["updated_at"] = get_current_time()

    st.session_state.regenerate_response = False

    save_chat_data()

    st.session_state.generate_again = True


# =========================================================
# 11. DISPLAY CHAT HISTORY
# =========================================================

if not active_chat["messages"]:

    st.info(
        "👋 Hello! Ask me anything to start a conversation."
    )

    st.markdown(
        """
        **Try asking:**

        - Explain Artificial Intelligence.
        - Write a Python program to check prime numbers.
        - Explain Python decorators.
        - Help me debug a Python program.
        """
    )


for index, message in enumerate(active_chat["messages"]):

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# 12. REGENERATE RESPONSE BUTTON
# =========================================================

if (
    active_chat["messages"]
    and active_chat["messages"][-1]["role"] == "assistant"
):

    if st.button("🔄 Regenerate Response"):

        st.session_state.regenerate_response = True
        st.rerun()


# =========================================================
# 13. GENERATE RESPONSE AFTER REGENERATION
# =========================================================

if st.session_state.get("generate_again", False):

    st.session_state.generate_again = False

    try:

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = generate_ai_response(
                    messages=active_chat["messages"],
                    model=st.session_state.selected_model,
                    system_prompt=st.session_state.system_prompt,
                    temperature=st.session_state.temperature,
                    max_tokens=st.session_state.max_tokens
                )

            st.markdown(answer)

        active_chat["messages"].append({
            "role": "assistant",
            "content": answer
        })

        active_chat["updated_at"] = get_current_time()

        save_chat_data()

        st.rerun()

    except Exception as error:

        st.error(f"Unable to generate response: {error}")


# =========================================================
# 14. CHAT INPUT AND NORMAL RESPONSE GENERATION
# =========================================================

prompt = st.chat_input(
    "Ask me anything...",
    disabled=not bool(available_models)
)

if prompt:

    # Save user message
    active_chat["messages"].append({
        "role": "user",
        "content": prompt
    })

    update_chat_title(active_chat, prompt)

    active_chat["updated_at"] = get_current_time()

    save_chat_data()

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    try:

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = generate_ai_response(
                    messages=active_chat["messages"],
                    model=st.session_state.selected_model,
                    system_prompt=st.session_state.system_prompt,
                    temperature=st.session_state.temperature,
                    max_tokens=st.session_state.max_tokens
                )

            st.markdown(answer)

        # Save assistant response
        active_chat["messages"].append({
            "role": "assistant",
            "content": answer
        })

        active_chat["updated_at"] = get_current_time()

        save_chat_data()

    except Exception as error:

        st.error(
            f"Unable to connect to Ollama or generate a response: {error}"
        )

        st.info(
            "Check whether Ollama is running and your selected model is installed."
        )
