# OpenEnv Customer Support Triage Environment

This project implements an OpenEnv-compliant environment for simulating a Customer Support Ticket Triage System.

## Environment Description
The environment simulates the workflow of a customer support agent who must categorize incoming tickets, provide polite and helpful responses, and decide whether to escalate critical issues.

## Why it's a Real-World Task
Ticket triage is a fundamental operation in any customer-facing business. It requires:
1. **Classification**: Understanding the intent and domain of the request.
2. **Communication**: Maintaining a professional and empathetic tone.
3. **Decision Making**: Identifying high-priority or complex issues that require specialist intervention.

## Observation Space
The observation is a Pydantic model containing:
- `ticket_id`: Unique identifier for the ticket.
- `customer_name`: Name of the customer.
- `subject`: Ticket subject line.
- `description`: Detailed problem description.
- `history`: List of previous interactions in the ticket.
- `status`: Current status (e.g., OPEN).
- `available_categories`: List of valid categories for classification.

## Action Space
The action is a Pydantic model containing:
- `category`: The selected category (Technical, Billing, Account, General).
- `response`: The text response to be sent to the customer.
- `escalate`: A boolean flag indicating if the ticket should be escalated.

## Reward Design
The reward is deterministic and ranges from 0.0 to 1.0:
- **+0.4**: Correct category classification.
- **+0.2**: Politeness check (presence of "please", "thank you", etc.).
- **+0.2**: Detail check (response length > 10 words).
- **+0.2**: Correct escalation decision.
- **-0.2**: Penalty for wrong category.
- **-0.1**: Penalty for empty or very short response.

## Task Descriptions
1. **easy (Password Reset)**: A straightforward request for account access. Requires "Account" category and no escalation.
2. **medium (Duplicate Billing)**: A billing discrepancy. Requires "Billing" category and polite handling.
3. **hard (API Error Escalation)**: A critical technical failure. Requires "Technical" category and mandatory escalation.

## Setup Instructions

### Local Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python3 main.py
   ```

### Docker Run
1. Build the image:
   ```bash
   docker build -t support-triage .
   ```
2. Run the container:
   ```bash
   docker run -p 7860:7860 support-triage
   ```

## Inference Instructions
1. Set environment variables:
   ```bash
   export OPENAI_API_KEY=your_key
   export API_BASE_URL=http://localhost:7860
   export MODEL_NAME=gpt-3.5-turbo
   ```
2. Run the inference script:
   ```bash
   python3 inference.py
   ```

## Example Baseline Scores
- **Easy**: 1.0 (Correct category, polite, detailed)
- **Medium**: 1.0 (Correct category, polite, detailed)
- **Hard**: 1.0 (Correct category, polite, detailed, escalated)
