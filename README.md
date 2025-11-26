# Claude-Agent-for-AWS-Policy-and-Information-Retrieval

## ⏱️ Phase 1: Setup & Plumbing

### **1.1 IAM & Bedrock Access**
- Create Lambda execution role
- Attach:
  - `AWSLambdaBasicExecutionRole`
  - Custom policy for:
    - `bedrock:InvokeModel`
    - `bedrock:InvokeModelWithResponseStream`

### **1.2 Lambda Function**
- Create Python 3.x Lambda function
- Paste code from `lambda_function.py`
- Test with a simple payload:
  ```json
  { "prompt": "Say hello" }
  
### **1.3 API Gateway Setup**
- Create REST API
- Create resource /draft
- Add POST method with Lambda Proxy Integration
- Deploy API

## ⚙️ Phase 2: Code, Persona & Testing 

### 2.1 System Prompt Setup
- Create strong persona for "AWS Operations Engineer"
- Enforce:
    - No explanations unless asked
    - Only JSON/YAML/Markdown output
    - Strict formatting

### 2.2 Lambda Logic Integration
- Implement:
  - System Prompt
  - User message
  - Claude Messages API request
  - Output extraction (`response_body['content'][0]['text']`)
  - Set `temperature = 0.3` for consistency
    
### 2.3 IAM Output Validation
- Test prompt:
  ```pgsql
  Generate an S3 read-only IAM policy in JSON. No explanations. 
- Expected output: clean JSON without comments.

## 📄 Phase 3: Final Deliverables

### 3.1 Documentation Output Test
- Test prompt:
  ```Rust
  Generate Markdown documentation for deploying an API Gateway + Lambda endpoint.
- Validate:
  - Markdown headings
  - Bullet lists
  - No intro text unless asked

### 3.2 Wrap-Up & Final Demo
Save:
- Final System Prompt
- IAM JSON output
- Markdown output
  
Prepare quick 1-minute demo:
- Call /draft
- Show consistent model responses

## Lambda Function
<img width="1920" height="834" alt="image" src="https://github.com/user-attachments/assets/a63619b1-9418-4a95-bd64-47f3817bbf98" />

## API Gateway
<img width="1920" height="843" alt="image" src="https://github.com/user-attachments/assets/9552dea9-01ce-4cbd-b8f1-8c2f282a714b" />


