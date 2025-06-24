## Security Measures

### Infrastructure Security

#### Network Security
- **Firewall Configuration**: UFW enabled with restricted access
- **Port Management**: Only necessary ports (22, 80, 443) exposed
- **SSL/TLS Encryption**: Full HTTPS encryption with TLS 1.2+ protocols
- **DDoS Protection**: Rate limiting and connection throttling

#### Server Hardening
```bash
# System hardening checklist
# 1. Disable root login
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# 2. Configure SSH key-only authentication
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# 3. Install fail2ban for intrusion prevention
sudo apt install -y fail2ban
sudo systemctl enable fail2ban

# 4. Configure automatic security updates
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

#### Application Security Architecture
```
Internet → AWS CloudFront/ALB → Streamlit App
                ↓
         Security Headers Applied
                ↓
         Authentication Layer
                ↓
         Encrypted Data Storage
```

### Authentication & Authorization

#### Multi-Layer Authentication
1. **Primary Authentication**: Username/password with SHA-256 hashing
2. **Session Management**: Time-based session expiration (30 minutes)
3. **Access Control**: Role-based permissions (admin/user)
4. **Audit Logging**: All authentication attempts logged

#### Password Security Policy
```python
# Password requirements (implement in production)
PASSWORD_POLICY = {
    'min_length': 12,
    'require_uppercase': True,
    'require_lowercase': True,
    'require_numbers': True,
    'require_special_chars': True,
    'max_attempts': 3,
    'lockout_duration': 900  # 15 minutes
}
```

#### Session Security
```python
# Session configuration
SESSION_CONFIG = {
    'timeout_minutes': 30,
    'secure_cookies': True,
    'httponly_cookies': True,
    'samesite': 'Strict',
    'session_token_rotation': True
}
```

### Data Protection

#### Encryption Standards
- **At Rest**: Fernet (AES 128/256) for user data and conversations
- **In Transit**: TLS 1.3 for all communications
- **Key Management**: Secure key generation and storage
- **Database**: JSON files with field-level encryption

#### Data Classification
```
[HIGHLY SENSITIVE]
- User passwords (hashed)
- Personal health information
- Session tokens

[SENSITIVE]
- Conversation history
- Appointment details
- User preferences

[INTERNAL]
- System logs
- Performance metrics
- Error logs
```

#### Backup Security
```bash
# Encrypted backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/ubuntu/secure-backups"
APP_DIR="/home/ubuntu/medical-assistant"

# Create encrypted backup
tar -czf - -C $APP_DIR data/ users.json secret.key logs/ | \
gpg --symmetric --cipher-algo AES256 --compress-algo 1 --s2k-mode 3 \
--s2k-digest-algo SHA512 --s2k-count 65536 --force-mdc \
--output $BACKUP_DIR/backup-$DATE.tar.gz.gpg
```

### Vulnerability Management

#### Security Scanning
```bash
# Automated security checks
#!/bin/bash
echo "=== Security Audit Report ===" > security-audit.log
echo "Date: $(date)" >> security-audit.log

# Check for outdated packages
echo "\n1. Package Vulnerabilities:" >> security-audit.log
sudo apt list --upgradable 2>/dev/null | grep -i security >> security-audit.log

# Check open ports
echo "\n2. Open Ports:" >> security-audit.log
sudo netstat -tlnp >> security-audit.log

# Check failed login attempts
echo "\n3. Failed Login Attempts:" >> security-audit.log
grep "Failed password" /var/log/auth.log | tail -10 >> security-audit.log

# Check file permissions
echo "\n4. Critical File Permissions:" >> security-audit.log
ls -la /home/ubuntu/medical-assistant/secret.key >> security-audit.log
ls -la /home/ubuntu/medical-assistant/.env >> security-audit.log
```

#### Dependency Management
```bash
# Security dependency checking
pip-audit --requirement requirements.txt --format json --output security-report.json

# Update vulnerable packages
pip install --upgrade $(pip-audit --requirement requirements.txt --format=columns --output /dev/stdout | awk 'NR>2 {print $1}' | uniq)
```

---

## Privacy Controls

### Data Minimization

#### Collection Principles
- **Purpose Limitation**: Only collect data necessary for appointment scheduling
- **Storage Limitation**: Automatic data purging after retention period
- **Processing Transparency**: Clear documentation of data usage
- **User Control**: Easy data deletion and export options

#### Data Inventory
```python
# Data retention policy
DATA_RETENTION = {
    'conversation_history': 90,      # days
    'appointment_records': 365,      # days
    'audit_logs': 2555,             # 7 years (compliance)
    'error_logs': 30,               # days
    'session_data': 1               # days
}
```

### User Rights Management

#### GDPR Compliance Features
```python
# User rights implementation
class PrivacyControls:
    def request_data_export(self, username):
        """Export all user data in JSON format"""
        user_data = {
            'appointments': self.get_user_appointments(username),
            'conversations': self.get_conversation_history(username),
            'preferences': self.get_user_preferences(username),
            'audit_trail': self.get_user_audit_logs(username)
        }
        return json.dumps(user_data, indent=2)
    
    def delete_user_data(self, username):
        """Permanently delete all user data"""
        self.clear_appointments(username)
        self.clear_conversations(username)
        self.clear_preferences(username)
        self.anonymize_audit_logs(username)
    
    def data_portability(self, username, format='json'):
        """Export data in portable format"""
        # Implementation for data portability
        pass
```

#### Privacy Dashboard
```python
# User privacy controls in UI
PRIVACY_CONTROLS = {
    'view_data': "See all data we have about you",
    'export_data': "Download your data",
    'delete_data': "Permanently delete your account and data",
    'modify_consent': "Change your privacy preferences",
    'audit_access': "See who accessed your data and when"
}
```

### Data Processing Transparency

#### Processing Activities Record
```
PURPOSE: Medical appointment scheduling
LEGAL BASIS: Consent (GDPR Article 6(1)(a))
DATA CATEGORIES: 
- Identity data (username, display name)
- Contact data (appointment preferences)
- Health data (appointment types, basic health queries)
RECIPIENTS: None (data not shared)
TRANSFERS: None (local processing only)
RETENTION: See data retention policy
```

#### Privacy Notice Template
```markdown
## Privacy Notice - Medical Assistant

### What We Collect
- Account information (username, encrypted password)
- Conversation history (for session continuity)
- Appointment bookings (date, time, type)
- Usage logs (for security and improvement)

### How We Use It
- Provide appointment scheduling services
- Maintain conversation context
- Security monitoring and audit compliance
- System performance optimization

### Your Rights
- Access your data
- Correct inaccurate data
- Delete your data
- Export your data
- Withdraw consent

### Contact
Data Protection Officer: [your-dpo@company.com]
```