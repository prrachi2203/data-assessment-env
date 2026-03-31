import copy
from typing import Tuple, Dict, Any
from .models import Observation, Action, Reward
from .tasks import TASKS
from .graders import grade_step

class SupportEnv:
    def __init__(self, task_name="easy"):
    self.task_name = task_name
    self.state_data = None
    self.done = False

    def reset(self, task_id: str = None) -> Observation:
        if task_id:
            task = next((t for t in self.tasks if t["id"] == task_id), self.tasks[0])
            self.current_task_index = self.tasks.index(task)
        else:
            self.current_task_index = 0
            
        self.current_step = 0
        task = self.tasks[self.current_task_index]
        self.state_data = copy.deepcopy(task["initial_state"])
        
        return Observation(**self.state_data)

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        self.current_step += 1
        task = self.tasks[self.current_task_index]
        
        reward = grade_step(action, task)
        
        # Update history
        self.state_data["history"].append({
            "role": "agent",
            "content": action.response,
            "category": action.category,
            "escalated": str(action.escalate)
        })
        
        done = reward.done or self.current_step >= self.max_steps
        
        info = {
            "step": self.current_step,
            "max_steps": self.max_steps,
            "difficulty": task["difficulty"]
        }
        
        return Observation(**self.state_data), reward, done, info

    def state(self) -> Dict[str, Any]:
        return {
            "task_index": self.current_task_index,
            "current_step": self.current_step,
            "state_data": self.state_data
        }
