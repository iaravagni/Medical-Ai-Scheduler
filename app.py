import streamlit as st
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from chatbot.conversation import call_llm
from chatbot.memory import init_context, get_conversation_summary, clear_context, save_context_to_file
from chatbot.orchestrator import orchestrated_llm_call

# Page configuration
st.set_page_config(page_title="Medical Assistant", layout="centered", page_icon="🎺")

# Encryption utilities
def load_key():
    return open("secret.key", "rb").read()

def encrypt_data(data_str):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(data_str.encode()).decode()

def decrypt_data(data_str):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(data_str.encode()).decode()

class SimpleAuth:
    def __init__(self):
        self.users_file = Path("users.json")
        self.load_users()

    def load_users(self):
        try:
            if self.users_file.exists():
                with open(self.users_file, 'r') as f:
                    encrypted = f.read()
                    decrypted = decrypt_data(encrypted)
                    self.users = json.loads(decrypted)
            else:
                self.users = {"admin": {"password": self.hash_password("admin123"), "name": "Administrator"}}
                self.save_users()
        except Exception as e:
            st.error(f"Error loading users: {e}")
            self.users = {"admin": {"password": self.hash_password("admin123"), "name": "Administrator"}}

    def save_users(self):
        try:
            encrypted = encrypt_data(json.dumps(self.users, indent=2))
            with open(self.users_file, 'w') as f:
                f.write(encrypted)
        except Exception as e:
            st.error(f"Error saving users: {e}")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username, password):
        if username in self.users:
            return self.users[username]["password"] == self.hash_password(password)
        return False

    def get_user_name(self, username):
        return self.users.get(username, {}).get("name", username)

    def create_user(self, username, password, name):
        if username in self.users:
            return False, "Username already exists"
        self.users[username] = {"password": self.hash_password(password), "name": name}
        self.save_users()
        return True, "User created successfully"

    def delete_user(self, username):
        if username == "admin":
            return False, "Cannot delete admin user"
        if username not in self.users:
            return False, "User not found"
        del self.users[username]
        self.save_users()
        return True, "User deleted successfully"

def get_auth():
    if 'auth_instance' not in st.session_state:
        st.session_state.auth_instance = SimpleAuth()
    return st.session_state.auth_instance

def login_form():
    st.markdown("## 🔐 Medical Assistant - Login")
    st.markdown("Please log in to continue")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", type="primary")
        if submit:
            if username and password:
                auth = get_auth()
                if auth.authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_name = auth.get_user_name(username)
                    st.session_state.login_time = datetime.now()
                    with open("logs/audit.log", "a") as log:
                        log.write(f"{datetime.now()} - LOGIN - {username}\n")
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please enter both username and password")
    st.info("**Default Login:** Username: `admin`, Password: `admin123`")

def check_consent():
    if "consent_given" not in st.session_state:
        st.markdown("### 📜 Consent to Proceed")
        if st.button("I consent to use this chatbot for scheduling purposes only"):
            st.session_state.consent_given = True
            st.rerun()
        else:
            st.stop()

def check_session():
    if not st.session_state.get("authenticated"):
        return False
    if st.session_state.get("login_time"):
        if datetime.now() - st.session_state.login_time > timedelta(minutes=30):
            st.error("Session expired. Please log in again.")
            for key in ["authenticated", "username", "user_name", "login_time"]:
                if key in st.session_state:
                    del st.session_state[key]
            return False
    return True

def main_app():
    if not check_session():
        login_form()
        return

    check_consent()
    st.title("🩺 Medical Appointment Assistant")

    if "context" not in st.session_state:
        st.session_state.context = init_context()

    with st.sidebar:
        st.header(f"**Welcome, {st.session_state.user_name}!**")
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                if key in ["authenticated", "username", "user_name", "login_time"]:
                    del st.session_state[key]
            st.rerun()

        st.header("Session Options")
        if st.button("ℹ️ General Health Info"):
            with open("logs/audit.log", "a") as log:
                log.write(f"{datetime.now()} - ACTION - {st.session_state.username} requested health info\n")
            response, updated_context = orchestrated_llm_call("Can you provide some general health information?", st.session_state.context)
            st.session_state.context = updated_context
            st.rerun()

        if st.button("🗕️ Schedule Appointment"):
            with open("logs/audit.log", "a") as log:
                log.write(f"{datetime.now()} - ACTION - {st.session_state.username} requested appointment scheduling\n")
            response, updated_context = orchestrated_llm_call("I'd like to schedule an appointment", st.session_state.context)
            st.session_state.context = updated_context
            st.rerun()

        if st.button("📋 View My Appointments"):
            with open("logs/audit.log", "a") as log:
                log.write(f"{datetime.now()} - ACTION - {st.session_state.username} viewed appointments\n")
            response, updated_context = orchestrated_llm_call("Show me my scheduled appointments", st.session_state.context)
            st.session_state.context = updated_context
            st.rerun()

        if st.button("🧹 Clear Conversation"):
            st.session_state.context = clear_context(st.session_state.context)
            st.success("Conversation cleared!")
            st.rerun()

        if st.button("Delete My Data"):
            st.session_state.context = clear_context(st.session_state.context)
            st.success("Your conversation data has been deleted.")

    st.markdown("### Chat with your Medical Assistant")
    if st.session_state.context.get('conversation_history'):
        for message in st.session_state.context['conversation_history'][-6:]:
            if message['role'] == 'user':
                st.markdown(f"**👤 You:** {message['content']}")
            else:
                st.markdown(f"**🩺 Assistant:** {message['content']}")
        st.markdown("---")

    if "message_sent" not in st.session_state:
        st.session_state.message_sent = False

    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Ask me something:", placeholder="e.g., 'Schedule an appointment for tomorrow at 3PM'", key="user_input_field", value="" if st.session_state.message_sent else st.session_state.get("user_input_field", ""))
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        send_button = st.button("Send", type="primary")

    if send_button and user_input:
        with st.spinner("Thinking..."):
            try:
                response, updated_context = orchestrated_llm_call(user_input, st.session_state.context)
                st.session_state.context = updated_context
            except Exception as e:
                st.error(f"Error processing your request: {e}")
        st.session_state.message_sent = True
        st.rerun()

    if st.session_state.message_sent:
        st.session_state.message_sent = False

    st.markdown("---")
    st.markdown("*💡 Tip: This assistant can help with appointment scheduling and general health information. For medical emergencies, please contact your healthcare provider or emergency services.*")

if __name__ == "__main__":
    main_app()
