import boto3
import json
import logging
from typing import Dict, List, Tuple
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class BedrockLLM:
    def __init__(self):
        """Initialize Bedrock client for Claude using .env variables"""
        region_name = os.getenv('AWS_REGION')
        model_id = os.getenv('BEDROCK_MODEL_ID')
        
        if not region_name or not model_id:
            raise ValueError("Missing AWS_REGION or BEDROCK_MODEL_ID in environment variables.")
        
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=region_name,
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        self.model_id = model_id
        self.max_tokens = 1000
        self.temperature = 0.7
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate_response(self, messages: List[Dict], system_prompt: str = None) -> str:
        """Generate response using Claude via Bedrock"""
        try:
            payload = {
                "anthropic_version": "bedrock-2023-05-31",  
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": messages
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
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
    """
    system_prompt = """You are a helpful medical appointment assistant. You can help users with:
    - Scheduling appointments
    - Providing general health information
    - Giving appointment reminders

    Always be professional, empathetic, and helpful. If asked about serious medical conditions, 
    remind users to consult with healthcare professionals for proper diagnosis and treatment.

    Keep track of appointment details and user preferences throughout the conversation."""
    
    try:
        messages = context.get('conversation_history', [])
        messages.append({"role": "user", "content": user_input})
        
        response = llm.generate_response(messages, system_prompt)
        
        messages.append({"role": "assistant", "content": response})
        
        updated_context = context.copy()
        updated_context['conversation_history'] = messages
        updated_context['last_interaction'] = user_input
        
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
        return f"I apologize, but I'm having trouble processing your request: {str(e)}", context
