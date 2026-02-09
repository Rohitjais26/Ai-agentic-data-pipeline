# =========================================
# PROMPT TEMPLATES
# =========================================

def documentation_prompt(lead_context):
    return f"""
You are a helpful education counsellor.

The student dropped because they did not submit documents.

Student details:
- Funnel stage: {lead_context['funnel_stage']}
- Value tier: {lead_context['value_tier']}
- Preferred language: {lead_context['language']}

Write a polite WhatsApp message asking them to submit documents.
Keep it short and friendly.
"""


def interest_prompt(lead_context):
    return f"""
You are a friendly education advisor.

The student lost interest.

Student details:
- Funnel stage: {lead_context['funnel_stage']}
- Value tier: {lead_context['value_tier']}

Write a soft re-engagement message.
Do not pressure the student.
"""
