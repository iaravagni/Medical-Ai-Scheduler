import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List
import boto3
from botocore.exceptions import ClientError, BotoCoreError

# Import the classes and functions to test
from chatbot.conversation import BedrockLLM, call_llm, llm


class TestBedrockLLM:
    """Test cases for BedrockLLM class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.bedrock_llm = BedrockLLM(region_name='us-east-1')
    
    def test_init_default_region(self):
        """Test BedrockLLM initialization with default region"""
        llm_instance = BedrockLLM()
        assert llm_instance.model_id == "us.anthropic.claude-3-haiku-20240307-v1:0"
        assert llm_instance.max_tokens == 1000
        assert llm_instance.temperature == 0.7
    
    def test_init_custom_region(self):
        """Test BedrockLLM initialization with custom region"""
        llm_instance = BedrockLLM(region_name='us-west-2')
        assert llm_instance.model_id == "us.anthropic.claude-3-haiku-20240307-v1:0"
    
    @patch('boto3.client')
    def test_bedrock_client_creation(self, mock_boto_client):
        """Test that boto3 client is created correctly"""
        BedrockLLM(region_name='us-east-1')
        mock_boto_client.assert_called_once_with('bedrock-runtime', region_name='us-east-1')
    
    @patch('chatbot.conversation.llm.bedrock_client')
    def test_generate_response_success(self, mock_client):
        """Test successful response generation"""
        # Mock successful API response
        mock_response = {
            'body': Mock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'content': [{'text': 'Hello! How can I help you today?'}]
        }).encode('utf-8')
        
        mock_client.invoke_model.return_value = mock_response
        
        messages = [{"role": "user", "content": "Hello"}]
        result = self.bedrock_llm.generate_response(messages)
        
        assert result == "Hello! How can I help you today?"
        mock_client.invoke_model.assert_called_once()
    
    @patch('chatbot.conversation.llm.bedrock_client')
    def test_generate_response_with_system_prompt(self, mock_client):
        """Test response generation with system prompt"""
        mock_response = {
            'body': Mock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'content': [{'text': 'I am a medical assistant.'}]
        }).encode('utf-8')
        
        mock_client.invoke_model.return_value = mock_response
        
        messages = [{"role": "user", "content": "Who are you?"}]
        system_prompt = "You are a medical assistant."
        
        result = self.bedrock_llm.generate_response(messages, system_prompt)
        
        assert result == "I am a medical assistant."
        
        # Verify the payload included system prompt
        call_args = mock_client.invoke_model.call_args
        payload = json.loads(call_args[1]['body'])
        assert payload['system'] == system_prompt
    
    @patch('chatbot.conversation.llm.bedrock_client')
    def test_generate_response_client_error(self, mock_client):
        """Test handling of ClientError"""
        mock_client.invoke_model.side_effect = ClientError(
            {'Error': {'Code': 'ValidationException', 'Message': 'Invalid request'}},
            'InvokeModel'
        )
        
        messages = [{"role": "user", "content": "Hello"}]
        result = self.bedrock_llm.generate_response(messages)
        
        assert "I apologize, but I'm experiencing technical difficulties" in result
        assert "Invalid request" in result
    
    @patch('chatbot.conversation.llm.bedrock_client')
    def test_generate_response_generic_exception(self, mock_client):
        """Test handling of generic exceptions"""
        mock_client.invoke_model.side_effect = Exception("Network error")
        
        messages = [{"role": "user", "content": "Hello"}]
        result = self.bedrock_llm.generate_response(messages)
        
        assert "I apologize, but I'm experiencing technical difficulties" in result
        assert "Network error" in result
    
    @patch('chatbot.conversation.llm.bedrock_client')
    def test_generate_response_malformed_response(self, mock_client):
        """Test handling of malformed API response"""
        mock_response = {
            'body': Mock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'invalid': 'response'
        }).encode('utf-8')
        
        mock_client.invoke_model.return_value = mock_response
        
        messages = [{"role": "user", "content": "Hello"}]
        result = self.bedrock_llm.generate_response(messages)
        
        assert "I apologize, but I'm experiencing technical difficulties" in result


class TestCallLLMFunction:
    """Test cases for call_llm function"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.sample_context = {
            'conversation_history': [],
            'session_start': '2024-01-01T10:00:00'
        }
    
    @patch('chatbot.conversation.llm.generate_response')
    def test_call_llm_first_interaction(self, mock_generate):
        """Test first interaction with empty context"""
        mock_generate.return_value = "Hello! I'm your medical appointment assistant."
        
        user_input = "Hello"
        context = {}
        
        response, updated_context = call_llm(user_input, context)
        
        assert response == "Hello! I'm your medical appointment assistant."
        assert 'conversation_history' in updated_context
        assert len(updated_context['conversation_history']) == 2
        assert updated_context['conversation_history'][0]['role'] == 'user'
        assert updated_context['conversation_history'][1]['role'] == 'assistant'
        assert updated_context['last_interaction'] == user_input
    
    @patch('chatbot.conversation.llm.generate_response')
    def test_call_llm_with_existing_history(self, mock_generate):
        """Test interaction with existing conversation history"""
        mock_generate.return_value = "I can help you schedule an appointment."
        
        context = {
            'conversation_history': [
                {'role': 'user', 'content': 'Hello'},
                {'role': 'assistant', 'content': 'Hi there!'}
            ]
        }
        
        user_input = "I need to book an appointment"
        response, updated_context = call_llm(user_input, context)
        
        assert response == "I can help you schedule an appointment."
        assert len(updated_context['conversation_history']) == 4
        assert updated_context['conversation_history'][-2]['content'] == user_input
        assert updated_context['conversation_history'][-1]['content'] == response
    
    @patch('chatbot.conversation.llm.generate_response')
    def test_call_llm_appointment_detection(self, mock_generate):
        """Test appointment keyword detection and storage"""
        mock_generate.return_value = "I've scheduled your appointment for 2pm tomorrow."
        
        appointment_inputs = [
            "I need to schedule an appointment",
            "Can you book a meeting with Dr. Smith?",
            "I want to make an appointment",
            "Schedule me for next week"
        ]
        
        for user_input in appointment_inputs:
            context = self.sample_context.copy()
            response, updated_context = call_llm(user_input, context)
            
            assert 'appointments' in updated_context
            assert len(updated_context['appointments']) == 1
            assert updated_context['appointments'][0]['request'] == user_input
            assert updated_context['appointments'][0]['response'] == response
    
    @patch('chatbot.conversation.llm.generate_response')
    def test_call_llm_multiple_appointments(self, mock_generate):
        """Test multiple appointment storage"""
        mock_generate.return_value = "Appointment confirmed."
        
        context = self.sample_context.copy()
        
        # First appointment
        response1, context = call_llm("Schedule appointment", context)
        
        # Second appointment
        response2, updated_context = call_llm("Book another meeting", context)
        
        assert len(updated_context['appointments']) == 2
        assert updated_context['appointments'][0]['request'] == "Schedule appointment"
        assert updated_context['appointments'][1]['request'] == "Book another meeting"
    
    @patch('chatbot.conversation.llm.generate_response')
    def test_call_llm_non_appointment_interaction(self, mock_generate):
        """Test non-appointment interactions don't create appointment records"""
        mock_generate.return_value = "Here's some general health information."
        
        user_input = "What are the symptoms of flu?"
        context = self.sample_context.copy()
        
        response, updated_context = call_llm(user_input, context)
        
        assert 'appointments' not in updated_context
        assert updated_context['last_interaction'] == user_input
    
    @patch('chatbot.conversation.llm.generate_response')
    def test_call_llm_system_prompt_usage(self, mock_generate):
        """Test that system prompt is passed correctly"""
        mock_generate.return_value = "I'm your medical assistant."
        
        user_input = "Who are you?"
        context = {}
        
        call_llm(user_input, context)
        
        # Verify system prompt was passed
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args
        system_prompt = call_args[0][1]  # Second argument should be system prompt
        
        assert "medical appointment assistant" in system_prompt
        assert "professional, empathetic, and helpful" in system_prompt
    
    @patch('chatbot.conversation.llm.generate_response')
    def test_call_llm_exception_handling(self, mock_generate):
        """Test exception handling in call_llm"""
        mock_generate.side_effect = Exception("API Error")
        
        user_input = "Hello"
        context = {}
        
        response, updated_context = call_llm(user_input, context)
        
        assert "I apologize, but I'm having trouble processing your request" in response
        assert "API Error" in response
        assert updated_context == context  # Context should remain unchanged on error
    
    def test_call_llm_context_preservation(self):
        """Test that original context is preserved when copied"""
        original_context = {
            'conversation_history': [{'role': 'user', 'content': 'test'}],
            'session_start': '2024-01-01',
            'user_preferences': {'language': 'en'}
        }
        
        with patch('chatbot.conversation.llm.generate_response') as mock_generate:
            mock_generate.return_value = "Test response"
            
            response, updated_context = call_llm("Hello", original_context)
            
            # Original context should be unchanged
            assert original_context['user_preferences'] == {'language': 'en'}
            
            # Updated context should have the new data plus original data
            assert updated_context['user_preferences'] == {'language': 'en'}
            assert len(updated_context['conversation_history']) > len(original_context['conversation_history'])


