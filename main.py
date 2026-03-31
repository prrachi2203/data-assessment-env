import os
import requests
from typing import Dict, Any
from fastapi import FastAPI, Body
from app.env import SupportEnv
from app.models import Action

app = FastAPI(title="OpenEnv Support Triage API")

env = None


@app.post("/reset")
def reset(body: Dict[str, Any] = Body(default={})):
    """
    MUST:
    - accept empty body {}
    - return JSON
    """
    global env

    try:
        task_id = body.get("task_id", "easy")

        env = SupportEnv()
        env.task_name = task_id

        obs = env.reset()

        # convert pydantic → dict
        return obs.dict() if hasattr(obs, "dict") else obs

    except Exception as e:
        return {"error": str(e)}


@app.post("/step")
def step(action: Action):
    global env

    try:
        if env is None:
            return {"error": "Call /reset first"}

        obs, reward, done, info = env.step(action)

        return {
            "observation": obs.dict() if hasattr(obs, "dict") else obs,
            "reward": reward.dict() if hasattr(reward, "dict") else reward,
            "done": done,
            "info": info,
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/state")
def get_state():
    global env

    if env is None:
        return {"error": "Environment not initialized"}

    return env.state()


@app.post("/chat/completions")
def proxy_chat_completions(request_data: Dict[str, Any] = Body(...)):
    """
    Required for inference compatibility
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("HF_TOKEN")

    if not api_key:
        return {"error": "API key not set"}

    url = os.getenv("API_BASE_URL", "https://api.openai.com/v1/chat/completions")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=request_data, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

def main():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=7860)
