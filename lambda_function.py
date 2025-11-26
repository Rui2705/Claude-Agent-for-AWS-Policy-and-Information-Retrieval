import json
import boto3

# --- Configuration ---

# Initialize the Bedrock Runtime client
# It will use the region configured for the Lambda function
bedrock_rt = boto3.client('bedrock-runtime') 
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


# 2.1.1: The Agent's Persona (Role Prompting)
# This System Prompt enforces conciseness and strict formatting control.
SYSTEM_PROMPT = "You are a concise, expert AWS Operations Engineer. Your task is to generate clean, usable infrastructure code, policies, or documentation based on the user's request. NEVER include introductory or explanatory text unless the user explicitly asks for it. Always use the specified format (JSON, YAML, Markdown)."

# --- Lambda Handler ---

def lambda_handler(event, context):
    try:
        # 1. Extract User Prompt from API Gateway payload
        # API Gateway sends the prompt in the request body as JSON: {"prompt": "..."}
        body = json.loads(event.get('body', '{}'))
        user_prompt = body.get('prompt')

        if not user_prompt:
            # Standard error response if the 'prompt' key is missing
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing "prompt" in request body. Please ensure the payload is {"prompt": "your request"}.'})
            }

        # 2. Construct the Bedrock Messages API payload
        prompt_config = {
            "anthropic_version": "bedrock-2023-05-31",
            "system": SYSTEM_PROMPT,  # The core of the Agent's behavior
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": user_prompt}]
                }
            ],
            # Inference parameters (low temperature for reliable code/policy generation)
            "max_tokens": 1000, 
            "temperature": 0.3 
        }

        # 3. Invoke the Claude model
        response = bedrock_rt.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(prompt_config),
            contentType='application/json'
        )

        # 4. Process the response
        response_body = json.loads(response['body'].read())
        
        # Claude's response text is nested inside the 'content' array
        claude_output = response_body['content'][0]['text']

        # 5. Return the result to the API Gateway
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'response': claude_output})
        }

    except Exception as e:
        # Log the error for debugging in CloudWatch
        print(f"Error during LLM invocation: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Internal server error. Check Lambda logs for details: {str(e)}'})
        }