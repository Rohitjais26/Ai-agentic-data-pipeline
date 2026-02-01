# =========================================
# OUTREACH AGENT (MOCK EXECUTION)
# Internship AI Agentic Project
# =========================================

import pandas as pd
from datetime import datetime
import random



# 1. Load Action Queue
action_queue = pd.read_csv("action_queue.csv")

print("Action queue loaded")
print("Total actions to execute:", action_queue.shape[0])


# 2. Message Templates
MESSAGE_TEMPLATES = {
    "send_document_checklist": "Hi {lead_id}, please share the pending documents to continue.",
    "soft_reengagement": "Hi {lead_id}, just checking in to see if you’d like to continue.",
    "counsellor_followup": "Hi {lead_id}, our counsellor will call you shortly.",
    "push_completion": "Hi {lead_id}, please complete your registration to move ahead."
}


# 3. Mock Send Functions
def send_whatsapp(lead_id, message):
    print(f"[WhatsApp] → Lead {lead_id}: {message}")
    return "sent"


def make_call(lead_id, message):
    print(f"[Call] → Lead {lead_id}: {message}")
    return random.choice(["answered", "missed"])



# 4. Execute Outreach
logs = []

for _, row in action_queue.iterrows():
    lead_id = row["lead_id"]
    action = row["next_action"]
    channel = row["channel"]
    priority = row["priority_score"]

    message = MESSAGE_TEMPLATES.get(action, "").format(lead_id=lead_id)

    if channel == "whatsapp":
        status = send_whatsapp(lead_id, message)
    elif channel == "call":
        status = make_call(lead_id, message)
    else:
        status = "skipped"

    logs.append({
        "lead_id": lead_id,
        "action": action,
        "channel": channel,
        "priority_score": priority,
        "status": status,
        "timestamp": datetime.now()
    })


# 5. Save Outreach Logs
log_df = pd.DataFrame(logs)
log_df.to_csv("outreach_logs.csv", index=False)

print("Outreach execution completed 🚀")
