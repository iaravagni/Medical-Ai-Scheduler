from dotenv import load_dotenv
import os
import boto3
import json

# Load environment variables from .env
load_dotenv()

# Fetch credentials from environment
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

# Initialize the Bedrock client
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=aws_region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
)

def call_llm(prompt, context=[]):
    try:
        # Build the prompt
        full_prompt = ""
        for message in context:
            full_prompt += f"\n\n{message['role'].capitalize()}: {message['content']}"
        full_prompt += f"\n\nUser: {prompt}\n\nAssistant:"

        # Call Bedrock 
        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
            body=json.dumps({
                "prompt": full_prompt,
                "max_tokens_to_sample": 300,
                "temperature": 0.7,
                "stop_sequences": ["\n\nUser:"]
            }),
            contentType="application/json",
            accept="application/json"
        )

        result = json.loads(response['body'].read())
        reply = result["completion"].strip()

        context.append({"role": "user", "content": prompt})
        context.append({"role": "assistant", "content": reply})

        return reply, context

    except Exception as e:
        return f"Sorry, something went wrong: {str(e)}", context
