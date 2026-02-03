
# METRICS & FEEDBACK LOOP
# Internship AI Agentic Project

import pandas as pd



# 1. Load Outreach Logs
logs = pd.read_csv("outreach_logs.csv")

print("Outreach logs loaded")
print("Total executions:", logs.shape[0])


# 2. Basic Data Prep
logs["timestamp"] = pd.to_datetime(logs["timestamp"])



# 3. Action Distribution
action_distribution = logs["action"].value_counts()
print("\nAction Distribution:")
print(action_distribution)


# 4. Channel Effectiveness
channel_distribution = logs["channel"].value_counts()
print("\nChannel Usage:")
print(channel_distribution)


# 5. Call Outcome Analysis
call_logs = logs[logs["channel"] == "call"]

call_outcomes = call_logs["status"].value_counts(normalize=True) * 100
print("\nCall Outcome Percentage:")
print(call_outcomes.round(2))



# 6. Priority vs Outcome
priority_outcome = (
    logs
    .groupby("priority_score")["status"]
    .value_counts(normalize=True)
    .unstack()
    .fillna(0) * 100
)

print("\nPriority vs Outcome (%):")
print(priority_outcome.round(2))


# 7. Time-based Analysis
logs["hour"] = logs["timestamp"].dt.hour

hourly_activity = logs["hour"].value_counts().sort_index()
print("\nHourly Execution Distribution:")
print(hourly_activity)


# 8. Export Metrics
action_distribution.to_csv("metrics_action_distribution.csv")
channel_distribution.to_csv("metrics_channel_usage.csv")
call_outcomes.to_csv("metrics_call_outcomes.csv")
priority_outcome.to_csv("metrics_priority_outcomes.csv")
hourly_activity.to_csv("metrics_hourly_activity.csv")

print("\nMetrics exported successfully 🚀")
