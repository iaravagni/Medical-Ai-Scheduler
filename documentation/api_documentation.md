# 👩‍⚕️ Medical Appointment Assistant – User Manual

## 🚀 Getting Started

The Medical Appointment Assistant helps you schedule medical appointments and provides general health information through an intelligent chat interface.

### First-Time Access

#### Open the Application
- Navigate to the provided URL in your web browser.
- You'll see the login screen.

#### Default Login
- **Username:** `admin`
- **Password:** `admin123`
> 🔐 Important: Change this password immediately after first login.

#### Grant Consent
- Click **"I consent to use this chatbot for scheduling purposes only"** to confirm understanding of the system's purpose.

---

## 🖥️ Main Interface

### Dashboard Overview

- **Title Bar:** Displays "Medical Appointment Assistant"
- **Sidebar:** Contains user controls and quick actions
- **Chat Area:** Main conversation interface
- **Input Field:** Where you type your messages

### Sidebar Features

#### Welcome Section
- Displays your name
- Includes logout button

#### Quick Actions
- **General Health Info:** Get health-related info
- **Schedule Appointment:** Begin booking process
- **View My Appointments:** View all your bookings
- **Clear Conversation:** Reset the current session
- **Delete My Data:** Permanently remove your data

---

## 💬 Using the Chat Interface

### Starting a Conversation

1. Type your message in the input field
2. Click "Send" or press **Enter**
3. Wait for the assistant's reply
4. Continue the conversation naturally

### Example Conversations

#### Scheduling an Appointment
You: I need to schedule an appointment for next Friday at 2 PM
Assistant: Let me check availability for 2:00 PM. What type of appointment do you need?
You: I need a cardiology consultation
Assistant: I've scheduled your cardiology appointment for 2024-12-20 at 14:00.
📅 Appointment booked on 2024-12-20 at 14:00.

shell
Always show details

Copy

#### General Health Information
You: What are the symptoms of flu?
Assistant: Common flu symptoms include fever, body aches, fatigue, cough, sore throat, runny nose, and headaches...

markdown
Always show details

Copy

---

## 🗓️ Appointment Scheduling

### Available Time Slots
- **Hours:** 10:00 AM to 4:00 PM
- **Duration:** 30-minute slots
- **Days:** Monday through Friday

### Booking Process
1. **Request:** "I want to schedule an appointment"
2. **Specify Time:** Provide preferred date and time
3. **Confirmation:** System confirms availability
4. **Booking:** Appointment is automatically added

### Date and Time Formats
- **Dates:** "December 20, 2024" or "2024-12-20"
- **Times:** "2:00 PM" or "14:00"

### Viewing Your Appointments
- Click **"View My Appointments"** in the sidebar
- Appointments displayed in `"YYYY-MM-DD at HH:MM"` format

---

## 👤 Account Management

### Changing Your Password
> Currently, password changes must be done by an administrator.

### Session Management
- **Duration:** 30 minutes of inactivity
- **Auto-Logout:** System logs you out after timeout
- **Manual Logout:** Use "Logout" button in sidebar

### Data Privacy
- **Conversation History:** Stored locally during session
- **Appointments:** Saved to your personal calendar
- **Data Deletion:** Use "Delete My Data" button

---

## ✅ Best Practices

### Effective Communication
- Be Specific: Use exact dates and times
- Clear Requests: State needs clearly
- Follow Up: Ask for confirmation

#### Examples of Good Requests
- "Schedule a dermatology appointment for January 15th at 10:30 AM"
- "I need a follow-up appointment next Tuesday afternoon"
- "What appointments do I have next week?"

#### Examples to Avoid
- "Book something soon"
- "Sometime next week"
- "Cancel everything"

---

## 🧯 Troubleshooting

### Common Issues

#### Login Problems
- **Issue:** Can’t log in
- **Solution:** Check username/password, ensure Caps Lock is off

#### Session Expired
- **Issue:** "Session expired"
- **Solution:** Log in again (session lasts 30 minutes)

#### Appointment Conflicts
- **Issue:** "Time slot already taken"
- **Solution:** Choose another time or view available slots

#### No Response from Assistant
- **Issue:** No reply
- **Solution:** Check internet connection, refresh the page

### Error Messages

```python
"I apologize, but I'm experiencing technical difficulties"
# Try again later or contact admin

"Sorry, [time] on [date] is already taken"
# Choose a different time

"Invalid username or password"
# Verify credentials or contact admin