from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx

app = FastAPI()

# Allow requests from your local HTML page
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your workflow ID
WORKFLOW_ID = "wf_68e5964d772481909ad033dd7a74a2020d5d3205250119fb"

@app.get("/")
def read_root():
    return {"status": "ChatKit backend is running"}

@app.post("/api/chatkit/session")
async def create_chatkit_session():
    try:
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        
        if not openai_api_key:
            return {"error": "OPENAI_API_KEY not configured"}, 500
        
        # Make direct API call to OpenAI ChatKit endpoint
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chatkit/sessions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {openai_api_key}",
                    "OpenAI-Beta": "chatkit_beta=v1"
                },
                json={
                    "workflow": {
                        "id": WORKFLOW_ID
                    }
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                error_detail = response.text
                return {"error": f"OpenAI API error: {response.status_code} - {error_detail}"}, 500
            
            data = response.json()
            return {"client_secret": data.get("client_secret")}
            
    except Exception as e:
        return {"error": str(e)}, 500
