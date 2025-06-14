from flask import Flask, request, jsonify
import boto3
import json
import os

app = Flask(__name__)

PORT = int(os.environ.get('PORT', 8080))
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

# Initialize Bedrock client
try:
    bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)
except Exception as e:
    print(f"Failed to initialize Bedrock client: {e}")
    bedrock = None

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "service": "LLM API",
        "bedrock_available": bedrock is not None
    }), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "LLM API is running",
        "model": "AWS Bedrock Claude",
        "provider": "AWS Bedrock",
        "region": AWS_REGION,
        "endpoints": {
            "chat": "/chat",
            "health": "/health"
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get("prompt")
    
    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400
    
    if not bedrock:
        return jsonify({"error": "AWS Bedrock client not available"}), 500
    
    # Using Claude 3 Haiku (fastest and cheapest)
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    
    try:
        # Prepare the request for Claude
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        
        if 'content' in response_body and len(response_body['content']) > 0:
            content = response_body['content'][0]['text']
            return jsonify({"response": content})
        else:
            return jsonify({"error": "No response from Bedrock"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Bedrock request failed: {str(e)}"}), 500

if __name__ == '__main__':
    print(f"Starting Flask app on port {PORT}")
    print(f"AWS Region: {AWS_REGION}")
    print(f"Bedrock available: {bedrock is not None}")
    app.run(host='0.0.0.0', port=PORT, debug=False)