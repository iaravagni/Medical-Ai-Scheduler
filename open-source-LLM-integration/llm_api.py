from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)
OLLAMA_API_URL = "http://localhost:11434/api/chat"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get("prompt")
    
    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400
    
    payload = {
        "model": "llama3",  # or "mistral"
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, stream=True)
        response.raise_for_status()
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8").strip()
                if line_str:  # Skip empty lines
                    try:
                        chunk = json.loads(line_str)
                        if "message" in chunk and "content" in chunk["message"]:
                            content = chunk["message"]["content"]
                            full_response += content
                        
                        # Check if this is the final chunk
                        if chunk.get("done", False):
                            break
                            
                    except json.JSONDecodeError as e:
                        print(f"Skipping invalid JSON chunk: {line_str[:100]}... Error: {e}")
                        continue
        
        return jsonify({"response": full_response})
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)