class TestIntegration:
    """Integration tests"""
    
    @patch('chatbot.conversation.llm.bedrock_client')
    def test_end_to_end_conversation(self, mock_client):
        """Test complete conversation flow"""
        # Mock API responses
        responses = [
            {'content': [{'text': 'Hello! How can I help you with medical appointments today?'}]},
            {'content': [{'text': 'I can help you schedule that appointment. What type of appointment do you need?'}]},
            {'content': [{'text': 'Great! I\'ve noted your cardiology appointment request.'}]}
        ]
        
        mock_response_objects = []
        for resp in responses:
            mock_resp = {'body': Mock()}
            mock_resp['body'].read.return_value = json.dumps(resp).encode('utf-8')
            mock_response_objects.append(mock_resp)
        
        mock_client.invoke_model.side_effect = mock_response_objects
        
        # Simulate conversation
        context = {}
        
        # First interaction
        response1, context = call_llm("Hello", context)
        assert "Hello!" in response1
        assert len(context['conversation_history']) == 2
        
        # Second interaction (appointment request)
        response2, context = call_llm("I need to schedule an appointment", context)
        assert "schedule" in response2
        assert len(context['conversation_history']) == 4
        assert 'appointments' in context
        
        # Third interaction
        response3, context = call_llm("I need a cardiology appointment", context)
        assert "cardiology" in response3
        assert len(context['appointments']) == 2


# Test fixtures and utilities
@pytest.fixture
def sample_messages():
    """Fixture providing sample message format"""
    return [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]


@pytest.fixture
def sample_context():
    """Fixture providing sample context"""
    return {
        'conversation_history': [],
        'session_start': '2024-01-01T10:00:00',
        'appointments': []
    }


# Test configuration
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=bedrock_llm", "--cov-report=html", "--cov-report=term"])