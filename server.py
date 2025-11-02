from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# Allow requests from your local HTML page
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.get("/")
def read_root():
    return {"status": "ChatKit backend is running"}

@app.post("/api/chatkit/session")
def create_chatkit_session():
    try:
        session = openai_client.chatkit.sessions.create({
            "workflow": {
                "id": os.environ.get("wf_68e5964d772481909ad033dd7a74a2020d5d3205250119fb")
            }
        })
        return {"client_secret": session.client_secret}
    except Exception as e:
        return {"error": str(e)}, 500
