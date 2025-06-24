# 🩺 Medical Appointment Assistant – Technical Documentation

## 🏗️ Architecture Overview

The **Medical Appointment Assistant** is a Streamlit-based web application designed to intelligently schedule medical appointments using AWS Bedrock (Claude). The system is built with a **modular architecture**, ensuring scalability and clear separation of concerns.

---

## 📦 System Components

```
medical-assistant/
├── chatbot/
│   ├── calendar_utils.py    # Appointment scheduling
│   ├── memory.py            # Session management
│   ├── conversation.py      # Core LLM integration
│   └── orchestrator.py      # Request orchestration
├── streamlit_app.py         # Web interface
├── generate_key.py          # Encryption key generation
├── data/
│   └── calendar.json        # Appointment storage
├── logs/
│   ├── audit.log            # User activity logs
│   └── orchestration.log    # System logs
├── users.json               # Encrypted user data
└── secret.key               # Encryption key
```

---

## 🧰 Core Technologies

| Layer         | Technology                      |
|---------------|----------------------------------|
| Frontend      | [Streamlit](https://streamlit.io) (Python web framework) |
| Backend       | Python 3.8+                      |
| LLM           | AWS Bedrock (Claude)             |
| Authentication| Custom hash-based system         |
| Encryption    | Fernet (Symmetric encryption)    |
| Data Storage  | JSON files                       |
| Logging       | Python's `logging` module        |
| Testing       | `pytest` with mocking            |

---

## 🧠 Key Classes and Modules

### 🔹 `BedrockLLM` Class
**Purpose:** Interfaces with AWS Bedrock to generate intelligent responses.

**Key Methods:**
- `generate_response()`: Sends user input to Claude and returns a response.
- Handles:
  - API failure gracefully
  - Temperature and token limit configurations

---

### 🔐 `SimpleAuth` Class
**Purpose:** Manages user authentication and session state.

**Features:**
- SHA-256 password hashing
- Encrypted storage using Fernet
- Session timeouts and user CRUD operations

---

### 📅 Calendar Management

**Purpose:** Handles all appointment-related logic.

**Features:**
- 30-minute time slots (from 10:00 AM to 4:00 PM)
- Conflict detection and validation
- User-specific tracking of scheduled slots
- Persistent storage via JSON

---

## 📄 Data Models

### 🧾 Context Structure

```python
{
    'conversation_history': [
        {'role': 'user', 'content': 'string'},
        {'role': 'assistant', 'content': 'string'}
    ],
    'session_start': datetime,
    'appointments': [
        {
            'request': 'string',
            'scheduled_for': 'YYYY-MM-DD HH:MM',
            'status': 'booked|failed',
            'response': 'string'
        }
    ],
    'user_preferences': {},
    'session_id': 'string'
}
```

---

### 👤 User Structure

```python
{
    'username': {
        'password': 'hashed_password',
        'name': 'display_name'
    }
}
```

---

## 🔒 Security Features

- **Encryption:** All user data is encrypted using `Fernet`.
- **Password Hashing:** SHA-256 with salting to protect credentials.
- **Session Management:** Inactivity timeout set to 30 minutes.
- **Audit Logging:** All user actions are recorded in `audit.log`.
- **Data Privacy:** No external databases; all data stored locally in JSON.

---

## ⚠️ Error Handling

| Area            | Handling Strategy                                     |
|------------------|--------------------------------------------------------|
| API Failures     | Graceful fallback with user-friendly error messages    |
| Network Issues   | Retry logic with exponential backoff                   |
| File I/O Errors  | Defaults loaded when data files are unavailable        |
| Authentication   | Secure error feedback without revealing sensitive info |

---

## ✅ Summary

The Medical Appointment Assistant is a secure, intelligent, and modular web app for booking medical appointments. It brings together AWS Bedrock's LLM capabilities with robust Python tooling to create a reliable and user-friendly system.
