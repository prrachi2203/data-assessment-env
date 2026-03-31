from .models import Action, Reward

def grade_step(action: Action, task: dict) -> Reward:
    score = 0.0
    feedback_parts = []

    # 1. Category Check (+0.4 or -0.2)
    if action.category == task["expected_category"]:
        score += 0.4
        feedback_parts.append("Correct category selected.")
    else:
        score -= 0.2
        feedback_parts.append(f"Incorrect category. Expected {task['expected_category']}.")

    # 2. Politeness Check (+0.2)
    response_lower = action.response.lower()
    if "please" in response_lower or "thank you" in response_lower or "thanks" in response_lower or "sorry" in response_lower:
        score += 0.2
        feedback_parts.append("Response is polite.")
    else:
        feedback_parts.append("Response could be more polite.")

    # 3. Detail Check (+0.2 or -0.1)
    if len(action.response.split()) > 10:
        score += 0.2
        feedback_parts.append("Response is sufficiently detailed.")
    elif len(action.response.strip()) == 0:
        score -= 0.1
        feedback_parts.append("Response is empty.")
    else:
        score -= 0.1
        feedback_parts.append("Response is too short.")

    # 4. Escalation Check (+0.2)
    if action.escalate == task["requires_escalation"]:
        score += 0.2
        feedback_parts.append("Correct escalation decision.")
    else:
        feedback_parts.append("Incorrect escalation decision.")

    # Clamp score between 0 and 1
    final_score = max(0.0, min(1.0, score))
    
    done = final_score >= 0.8
    
    return Reward(
        score=final_score,
        feedback=" ".join(feedback_parts),
        done=done
    )
