from app.models import Observation, Action, Reward


class SupportEnv:
    def __init__(self, task_name="easy"):
        self.task_name = task_name
        self.state_data = None
        self.done = False

    def reset(self):
        if self.task_name == "easy":
            self.state_data = {
                "ticket_id": "T1",
                "customer_message": "I forgot my password",
                "history": [],
                "expected_category": "password_reset"
            }
        elif self.task_name == "medium":
            self.state_data = {
                "ticket_id": "T2",
                "customer_message": "I was charged twice",
                "history": [],
                "expected_category": "billing"
            }
        else:
            self.state_data = {
                "ticket_id": "T3",
                "customer_message": "API error 500",
                "history": [],
                "expected_category": "technical"
            }

        self.done = False
        return Observation(**self.state_data)

    def step(self, action: Action):
        score = 0.0

        if action.category == self.state_data["expected_category"]:
            score += 0.4
        else:
            score -= 0.2

        if "please" in action.response.lower():
            score += 0.2

        if len(action.response) > 20:
            score += 0.2

        if self.state_data["expected_category"] == "technical" and action.escalate:
            score += 0.2

        score = max(0.0, min(1.0, score))

        if score >= 0.8:
            self.done = True

        self.state_data["history"].append(action.response)

        return Observation(**self.state_data), Reward(score=score, feedback=""), self.done, {}

    def state(self):
        return self.state_data
