# Medical Appointment Assistant

A secure, AI-powered medical appointment scheduling system built with Streamlit and AWS Bedrock (Claude). This application provides an intelligent chatbot interface for scheduling medical appointments while maintaining strict privacy and security standards.

-- [Demo Video][https://youtu.be/RgrGfa-4Shk]

## 🚀 Features

- **Intelligent Chat Interface**: Natural language appointment scheduling using Claude AI
- **Secure Authentication**: Encrypted user management with session control
- **Appointment Management**: 30-minute time slots from 10:00 AM to 4:00 PM (weekdays)
- **Privacy-First Design**: Local data storage with encryption
- **Audit Logging**: Comprehensive activity tracking
- **Responsive UI**: Modern Streamlit-based web interface
- **General Health Info**: Basic health information queries (non-diagnostic)

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Usage](#usage)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/iaravagni/Medical-Ai-Scheduler
   cd medical-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate encryption key**
   ```bash
   python generate_key.py
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your AWS credentials
   ```

6. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

7. **Access the application**
   - Open http://localhost:8501
   - Default login: `admin` / `admin123`

## 📦 Installation

### System Requirements

- **Memory**: 4GB RAM minimum
- **Storage**: 10GB available space
- **Python**: 3.8 or higher
- **OS**: Linux (Ubuntu 22.04+ recommended), macOS, or Windows

### Dependencies

```bash
# Core dependencies
streamlit>=1.28.0
boto3>=1.34.0
cryptography>=41.0.0
python-dotenv>=1.0.0

# Development dependencies
pytest>=7.4.0
pytest-mock>=3.11.0
black>=23.7.0
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
BEDROCK_MODEL_ID=us.anthropic.claude-3-haiku-20240307-v1:0
```

### AWS Bedrock Setup

1. **Enable Model Access**
   - Go to AWS Console → Amazon Bedrock
   - Navigate to "Model Access"
   - Request access to Anthropic Claude models
   - Wait for approval (24-48 hours)

2. **IAM Permissions**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "bedrock:InvokeModel",
           "bedrock:ListFoundationModels"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

## 🚀 Deployment

### AWS EC2 Deployment

1. **Launch EC2 Instance**
   - Instance Type: t2.medium or higher
   - OS: Ubuntu 22.04 LTS
   - Storage: 10GB+ EBS volume

2. **Security Group Configuration**
   ```
   SSH (22) - Your IP only
   HTTP (80) - 0.0.0.0/0
   HTTPS (443) - 0.0.0.0/0
   Custom TCP (8501) - 0.0.0.0/0
   ```

3. **Server Setup**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install dependencies
   sudo apt install -y python3 python3-pip python3-venv git nginx
   
   # Clone and setup application
   git clone https://github.com/iaravagni/Medical-Ai-Scheduler
   cd Medical-Ai-Scheduler
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## 💻 Usage

### First-Time Setup

1. **Access the Application**
   - Navigate to your deployment URL
   - Use default credentials: `admin` / `admin123`

2. **Change Default Password**
   - Contact system administrator for password changes
   - Default passwords should be changed immediately

3. **Grant Consent**
   - Click "I consent to use this chatbot for scheduling purposes only"

### Scheduling Appointments

```
User: I need to schedule an appointment for next Friday at 2 PM
Assistant: I can help you schedule that appointment. Let me check availability for 2:00 PM...

User: I need a cardiology consultation
Assistant: I've scheduled your cardiology appointment for 2024-12-20 at 14:00.
📅 Appointment booked on 2024-12-20 at 14:00.
```

### Available Time Slots

- **Days**: Monday - Friday (weekdays only)
- **Hours**: 10:00 AM - 4:00 PM
- **Duration**: 30-minute slots
- **Booking**: Real-time availability checking

### Quick Actions

- **Schedule Appointment**: Start booking process
- **View Appointments**: See all your bookings
- **General Health Info**: Get health information
- **Clear Conversation**: Reset chat history
- **Delete My Data**: Remove all personal data

## 🏗️ Architecture

### System Components

```
medical-assistant/
├── chatbot/
│   ├── calendar_utils.py   # Appointment logic
│   ├── conversation.py     # LLM integration
│   ├── memory.py           # Session management
│   └── orchestrator.py     # Request handling
├── streamlit_app.py        # Web interface
├── generate_key.py         # Encryption setup
├── data/
│   └── calendar.json       # Appointment storage
├── logs/
│   ├── audit.log          # User activity
│   └── orchestration.log  # System logs
└── users.json             # Encrypted user data
```

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.8+
- **AI**: AWS Bedrock (Claude)
- **Authentication**: Custom hash-based system
- **Encryption**: Fernet (symmetric encryption)
- **Storage**: JSON files (local)
- **Logging**: Python logging module

## 🔒 Security

### Security Features

- **Encryption**: AES-256 for all user data
- **Authentication**: SHA-256 password hashing
- **Session Management**: 30-minute timeout
- **Audit Logging**: All activities tracked
- **HTTPS**: TLS 1.3 encryption in transit
- **Input Validation**: Comprehensive input sanitization

### Data Protection

- **Local Storage**: No external data sharing
- **Privacy Controls**: User data deletion available
- **Compliance**: GDPR and HIPAA considerations
- **Access Control**: Role-based permissions
- **Backup Security**: Encrypted backups

### Best Practices

1. **Change default passwords immediately**
2. **Use strong, unique passwords**
3. **Enable HTTPS in production**
4. **Regular security updates**
5. **Monitor audit logs**
6. **Implement proper backup procedures**

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-mock

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_bedrock_llm.py
```

## 📊 Monitoring

### Log Files

- **Audit Log**: `logs/audit.log` - User activities
- **System Log**: `logs/orchestration.log` - Application events
- **Error Log**: Available via systemd journal

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Run tests**
   ```bash
   pytest
   ```

5. **Submit pull request**

### Code Standards

- **Python**: Follow PEP 8 style guide
- **Formatting**: Use Black code formatter
- **Testing**: Write tests for new features
- **Documentation**: Update docs for changes

### Pull Request Process

1. Update documentation for any changes
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## 🐛 Troubleshooting

### Common Issues

**Login Problems**
```bash
# Check user file
cat users.json
# Verify encryption key exists
ls -la secret.key
```

**Service Won't Start**
```bash
# Check service logs
sudo journalctl -u medical-assistant --no-pager -l
# Verify port availability
sudo netstat -tlnp | grep :8501
```

**AWS Connection Issues**
```bash
# Test AWS credentials
aws bedrock list-foundation-models --region us-east-1
# Check model access
aws bedrock get-model-invocation-logging-configuration
```


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic**: For providing Claude AI models
- **AWS**: For Bedrock AI platform
- **Streamlit**: For the web framework
- **Community**: For testing and feedback

---

⚠️ **Important**: This system is for appointment scheduling only and should not be used for medical emergencies or clinical decision-making.