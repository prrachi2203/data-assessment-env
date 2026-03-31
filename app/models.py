from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Observation(BaseModel):
    ticket_id: str
    customer_name: str
    subject: str
    description: str
    history: List[Dict[str, str]]
    status: str
    available_categories: List[str] = ["Technical", "Billing", "Account", "General"]

class Action(BaseModel):
    category: str
    response: str
    escalate: bool = False

class Reward(BaseModel):
    score: float
    feedback: str
    done: bool
