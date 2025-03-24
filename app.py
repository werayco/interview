import os
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq


groq_api_key = st.secrets["GROQ_API_KEY"]

# Initialize chatbot
chat_bot = ChatGroq(model="gemma2-9b-it", api_key=groq_api_key, temperature=0.5, max_tokens=500)

# Streamlit UI
st.set_page_config(page_title="AI Interview Assistant", layout="wide")

st.title("🎤 AI Interview Assistant")
st.subheader("Ask AI interview-related questions and get instant responses!")

# Sidebar for user input
users_role = st.sidebar.text_input("Enter your job role", value="Software Engineer")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask your interview question...")

if user_input:
    # Store user message in chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate AI response
    template = """
    You are an AI assistant helping with interview preparation.
    The user's job role/title is {users_role}.

    The user will ask you interview-related questions, and you are to provide a detailed answer.
    Here is the user's question: "{user_response}"
    """
    
    prompt = ChatPromptTemplate.from_template(template).format(users_role=users_role, user_response=user_input)
    response = chat_bot.invoke(prompt).content

    # Store AI response in chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(response)
