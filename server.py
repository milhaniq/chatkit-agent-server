from fastapi import FastAPI
from openai import OpenAI
import os

app = FastAPI()
openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.post("/api/chatkit/session")
def create_chatkit_session():
    session = openai.chatkit.sessions.create(
        workflow={"id": "wf_68e5964d772481909ad033dd7a74a2020d5d3205250119fb"}
    )
    return {"client_secret": session.client_secret}
