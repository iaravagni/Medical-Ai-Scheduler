from datetime import datetime
from typing import Dict, List

def init_context() -> Dict:
    """Initialize conversation context for new session"""
    return {
        'conversation_history': [],
        'session_start': datetime.now(),
        'appointments': [],
        'user_preferences': {},
        'last_interaction': None,
        'session_id': f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    }

def get_conversation_summary(context: Dict) -> str:
    """Get summary of current conversation"""
    history = context.get('conversation_history', [])
    if not history:
        return "No conversation history yet."
    
    summary = f"Conversation started: {context.get('session_start', 'Unknown')}\n"
    summary += f"Total messages: {len(history)}\n"
    
    if context.get('appointments'):
        summary += f"Appointments discussed: {len(context['appointments'])}\n"
    
    return summary

def clear_context(context: Dict) -> Dict:
    """Clear conversation history but keep session info"""
    new_context = init_context()
    new_context['session_start'] = context.get('session_start', datetime.now())
    new_context['user_preferences'] = context.get('user_preferences', {})
    return new_context

def save_context_to_file(context: Dict, filename: str = None) -> str:
    """Save context to JSON file"""
    import json
    
    if not filename:
        session_id = context.get('session_id', 'unknown')
        filename = f"medical_session_{session_id}.json"
    
    try:
        # Prepare data for JSON serialization
        save_data = context.copy()
        if 'session_start' in save_data:
            save_data['session_start'] = save_data['session_start'].isoformat()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        return f"Session saved to {filename}"
    except Exception as e:
        return f"Failed to save session: {str(e)}"