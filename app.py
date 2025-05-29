import streamlit as st
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from chatbot.conversation import call_llm
from chatbot.memory import init_context, get_conversation_summary, clear_context, save_context_to_file

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Medical Assistant", 
    layout="centered",
    page_icon="🩺"
)

class SimpleAuth:
    def __init__(self):
        self.users_file = Path("users.json")
        self.load_users()
    
    def load_users(self):
        """Load users from file or create default admin"""
        try:
            if self.users_file.exists():
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            else:
                # Create default admin user
                self.users = {
                    "admin": {
                        "password": self.hash_password("admin123"),
                        "name": "Administrator"
                    }
                }
                self.save_users()
        except Exception as e:
            st.error(f"Error loading users: {e}")
            # Fallback to default admin
            self.users = {
                "admin": {
                    "password": self.hash_password("admin123"),
                    "name": "Administrator"
                }
            }
    
    def save_users(self):
        """Save users to file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            st.error(f"Error saving users: {e}")
    
    def hash_password(self, password):
        """Simple password hashing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username, password):
        """Check if username/password is valid"""
        if username in self.users:
            return self.users[username]["password"] == self.hash_password(password)
        return False
    
    def get_user_name(self, username):
        """Get user's display name"""
        return self.users.get(username, {}).get("name", username)

    def create_user(self, username, password, name):
        """Create a new user"""
        try:
            if username in self.users:
                return False, "Username already exists"
            
            self.users[username] = {
                "password": self.hash_password(password),
                "name": name
            }
            self.save_users()
            return True, "User created successfully"
        except Exception as e:
            return False, f"Error creating user: {e}"
    
    def delete_user(self, username):
        """Delete a user (except admin)"""
        try:
            if username == "admin":
                return False, "Cannot delete admin user"
            if username not in self.users:
                return False, "User not found"
            
            del self.users[username]
            self.save_users()
            return True, "User deleted successfully"
        except Exception as e:
            return False, f"Error deleting user: {e}"

# Initialize auth system - Fixed caching issue
def get_auth():
    """Get or create auth instance without caching to avoid issues"""
    if 'auth_instance' not in st.session_state:
        st.session_state.auth_instance = SimpleAuth()
    return st.session_state.auth_instance

def login_form():
    """Simple login form"""
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
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please enter both username and password")
    
    st.info("**Default Login:** Username: `admin`, Password: `admin123`")

def show_user_management():
    """Admin panel for creating new users"""
    st.markdown("## 👥 User Management")
    
    # Create new user section
    st.markdown("### Create New User")
    with st.form("create_user"):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        new_name = st.text_input("Full Name")
        
        if st.form_submit_button("Create User"):
            if new_username and new_password and new_name:
                auth = get_auth()
                success, message = auth.create_user(new_username, new_password, new_name)
                if success:
                    st.success(message)
                    # Force refresh of auth instance to reflect changes
                    st.session_state.auth_instance = SimpleAuth()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all fields")
    
    # Back button
    if st.button("← Back to Chat", key="back_to_chat_from_summary"):
        st.session_state.show_admin = False
        st.rerun()

def show_user_list():
    """Show list of all users"""
    st.markdown("## 👥 Current Users")
    
    auth = get_auth()
    
    if hasattr(auth, 'users') and auth.users:
        for username, user_data in auth.users.items():
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.text(f"👤 {username}")
            with col2:
                st.text(user_data.get("name", ""))
            with col3:
                if username != "admin" and st.button(f"🗑️", key=f"delete_{username}"):
                    success, message = auth.delete_user(username)
                    if success:
                        st.success(message)
                        # Force refresh of auth instance to reflect changes
                        st.session_state.auth_instance = SimpleAuth()
                        st.rerun()
                    else:
                        st.error(message)
    else:
        st.warning("No users found or error loading users.")
    
    # Back button
    if st.button("← Back to Chat", key="back_to_chat_from_user_list"):
        st.session_state.show_users = False
        st.rerun()

def check_session():
    """Check if user is logged in and session is valid"""
    if not st.session_state.get("authenticated"):
        return False
    
    # Check session timeout (30 minutes)
    if st.session_state.get("login_time"):
        if datetime.now() - st.session_state.login_time > timedelta(minutes=30):
            st.error("Session expired. Please log in again.")
            # Clear session
            for key in ["authenticated", "username", "user_name", "login_time"]:
                if key in st.session_state:
                    del st.session_state[key]
            return False
    
    return True

def main_app():
    """Your original app with minimal changes"""
    
    # Check authentication first
    if not check_session():
        login_form()
        return
    
    st.title("🩺 Medical Appointment Assistant")
    
    # Initialize context
    if "context" not in st.session_state:
        st.session_state.context = init_context()

    # Sidebar for additional features
    with st.sidebar:
        st.header(f"**Welcome, {st.session_state.user_name}!**")
        
        col1 = st.container()
        with col1:
            if st.button("🚪 Logout", use_container_width=True):
                # Clear session
                for key in list(st.session_state.keys()):
                    if key in ["authenticated", "username", "user_name", "login_time"]:
                        del st.session_state[key]
                st.rerun()
            
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
    
            # Admin panel (only for admin user)
            if st.session_state.username == "admin":
                st.markdown("---")
                st.header("👨‍💼 Admin Panel")
                
                if st.button("👥 Manage Users", use_container_width=True):
                    st.session_state.show_admin = True
                    st.rerun()
                
                if st.button("📊 View Users", use_container_width=True):
                    st.session_state.show_users = True
                    st.rerun()

    # Handle admin panel display
    if st.session_state.get("show_admin"):
        show_user_management()
        return
    
    if st.session_state.get("show_users"):
        show_user_list()
        return

    # Main chat interface
    st.markdown("### Chat with your Medical Assistant")

    # Display conversation history
    if st.session_state.context.get('conversation_history'):
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
            placeholder="e.g., 'Schedule an appointment for tomorrow at 3PM'",
            key="user_input_field",
            value="" if st.session_state.message_sent else st.session_state.get("user_input_field", "")
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add space to align button
        send_button = st.button("Send", type="primary")

    # Process input only when send button is clicked
    if send_button and user_input:
        with st.spinner("Thinking..."):
            try:
                response, updated_context = call_llm(user_input, st.session_state.context)
                st.session_state.context = updated_context
            except Exception as e:
                st.error(f"Error processing your request: {e}")
        
        # Set flag to clear input on next run
        st.session_state.message_sent = True
        st.rerun()

    # Reset the message sent flag after rerun
    if st.session_state.message_sent:
        st.session_state.message_sent = False

    # Footer
    st.markdown("---")
    st.markdown("*💡 Tip: This assistant can help with appointment scheduling and general health information. For medical emergencies, please contact your healthcare provider or emergency services.*")

if __name__ == "__main__":
    main_app()