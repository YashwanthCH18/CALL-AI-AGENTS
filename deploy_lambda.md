# Deploying to AWS Lambda

This guide explains how to deploy your Voice AI Microservice to AWS Lambda using the `Mangum` adapter.

## Prerequisites
- AWS Account
- AWS CLI installed and configured (optional, but easier)
- Python 3.11 or 3.12 installed

## Step 1: Prepare the Deployment Package
AWS Lambda requires all dependencies to be included in the uploaded ZIP file.

1.  **Create a package directory:**
    ```powershell
    mkdir package
    ```

2.  **Install dependencies into the package directory:**
    ```powershell
    pip install -r requirements.txt --target ./package
    ```

3.  **Copy your application code into the package directory:**
    Copy the `app` folder and `main.py` into the `package` folder.
    *   Do NOT copy `venv` or `.git`.

4.  **Zip the contents:**
    *   Go inside the `package` folder.
    *   Select all files and folders.
    *   Right-click -> Send to -> Compressed (zipped) folder.
    *   Name it `function.zip`.

## Step 2: Create Lambda Function
1.  Go to the **AWS Lambda Console**.
2.  Click **Create function**.
3.  Select **Author from scratch**.
4.  **Function name**: `voice-ai-service`.
5.  **Runtime**: Python 3.11 (or matching your local version).
6.  **Architecture**: x86_64.
7.  Click **Create function**.

## Step 3: Upload Code
1.  In the **Code** tab, click **Upload from** -> **.zip file**.
2.  Upload your `function.zip`.
3.  **Important**: In **Runtime settings** (scroll down), change **Handler** to:
    `app.main.handler`
    (This points to the `handler` object in `app/main.py`).

## Step 4: Environment Variables
1.  Go to the **Configuration** tab -> **Environment variables**.
2.  Click **Edit**.
3.  Add all variables from your `.env` file:
    *   `SARVAM_API_KEY`
    *   `GEMINI_API_KEY`
    *   `TWILIO_ACCOUNT_SID`
    *   `TWILIO_AUTH_TOKEN`
    *   `SUPABASE_URL`
    *   `SUPABASE_KEY`
    *   `GEMINI_MODEL` (e.g., `gemini-2.5-flash`)

## Step 5: Increase Timeout
1.  Go to **Configuration** -> **General configuration**.
2.  Click **Edit**.
3.  Increase **Timeout** to **30 seconds** (or 1 minute). The default 3 seconds is too short for AI processing.
4.  Click **Save**.

## Step 6: Setup API Gateway
1.  Click **Add trigger**.
2.  Select **API Gateway**.
3.  **Intent**: Create a new API.
4.  **API type**: HTTP API (cheaper and easier).
5.  **Security**: Open (for Twilio to access).
6.  Click **Add**.

## Step 7: Configure Twilio
1.  Copy the **API Endpoint** URL from the API Gateway trigger (e.g., `https://xyz.execute-api.us-east-1.amazonaws.com/default`).
2.  Go to **Twilio Console**.
3.  Update the **Webhook URL** to:
    `YOUR_API_GATEWAY_URL/twilio/voice`
4.  Save.

## Done!
Your service is now serverless and scalable. No more ngrok!
