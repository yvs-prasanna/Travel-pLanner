from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from flask import json
from pydantic import BaseModel
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

api_key = "AIzaSyAcWIxEMPzZqkfvgM3oqqNPOmWW8DaF7Wg"

model = init_chat_model(
    "google_genai:gemini-2.5-flash",
    api_key=api_key)


agent = create_agent(
    model=model,
    system_prompt="You are a helpful assistant. For every user_input, "
        "respond strictly in JSON format with two fields: "
        "`title` (a concise 3-5 word summary) and `content` (a clear, detailed explanation). "
        )


app = FastAPI()

# Allow the frontend to call this Python backend during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ModelRequest(BaseModel):
    user_input: str


def run_model(user_input: str) -> str:
    response = agent.invoke({
        "messages": [{"role": "user", "content": user_input}]
    })

    # If response is a dict with messages, loop through them
    if isinstance(response, dict) and "messages" in response:
        for msg in response["messages"]:
            if msg.__class__.__name__ == "AIMessage":
                try:
                    return json.loads(msg.content)  # Parse JSON
                except Exception as e:
                    return {"title": "Error", "content": msg.content}

    return  {"result": response}


@app.post("/predict")
def predict(request: ModelRequest):
    result = run_model(request.user_input)
    return {"result": result}


@app.get("/")
def home():
    return {"message": "Python model API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
