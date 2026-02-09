# =========================================
# LLM MESSAGE GENERATOR
# =========================================

from llm.prompt_templates import documentation_prompt, interest_prompt
from llm.llm_client import call_llm


def generate_message(action, lead_row):
    """
    Generates AI message based on action & lead context.
    """

    lead_context = {
        "funnel_stage": lead_row["funnel_stage_seg"],
        "value_tier": lead_row["value_tier"],
        "language": lead_row.get("language", "english")
    }

    if action == "send_document_checklist":
        prompt = documentation_prompt(lead_context)

    elif action == "soft_reengagement":
        prompt = interest_prompt(lead_context)

    else:
        return None  # No AI needed

    response = call_llm(prompt)
    return response
