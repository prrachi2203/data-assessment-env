from typing import List, Dict, Any

TASKS = [
    {
        "id": "easy",
        "name": "Password Reset",
        "difficulty": "EASY",
        "initial_state": {
            "ticket_id": "TKT-001",
            "customer_name": "Alice Smith",
            "subject": "Cannot login to my account",
            "description": "Hi, I forgot my password and the reset link isn't arriving in my inbox. Can you help?",
            "history": [],
            "status": "OPEN"
        },
        "expected_category": "Account",
        "requires_escalation": False
    },
    {
        "id": "medium",
        "name": "Duplicate Billing",
        "difficulty": "MEDIUM",
        "initial_state": {
            "ticket_id": "TKT-002",
            "customer_name": "Bob Jones",
            "subject": "Charged twice for subscription",
            "description": "I noticed two charges of $29.99 on my credit card this month instead of one. Please refund the duplicate charge.",
            "history": [],
            "status": "OPEN"
        },
        "expected_category": "Billing",
        "requires_escalation": False
    },
    {
        "id": "hard",
        "name": "API Error Escalation",
        "difficulty": "HARD",
        "initial_state": {
            "ticket_id": "TKT-003",
            "customer_name": "Charlie Tech",
            "subject": "Critical API 500 Errors",
            "description": "Our production environment is receiving 500 Internal Server Errors when calling the /v1/process endpoint. This is urgent.",
            "history": [],
            "status": "OPEN"
        },
        "expected_category": "Technical",
        "requires_escalation": True
    }
]
