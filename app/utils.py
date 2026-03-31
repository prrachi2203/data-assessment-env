# Utility functions if needed
def format_history(history):
    return "\n".join([f"{h['role']}: {h['content']}" for h in history])
