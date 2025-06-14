from flask import Flask, request, jsonify
import boto3
import json
import os
import logging
from botocore.exceptions import ClientError, BotoCoreError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

PORT = int(os.environ.get('PORT', 8080))
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-2')

# Initialize Bedrock client with better error handling
bedrock = None
bedrock_error = None

try:
    # Create session first to handle credentials better
    session = boto3.Session()
    bedrock = session.client('bedrock-runtime', region_name=AWS_REGION)
    logger.info(f"Bedrock client initialized successfully in region {AWS_REGION}")
except Exception as e:
    bedrock_error = str(e)
    logger.error(f"Failed to initialize Bedrock client: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for App Runner monitoring"""
    health_status = {
        "status": "healthy" if bedrock else "degraded",
        "service": "LLM API",
        "bedrock_available": bedrock is not None,
        "region": AWS_REGION,
        "port": PORT
    }
    
    if bedrock_error:
        health_status["bedrock_error"] = bedrock_error
    
    status_code = 200 if bedrock else 503
    return jsonify(health_status), status_code

@app.route('/', methods=['GET'])
def home():
    """Root endpoint with service information"""
    return jsonify({
        "message": "LLM API is running",
        "model": "AWS Bedrock Claude",
        "provider": "AWS Bedrock",
        "region": AWS_REGION,
        "bedrock_available": bedrock is not None,
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
        # Validate request content type
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
            
        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "Missing 'prompt' field in request"}), 400
        
        if not bedrock:
            return jsonify({
                "error": "AWS Bedrock client not available",
                "details": bedrock_error
            }), 503
        
        # Using Claude 3 Haiku (fastest and cheapest)
        model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        
        # Prepare the request for Claude
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": data.get("max_tokens", 1000),
            "temperature": data.get("temperature", 0.7),
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        logger.info(f"Invoking Bedrock model {model_id}")
        
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        logger.info("Received response from Bedrock")
        
        if 'content' in response_body and len(response_body['content']) > 0:
            content = response_body['content'][0]['text']
            return jsonify({
                "response": content,
                "model": model_id,
                "usage": response_body.get('usage', {})
            })
        else:
            logger.error("No content in Bedrock response")
            return jsonify({"error": "No response content from Bedrock"}), 500
            
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"AWS ClientError: {error_code} - {error_message}")
        
        if error_code == 'AccessDeniedException':
            return jsonify({
                "error": "Access denied to Bedrock service",
                "details": "Check IAM permissions for Bedrock model access"
            }), 403
        elif error_code == 'ValidationException':
            return jsonify({
                "error": "Invalid request parameters",
                "details": error_message
            }), 400
        else:
            return jsonify({
                "error": f"AWS service error: {error_code}",
                "details": error_message
            }), 500
            
    except BotoCoreError as e:
        logger.error(f"BotoCore error: {str(e)}")
        return jsonify({
            "error": "AWS connection error",
            "details": str(e)
        }), 500
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return jsonify({
            "error": "Invalid response from Bedrock",
            "details": "Failed to parse response JSON"
        }), 500
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": ["/", "/health", "/chat"]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "Method not allowed",
        "details": "Check the HTTP method for this endpoint"
    }), 405

if __name__ == '__main__':
    logger.info(f"Starting Flask app on port {PORT}")
    logger.info(f"AWS Region: {AWS_REGION}")
    logger.info(f"Bedrock available: {bedrock is not None}")
    
    # Use Gunicorn in production, Flask dev server for local testing
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(host='0.0.0.0', port=PORT, debug=True)
    else:
        # For production, we'll use Gunicorn
        app.run(host='0.0.0.0', port=PORT, debug=False)