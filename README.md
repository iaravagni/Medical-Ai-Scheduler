# Medical-AI-Scheduler

## Overview
Medical-AI-Scheduler is an intelligent appointment scheduling system designed for healthcare facilities. It leverages artificial intelligence to optimize appointment scheduling, reduce wait times, and improve resource allocation in medical settings.

## Features
- AI-powered appointment scheduling
- Patient priority management
- Resource optimization for medical staff and equipment
- Automated reminders and notifications
- Integration with electronic health records
- Analytics dashboard for operational insights

## Installation

```bash
# Clone the repository
git clone https://github.com/iaravagni/Medical-Ai-Scheduler.git

# Navigate to the project directory
cd Medical-Ai-Scheduler

# Install dependencies
pip install -r requirements.txt
```

## Configuration
Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=your_database_connection_string
API_KEY=your_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
BEDROCK_MODEL_ID=anthropic.claude-v2
```

## Usage
```bash
# Start the application
python app.py
```

<!-- Access the web interface at `http://localhost:5000` -->

<!-- ## API Documentation
The API endpoints are available at `/api/v1/`:

- `GET /api/v1/appointments` - List all appointments
- `POST /api/v1/appointments` - Create a new appointment
- `GET /api/v1/appointments/{id}` - Get appointment details
- `PUT /api/v1/appointments/{id}` - Update an appointment
- `DELETE /api/v1/appointments/{id}` - Cancel an appointment -->

## Amazon Bedrock Integration

### Overview
This application leverages Amazon Bedrock to provide intelligent scheduling recommendations and natural language processing capabilities for patient communications.

### Setup Requirements
1. AWS account with access to Amazon Bedrock service
2. IAM role with appropriate permissions for Bedrock API access
3. AWS SDK for Python (Boto3) installed

### Configuration
Add the following to your `.env` file:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_aws_region
BEDROCK_MODEL_ID=anthropic.claude-v2 # or your preferred model
```

## Orchestration

- **LLM Orchestration Function**
  - A robust `orchestrated_llm_call()` pipeline was implemented with logging, error handling, retry logic (via `tenacity`), and context saving.

- **Logging**
  - Logs are stored in a dedicated `/logs/orchestration.log` file with timestamps and clear labels for:
    - Pipeline start
    - LLM call attempts
    - Success or failure messages
    - Context save status
    - Total runtime

- **Context Management**
  - User conversation history, session details, and preferences are stored in a JSON file after every interaction (e.g., `medical_session_<timestamp>.json`).
  - This supports session continuity and reproducibility.

- **Error Handling**
  - Wrapped the LLM call in a retry mechanism (`tenacity`) to handle transient failures.
  - Logged meaningful error messages for easier debugging.

## Enterprise Integration

To support real-world enterprise needs, the Medical-AI-Scheduler has been extended with components that ensure security, scalability, and operational transparency. A secure chat interface allows authenticated users to interact with the AI scheduling assistant while maintaining individual session context. Each session is tracked with a unique identifier, and user data is stored securely.

All interactions—such as user queries and AI responses—are logged to dedicated audit logs, enabling traceability and compliance with institutional standards. Additionally, orchestration performance metrics such as execution time and error reporting are captured in a separate log to support performance analysis and system monitoring.

The system is modular and deployment-ready. Environment-based configuration and clear separation between logic and orchestration make it easy to launch and maintain. A deployment guide is included as part of the project documentation to assist with setup and integration into existing infrastructures. Security documentation outlines the basic authentication mechanism and logging safeguards in place.

## Security Architecture: Medical Appointment Chatbot

### #Authentication
- Users authenticate via username/password (hashed with SHA-256).
- Session management includes 30-min timeout and role-based access.

### Encryption
- User data (`users.json`) is encrypted using AES with Fernet.
- Secrets stored securely in `secret.key`.

### Privacy Controls
- Users must provide explicit consent before interacting with the chatbot.
- Option to delete stored conversation data.

### Audit System
- Logs stored in `logs/audit.log` include login events and user actions.
- LLM request logs saved in `logs/orchestration.log`.

### Admin Controls
- Admins can create/delete users and view logs.


## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
Project Link: [https://github.com/iaravagni/Medical-Ai-Scheduler](https://github.com/iaravagni/Medical-Ai-Scheduler)