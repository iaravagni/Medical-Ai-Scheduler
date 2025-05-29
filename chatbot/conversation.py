import boto3
import json
import logging
from typing import Dict, List, Tuple

class BedrockLLM:
    def __init__(self, region_name: str = 'us-east-1'):
        """Initialize Bedrock client for Claude"""
        self.bedrock_client = boto3.client('bedrock-runtime', region_name=region_name)
        # Use inference profile instead of direct model ID
        self.model_id = "us.anthropic.claude-3-haiku-20240307-v1:0"
        self.max_tokens = 1000
        self.temperature = 0.7
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate_response(self, messages: List[Dict], system_prompt: str = None) -> str:
        """Generate response using Claude via Bedrock"""
        try:
            payload = {
                "anthropic_version": "bedrock-2023-05-31",  # Updated API version
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": messages
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,  # This should be the inference profile
                body=json.dumps(payload),
                contentType='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            self.logger.error(f"Error calling Bedrock: {str(e)}")
            return f"I apologize, but I'm experiencing technical difficulties: {str(e)}"

# Initialize the LLM instance
llm = BedrockLLM()

def call_llm(user_input: str, context: Dict) -> Tuple[str, Dict]:
    """
    Call the LLM with user input and context, return response and updated context
    
    Args:
        user_input: User's message
        context: Current conversation context
        
    Returns:
        Tuple of (response, updated_context)
    """
    
    # Medical assistant system prompt
    system_prompt = """You are a helpful medical appointment assistant. You can help users with:
    - Scheduling appointments
    - Providing general health information
    - Answering questions about medical procedures
    - Giving appointment reminders
    
    Always be professional, empathetic, and helpful. If asked about serious medical conditions, 
    remind users to consult with healthcare professionals for proper diagnosis and treatment.
    
    Keep track of appointment details and user preferences throughout the conversation."""
    
    try:
        # Get conversation history from context
        messages = context.get('conversation_history', [])
        
        # Add current user message
        messages.append({
            "role": "user", 
            "content": user_input
        })
        
        # Generate response
        response = llm.generate_response(messages, system_prompt)
        
        # Add assistant response to history
        messages.append({
            "role": "assistant",
            "content": response
        })
        
        # Update context
        updated_context = context.copy()
        updated_context['conversation_history'] = messages
        updated_context['last_interaction'] = user_input
        
        # Extract and store any appointment information
        if any(word in user_input.lower() for word in ['appointment', 'schedule', 'book', 'meeting']):
            appointments = updated_context.get('appointments', [])
            appointments.append({
                'request': user_input,
                'response': response,
                'timestamp': str(context.get('session_start', 'unknown'))
            })
            updated_context['appointments'] = appointments
        
        return response, updated_context
        
    except Exception as e:
        error_response = f"I apologize, but I'm having trouble processing your request: {str(e)}"
        return error_response, context