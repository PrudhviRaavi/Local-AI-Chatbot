
import streamlit as st
import ollama

# 1. Page configuration
st.set_page_config(
    page_title="Local AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# 2. System prompt: Defines AI behavior
SYSTEM_PROMPT = """
You are a helpful, friendly and intelligent AI assistant.

Your responsibilities:

1. Answer general questions accurately and clearly.
2. Explain technical concepts in simple language.
3. Write clean, readable and properly formatted code.
4. Use Markdown code blocks with the correct language.
5. Explain code step by step whenever requested.
6. Help debug errors and suggest practical solutions.
7. Maintain context from previous messages in the conversation.
8. Keep simple answers concise and provide detail when necessary.
9. Never invent facts, personal information or capabilities.
10. If you are unsure about something, say so honestly.

For programming questions:
- Provide working code.
- Use meaningful variable names.
- Follow good programming practices.
- Explain important logic clearly.
- Include examples when useful.

Your tone should be friendly, natural and professional.
"""

# 3. Application heading
st.title("🤖 Local AI Chatbot")
st.caption("Your personal AI assistant · Powered by Qwen 3 1.7B")

# 4. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat input
if prompt := st.chat_input("Ask me anything..."):

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # 7. Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                response = ollama.chat(
                    model="qwen3:1.7b",
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        *st.session_state.messages
                    ]
                )

                answer = response["message"]["content"]

                st.markdown(answer)

                # Save assistant response
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Error connecting to Ollama: {e}")
