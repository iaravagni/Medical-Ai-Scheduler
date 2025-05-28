import streamlit as st
from chatbot.conversation import call_llm
from chatbot.memory import init_context

st.set_page_config(page_title="Medical Assistant", layout="centered")
st.title("🩺 Medical Appointment Assistant")

if "context" not in st.session_state:
    st.session_state.context = init_context()

user_input = st.text_input("Ask me something (e.g., 'Schedule an appointment for tomorrow at 3PM'):")

if user_input:
    response, updated_context = call_llm(user_input, st.session_state.context)
    st.session_state.context = updated_context
    st.markdown(f"**Assistant**: {response}")
