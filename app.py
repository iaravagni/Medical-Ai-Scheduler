import streamlit as st
from chatbot.conversation import call_llm
from chatbot.memory import init_context, get_conversation_summary, clear_context, save_context_to_file

st.set_page_config(
    page_title="Medical Assistant", 
    layout="centered",
    page_icon="🩺"
)

st.title("🩺 Medical Appointment Assistant")

# Initialize context
if "context" not in st.session_state:
    st.session_state.context = init_context()

# Sidebar for additional features
with st.sidebar:
    st.header("Session Options")

    # Use consistent width for all buttons using container and layout
    col1 = st.container()
    with col1:
        if st.button("ℹ️ General Health Info", use_container_width=True):
            response, updated_context = call_llm("Can you provide some general health information?", st.session_state.context)
            st.session_state.context = updated_context
            st.rerun()

        if st.button("📅 Schedule Appointment", use_container_width=True):
            response, updated_context = call_llm("I'd like to schedule an appointment", st.session_state.context)
            st.session_state.context = updated_context
            st.rerun()

        if st.button("📋 View My Appointments", use_container_width=True):
            response, updated_context = call_llm("Show me my scheduled appointments", st.session_state.context)
            st.session_state.context = updated_context
            st.rerun()

        if st.button("🧹 Clear Conversation", use_container_width=True):
            st.session_state.context = clear_context(st.session_state.context)
            st.success("Conversation cleared!")
            st.rerun()


# Main chat interface
st.markdown("### Chat with your Medical Assistant")

# Display conversation history
if st.session_state.context.get('conversation_history'):
    st.markdown("**Conversation History:**")
    for message in st.session_state.context['conversation_history'][-6:]:  # Show last 6 messages
        if message['role'] == 'user':
            st.markdown(f"**👤 You:** {message['content']}")
        else:
            st.markdown(f"**🩺 Assistant:** {message['content']}")
    st.markdown("---")

# Initialize message sent flag
if "message_sent" not in st.session_state:
    st.session_state.message_sent = False

# User input with send button
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Ask me something:", 
        placeholder="e.g., 'Schedule an appointment for tomorrow at 3PM' or 'What should I know about my blood test?'",
        key="user_input_field",
        value="" if st.session_state.message_sent else st.session_state.get("user_input_field", "")
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Add space to align button
    send_button = st.button("Send", type="primary")

# Process input only when send button is clicked
if send_button and user_input:
    with st.spinner("Thinking..."):
        response, updated_context = call_llm(user_input, st.session_state.context)
        st.session_state.context = updated_context
    
    # Set flag to clear input on next run
    st.session_state.message_sent = True
    st.rerun()

# Reset the message sent flag after rerun
if st.session_state.message_sent:
    st.session_state.message_sent = False

# Footer
st.markdown("---")
st.markdown("*💡 Tip: This assistant can help with appointment scheduling and general health information. For medical emergencies, please contact your healthcare provider or emergency services.*")