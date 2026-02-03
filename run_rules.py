# =========================================
# RULE ENGINE RUNNER (V1 / V2 SWITCH)
# AI Agentic Project
# =========================================

import pandas as pd

# -----------------------------------------
# CONFIGURATION SWITCH
# -----------------------------------------
USE_CONFIG_RULES = True   # True = YAML (V2), False = Hardcoded (V1)

SEGMENTED_DATA_PATH = "data/clean/segmented_dataset.csv"
OUTPUT_PATH = "data/clean/action_queue.csv"


# -----------------------------------------
# LOAD DATA
# -----------------------------------------
df = pd.read_csv(SEGMENTED_DATA_PATH)

print("Segmented dataset loaded")
print("Rows:", df.shape[0])


# -----------------------------------------
# INITIALIZE DECISION COLUMNS
# -----------------------------------------
df["next_action"] = "no_action"
df["channel"] = "none"
df["priority_score"] = 0


# -----------------------------------------
# EXECUTE RULE ENGINE
# -----------------------------------------
if USE_CONFIG_RULES:
    print("Using CONFIG-DRIVEN RULE ENGINE (V2)")

    from engine.rule_engine_v2_config import RuleEngine

    engine = RuleEngine("config/rules.yaml")

    # Apply rules in correct order
    df = engine.apply_base_priority(df)
    df = engine.apply_value_boost(df)
    df = engine.apply_rules(df)

else:
    print("Using HARDCODED RULE ENGINE (V1)")

    from rules.rules_engine_v1_hardcoded import apply_rules_v1

    df = apply_rules_v1(df)


# -----------------------------------------
# CONSENT SAFETY GUARD (MANDATORY)
# -----------------------------------------
df.loc[df["consent_status"] != "Consented", ["next_action", "channel"]] = ["no_action", "none"]
df.loc[df["consent_status"] != "Consented", "priority_score"] = 0


# -----------------------------------------
# FINAL ACTION QUEUE
# -----------------------------------------
action_queue = (
    df[df["next_action"] != "no_action"]
    .sort_values(by="priority_score", ascending=False)
    [["lead_id", "next_action", "channel", "priority_score"]]
)

action_queue.to_csv(OUTPUT_PATH, index=False)

print("Action queue generated successfully 🚀")
print("Total actionable leads:", action_queue.shape[0])
