
import streamlit as st
import streamlit.components.v1 as components
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
1. Answer questions directly and accurately.
2. Use simple, clear and natural language.
3. Keep answers concise unless more detail is requested.
4. Avoid unnecessary introductions and repetition.
5. Maintain context from the current conversation.
6. Never invent facts. Admit when you are unsure.
7. Use headings and bullet points when useful.

PROGRAMMING INSTRUCTIONS:
1. Provide complete, executable code when requested.
2. Always use properly formatted Markdown code blocks.
3. Specify the correct programming language.
4. Never put an entire program inside inline code formatting.
5. Preserve correct indentation and line breaks.
6. Include necessary imports and example usage.
7. Explain code in beginner-friendly language when useful.
8. Include expected output when appropriate.
9. Avoid incomplete code and unnecessary placeholders.
10. For debugging, explain the issue and provide corrected code.

FORMATTING:
- Use bold for important terms.
- Use headings for longer explanations.
- Use numbered steps for procedures.
- Use fenced code blocks for programming examples.
- Keep responses readable and well structured.

Be friendly, accurate and professional.
"""


# =========================================================
# 3. CHAT DATA FUNCTIONS
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


def load_chat_data():

    if not CHAT_FILE.exists():
        return {}, None

    try:

        data = json.loads(
            CHAT_FILE.read_text(encoding="utf-8")
        )

        # Compatibility with previous flat chat history
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


def save_chat_data():

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

        st.error(f"Unable to save conversations: {error}")


def get_active_chat():

    return st.session_state.chats[
        st.session_state.active_chat_id
    ]


def update_chat_title(chat, prompt):

    if chat["title"] == "New Chat":

        title = prompt.strip().replace("\n", " ")

        chat["title"] = (
            title[:40] + "..."
            if len(title) > 40
            else title
        )


def format_chat_as_markdown(chat):

    content = f"# {chat['title']}\n\n"

    for message in chat["messages"]:

        role = (
            "You"
            if message["role"] == "user"
            else "Assistant"
        )

        content += f"## {role}\n\n"
        content += message["content"] + "\n\n"

    return content


# =========================================================
# 4. OLLAMA MODEL MANAGEMENT
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


def generate_ai_response(
    messages,
    model,
    system_prompt,
    temperature,
    max_tokens
):

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

    # Disable Qwen 3 thinking mode
    if model.lower().startswith("qwen3"):
        request["think"] = False

    response = ollama.chat(**request)

    answer = response.message.content

    if not answer:
        raise ValueError("The model returned an empty response.")

    return answer


# =========================================================
# 5. COPY RESPONSE COMPONENT
# =========================================================

def copy_button(text, key):

    # JavaScript clipboard button.
    # Uses a fallback if clipboard API is unavailable.

    escaped_text = json.dumps(text)

    html = f"""
    <html>
    <body style="
        margin:0;
        padding:0;
        background:transparent;
        font-family:Arial,sans-serif;
    ">

    <button id="copy-{key}" style="
        border:1px solid var(--unused, #888888);
        border-radius:8px;
        padding:6px 12px;
        background:transparent;
        color:#888888;
        font-size:12px;
        cursor:pointer;
    ">
        📋 Copy response
    </button>

    <script>
    const copyText = {escaped_text};

    const button = document.getElementById("copy-{key}");

    button.addEventListener("click", async function() {{

        try {{

            if (navigator.clipboard && window.isSecureContext) {{

                await navigator.clipboard.writeText(copyText);

            }} else {{

                const textarea = document.createElement("textarea");

                textarea.value = copyText;

                textarea.style.position = "fixed";
                textarea.style.opacity = "0";

                document.body.appendChild(textarea);

                textarea.select();

                const success = document.execCommand("copy");

                textarea.remove();

                if (!success) {{
                    throw new Error("Clipboard unavailable");
                }}
            }}

            button.innerText = "✓ Copied!";
            button.style.color = "#16a34a";

            setTimeout(function() {{
                button.innerText = "📋 Copy response";
                button.style.color = "#888888";
            }}, 1800);

        }} catch (error) {{

            button.innerText = "Copy unavailable";

        }}

    }});
    </script>

    </body>
    </html>
    """

    components.html(
        html,
        height=38,
        scrolling=False
    )

# =========================================================
# 6. SESSION STATE INITIALIZATION
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
    st.session_state.theme = "Dark"
    st.session_state.initialized = True


# Ensure all settings exist, including after app reruns

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.3

if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 512

if "selected_model" not in st.session_state:
    st.session_state.selected_model = DEFAULT_MODEL

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT

# =========================================================
# 7. LOAD MODELS
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

    st.markdown(
        """
        <div style="padding:8px 0 15px 0;">
            <h2 style="margin:0;">🤖 Local AI</h2>
            <p style="color:gray;font-size:13px;">
                Your personal AI assistant
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # NEW CHAT BUTTON

    if st.button(
        "＋  New Chat",
        use_container_width=True,
        type="primary"
    ):

        new_chat = create_new_chat()

        st.session_state.chats[new_chat["id"]] = new_chat

        st.session_state.active_chat_id = new_chat["id"]

        save_chat_data()

        st.rerun()

    st.divider()

    # CONVERSATION HISTORY

    st.markdown("### 💬 History")

    chat_ids = sorted(
        st.session_state.chats.keys(),
        key=lambda chat_id: (
            st.session_state.chats[chat_id]["updated_at"]
        ),
        reverse=True
    )

    for chat_id in chat_ids:

        chat = st.session_state.chats[chat_id]

        is_active = (
            chat_id == st.session_state.active_chat_id
        )

        button_label = (
            f"●  {chat['title']}"
            if is_active
            else f"   {chat['title']}"
        )

        if st.button(
            button_label,
            key=f"history_{chat_id}",
            use_container_width=True,
            type="secondary" if not is_active else "primary"
        ):

            st.session_state.active_chat_id = chat_id

            save_chat_data()

            st.rerun()

    active_chat = get_active_chat()

    # CHAT MANAGEMENT

    with st.expander("✏️ Manage conversation"):

        with st.form("rename_chat_form"):

            new_title = st.text_input(
                "Conversation name",
                value=active_chat["title"],
                max_chars=60
            )

            if st.form_submit_button(
                "Rename",
                use_container_width=True
            ):

                if new_title.strip():

                    active_chat["title"] = new_title.strip()

                    save_chat_data()

                    st.rerun()

                else:

                    st.warning("Enter a conversation name.")

        if st.button(
            "Clear current chat",
            use_container_width=True
        ):

            active_chat["messages"] = []

            active_chat["title"] = "New Chat"

            active_chat["updated_at"] = get_current_time()

            save_chat_data()

            st.rerun()

        if st.button(
            "Delete conversation",
            use_container_width=True
        ):

            del st.session_state.chats[
                st.session_state.active_chat_id
            ]

            if not st.session_state.chats:

                new_chat = create_new_chat()

                st.session_state.chats[new_chat["id"]] = new_chat

            st.session_state.active_chat_id = next(
                iter(st.session_state.chats)
            )

            save_chat_data()

            st.rerun()

    # DOWNLOAD CONVERSATION

    if active_chat["messages"]:

        st.download_button(
            "📥 Download conversation",
            data=format_chat_as_markdown(active_chat),
            file_name="chat_conversation.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.divider()

    # APPEARANCE

    st.markdown("### 🎨 Appearance")

    selected_theme = st.selectbox(
        "Theme",
        ["Dark", "Light"],
        index=(
            0
            if st.session_state.theme == "Dark"
            else 1
        )
    )

    st.session_state.theme = selected_theme

    st.divider()

    # MODEL SETTINGS

    st.markdown("### ⚙️ AI Settings")

    if available_models:

        selected_model = st.selectbox(
            "AI Model",
            available_models,
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
        f"Selected model: {st.session_state.selected_model}"
    )

    with st.expander("Advanced settings"):

        st.session_state.temperature = st.slider(
            "Temperature",
            0.0,
            1.0,
            st.session_state.temperature,
            0.1
        )

        st.session_state.max_tokens = st.slider(
            "Maximum response tokens",
            128,
            1024,
            st.session_state.max_tokens,
            64
        )

        st.session_state.system_prompt = st.text_area(
            "AI instructions",
            value=st.session_state.system_prompt,
            height=220
        )

        if st.button(
            "Reset AI instructions",
            use_container_width=True
        ):

            st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT

            st.rerun()

    st.divider()

    st.markdown(
        """
        <div style="text-align:center;padding:8px 0;color:gray;">
            <p style="font-size:12px;margin:0;">
                Powered by Ollama
            </p>
            <p style="font-size:11px;margin:4px 0;">
                Private · Local · Open Source
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )



# =========================================================
# 9. THEME STYLING
# =========================================================

if st.session_state.theme == "Dark":

    background = "#0e1117"
    sidebar_background = "#151922"
    text_color = "#f1f5f9"
    muted_color = "#9ca3af"
    border_color = "#303642"
    assistant_background = "#1a202c"
    user_background = "#243247"
    input_background = "#1a202c"
    button_background = "#252d3a"

else:

    background = "#ffffff"
    sidebar_background = "#f7f8fa"
    text_color = "#202124"
    muted_color = "#6b7280"
    border_color = "#e5e7eb"
    assistant_background = "#f3f4f6"
    user_background = "#e8f0fe"
    input_background = "#ffffff"
    button_background = "#f3f4f6"


st.markdown(
    f"""
    <style>

    /* GLOBAL APPLICATION */

    .stApp,
    [data-testid="stAppViewContainer"] {{
        background-color: {background} !important;
        color: {text_color} !important;
    }}

    .main .block-container {{
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }}

    /* SIDEBAR */

    [data-testid="stSidebar"] {{
        background-color: {sidebar_background} !important;
        border-right: 1px solid {border_color};
    }}

    [data-testid="stSidebar"] > div {{
        background-color: {sidebar_background} !important;
    }}

    [data-testid="stSidebar"] * {{
        color: {text_color};
    }}

    /* TEXT */

    h1, h2, h3, h4, p, li, label,
    [data-testid="stMarkdownContainer"] {{
        color: {text_color};
    }}

    [data-testid="stCaptionContainer"] {{
        color: {muted_color} !important;
    }}

    
    /* CHAT MESSAGE DEFAULT */

    [data-testid="stChatMessage"] {{
        border: 1px solid {border_color};
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
    }}

    /* USER MESSAGE */

    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) {{
        background-color: {user_background} !important;
    }}

    /* AI ASSISTANT MESSAGE */

    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarAssistant"]
    ) {{
        background-color: {assistant_background} !important;
    }}

    /* CHAT INPUT */

    [data-testid="stChatInput"] {{
        background-color: {input_background} !important;
        border: 1px solid {border_color} !important;
        border-radius: 15px;
    }}

    [data-testid="stChatInput"] textarea {{
        background-color: {input_background} !important;
        color: {text_color} !important;
        -webkit-text-fill-color: {text_color} !important;
    }}

    [data-testid="stChatInput"] textarea::placeholder {{
        color: {muted_color} !important;
        -webkit-text-fill-color: {muted_color} !important;
    }}

    /* TEXT INPUTS */

    .stTextInput input,
    .stTextArea textarea {{
        background-color: {input_background} !important;
        color: {text_color} !important;
        -webkit-text-fill-color: {text_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 9px;
    }}

    /* SELECT BOXES */

    [data-testid="stSelectbox"] [data-baseweb="select"] > div {{
        background-color: {input_background} !important;
        color: {text_color} !important;
        border-color: {border_color} !important;
    }}

    [data-testid="stSelectbox"] input {{
        color: {text_color} !important;
    }}

    /* BUTTONS */

    .stButton button,
    .stDownloadButton button {{
        background-color: {button_background} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 9px;
        transition: all 0.2s ease;
    }}

    .stButton button:hover,
    .stDownloadButton button:hover {{
        border-color: #6366f1 !important;
        color: {text_color} !important;
    }}

    /* SLIDERS */

    [data-testid="stSlider"] {{
        color: {text_color};
    }}

    /* EXPANDERS */

    [data-testid="stExpander"] {{
        border-color: {border_color} !important;
    }}

    [data-testid="stExpander"] details {{
        background-color: {sidebar_background};
    }}

    /* DIVIDERS */

    hr {{
        border-color: {border_color} !important;
    }}

    /* CODE BLOCKS */

    [data-testid="stCodeBlock"] {{
        border-radius: 10px;
    }}

    /* CHECKBOXES AND RADIO BUTTONS */

    [data-testid="stCheckbox"],
    [data-testid="stRadio"] {{
        color: {text_color} !important;
    }}

    /* POPOVERS AND DROPDOWNS */

    [data-baseweb="popover"] {{
        background-color: {input_background} !important;
        color: {text_color} !important;
    }}

    
    /* TOP HEADER */

    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}

    /* BOTTOM CHAT INPUT AREA */

    [data-testid="stBottom"] {{
        background-color: transparent !important;
    }}

    [data-testid="stBottom"] > div {{
        background-color: transparent !important;
    }}

    [data-testid="stBottomBlockContainer"] {{
        background-color: transparent !important;
    }}

    /* CHAT INPUT OUTER CONTAINER */

    [data-testid="stChatInput"] {{
        background-color: {input_background} !important;
        border: 1px solid {border_color} !important;
    }}

    [data-testid="stChatInput"] > div {{
        background-color: {input_background} !important;
    }}

    /* MAIN CONTENT BOTTOM AREA */

    [data-testid="stMain"] {{
        background-color: {background} !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 10. MAIN CHAT HEADER
# =========================================================

active_chat = get_active_chat()

st.markdown(
    """
    <div style="padding:5px 0 10px 0;">
        <h1 style="font-size:29px;margin-bottom:3px;">
            Local AI Chatbot
        </h1>
        <p style="font-size:14px;color:gray;">
            Your personal AI assistant, running locally.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    f"Model: {st.session_state.selected_model}"
)

st.divider()


# =========================================================
# 11. DISPLAY CONVERSATION HISTORY
# =========================================================

if not active_chat["messages"]:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:75px 15px 65px 15px;
        ">
            <div style="font-size:48px;">🤖</div>
            <h2 style="margin:15px 0 5px 0;">
                How can I help you today?
            </h2>
            <p style="color:gray;font-size:14px;">
                Ask a question, write code or explore something new.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("**💡 Learn something**")

        st.caption("Explain Artificial Intelligence in simple terms.")

    with col2:

        st.markdown("**💻 Write code**")

        st.caption("Write a Python program to check prime numbers.")


for index, message in enumerate(active_chat["messages"]):

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            copy_button(
                message["content"],
                f"{active_chat['id']}_{index}"
            )


# =========================================================
# 12. REGENERATE LAST RESPONSE
# =========================================================

if (
    active_chat["messages"]
    and active_chat["messages"][-1]["role"] == "assistant"
):

    if st.button("🔄 Regenerate response"):

        active_chat["messages"].pop()

        save_chat_data()

        try:

            with st.spinner("Generating a new response..."):

                answer = generate_ai_response(
                    messages=active_chat["messages"],
                    model=st.session_state.selected_model,
                    system_prompt=st.session_state.system_prompt,
                    temperature=st.session_state.temperature,
                    max_tokens=st.session_state.max_tokens
                )

            active_chat["messages"].append({
                "role": "assistant",
                "content": answer
            })

            active_chat["updated_at"] = get_current_time()

            save_chat_data()

            st.rerun()

        except Exception as error:

            st.error(f"Unable to regenerate response: {error}")


# =========================================================
# 13. CHAT INPUT
# =========================================================

prompt = st.chat_input(
    "Message Local AI...",
    disabled=not bool(available_models)
)


# =========================================================
# 14. GENERATE AI RESPONSE
# =========================================================

if prompt:

    active_chat["messages"].append({
        "role": "user",
        "content": prompt
    })

    update_chat_title(active_chat, prompt)

    active_chat["updated_at"] = get_current_time()

    save_chat_data()

    with st.chat_message("user"):

        st.markdown(prompt)

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

            copy_button(
                answer,
                f"{active_chat['id']}_new"
            )

        active_chat["messages"].append({
            "role": "assistant",
            "content": answer
        })

        active_chat["updated_at"] = get_current_time()

        save_chat_data()

    except Exception as error:

        st.error(
            f"Unable to generate a response: {error}"
        )

        st.info(
            "Check whether Ollama is running and the selected model is installed."
        )
