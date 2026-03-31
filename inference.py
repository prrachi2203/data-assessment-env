import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY) if API_KEY else None

MAX_STEPS = 5


def safe_action_parse(text):
    try:
        data = json.loads(text)
        return {
            "category": data.get("category", "general"),
            "response": data.get("response", "We will assist you shortly."),
            "escalate": data.get("escalate", False),
        }
    except:
        return {
            "category": "general",
            "response": "We will assist you shortly. Please wait.",
            "escalate": False,
        }


def run_task(task_id):
    print(f"\n--- Running Task: {task_id} ---")

    response = requests.post(f"{API_BASE_URL}/reset", json={"task_id": task_id})
    obs = response.json()

    total_reward = 0.0

    for step in range(MAX_STEPS):
        print(f"Step {step+1}")

        prompt = f"""
        You are a customer support agent.

        Subject: {obs.get('subject')}
        Description: {obs.get('description')}
        History: {obs.get('history')}

        Return JSON:
        {{
            "category": "...",
            "response": "...",
            "escalate": true/false
        }}
        """

        try:
            if not client:
                raise Exception("No API key")

            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"},
            )

            text = completion.choices[0].message.content

        except Exception as e:
            print(f"LLM failed: {e}")
            text = ""

        action_data = safe_action_parse(text)

        try:
            result = requests.post(f"{API_BASE_URL}/step", json=action_data).json()
        except Exception as e:
            print(f"Step failed: {e}")
            break

        obs = result["observation"]
        reward = result["reward"]
        done = result["done"]

        total_reward += reward["score"]

        print(f"Reward: {reward['score']} | Done: {done}")

        if done:
            break

    print(f"Final Score ({task_id}): {total_reward}")
    return total_reward


if __name__ == "__main__":
    tasks = ["easy", "medium", "hard"]
    scores = []

    for t in tasks:
        scores.append(run_task(t))

    print("\nFINAL RESULTS")
    for i, t in enumerate(tasks):
        print(f"{t}: {scores[i]}")

    print(f"Average: {sum(scores)/len(scores)}")
