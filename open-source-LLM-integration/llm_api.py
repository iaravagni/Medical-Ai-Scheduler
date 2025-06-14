from flask import Flask, request, jsonify
import os
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

PORT = int(os.environ.get('PORT', 8080))

# Global variables for model
text_generator = None
model_name = "microsoft/DialoGPT-small"  # Small, fast conversational model

def load_model():
    """Load the language model on startup"""
    global text_generator
    try:
        logger.info(f"Loading model: {model_name}")
        
        # Use a simple text generation pipeline
        text_generator = pipeline(
            "text-generation",
            model=model_name,
            tokenizer=model_name,
            device=-1,  # CPU only (more reliable for deployment)
            max_length=100,
            do_sample=True,
            temperature=0.7,
            pad_token_id=50256
        )
        
        logger.info("Model loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return False

# Load model on startup
model_loaded = load_model()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy" if model_loaded else "degraded",
        "service": "Local LLM API",
        "model": model_name,
        "model_loaded": model_loaded
    }), 200 if model_loaded else 503

@app.route('/', methods=['GET'])
def home():
    """Root endpoint with service information"""
    return jsonify({
        "message": "Local LLM API is running",
        "model": model_name,
        "provider": "Hugging Face Transformers",
        "model_loaded": model_loaded,
        "endpoints": {
            "chat": "/chat (POST)",
            "health": "/health (GET)",
            "home": "/ (GET)"
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for LLM interactions"""
    try:
        if not model_loaded or not text_generator:
            return jsonify({
                "error": "Model not available",
                "details": "Language model failed to load"
            }), 503
        
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
            
        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "Missing 'prompt' field in request"}), 400
        
        # Get optional parameters
        max_length = min(data.get("max_length", 50), 200)  # Cap at 200 for performance
        temperature = max(0.1, min(data.get("temperature", 0.7), 1.0))  # Between 0.1 and 1.0
        
        logger.info(f"Processing prompt: {prompt[:50]}...")
        
        # Generate response
        try:
            responses = text_generator(
                prompt,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=1,
                truncation=True
            )
            
            if responses and len(responses) > 0:
                generated_text = responses[0]['generated_text']
                
                # Clean up the response (remove the original prompt)
                if generated_text.startswith(prompt):
                    response_text = generated_text[len(prompt):].strip()
                else:
                    response_text = generated_text.strip()
                
                # If response is empty, provide a fallback
                if not response_text:
                    response_text = "I understand your message. Could you please be more specific about what you'd like to discuss?"
                
                return jsonify({
                    "response": response_text,
                    "model": model_name,
                    "parameters": {
                        "max_length": max_length,
                        "temperature": temperature
                    }
                })
            else:
                return jsonify({"error": "No response generated"}), 500
                
        except Exception as model_error:
            logger.error(f"Model generation error: {str(model_error)}")
            return jsonify({
                "error": "Model generation failed",
                "details": str(model_error)
            }), 500
            
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@app.route('/models', methods=['GET'])
def list_models():
    """List available model information"""
    return jsonify({
        "current_model": model_name,
        "model_info": {
            "name": "DialoGPT-small",
            "description": "Small conversational AI model by Microsoft",
            "size": "Small (~117MB)",
            "good_for": ["Conversations", "Q&A", "Simple chat"]
        },
        "status": "loaded" if model_loaded else "failed"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": ["/", "/health", "/chat", "/models"]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "Method not allowed",
        "details": "Check the HTTP method for this endpoint"
    }), 405

if __name__ == '__main__':
    logger.info(f"Starting Flask app on port {PORT}")
    logger.info(f"Model loaded: {model_loaded}")
    logger.info(f"Using model: {model_name}")
    
    app.run(host='0.0.0.0', port=PORT, debug=False)