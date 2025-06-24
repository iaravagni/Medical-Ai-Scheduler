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


