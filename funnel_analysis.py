import pandas as pd


#importing clean csv file 
df = pd.read_csv("final_ready_for_outreach.csv")
#print("Clean datasett loaded") 

#print(df.shape)

#counting the stage 
funnel_stage = df["current_stage"].value_counts()
#print(funnel_stage)

#Ordered Funnel view
funnel_order = [
    "New",
    "Contacted",
    "Interested",
    "Registered",
    "Enrolled"
]

funnel_ordered = funnel_stage.reindex(funnel_order, fill_value=0)
#print(funnel_ordered)

#4. active vs Drop User
#print("\nUser Status Distribution:")
#print(df["user_status"].value_counts())

# 6. Funnel by Priority (Effectiveness Check)

print("\nFunnel by Priority:")
priority_funnel = (
    df.groupby("priority")["current_stage"]
    .value_counts()
)
print(priority_funnel)


# 7. Funnel by State 


"""print("\nFunnel by State (Top 10):")
state_funnel = (
    df.groupby("state")["current_stage"]
    .value_counts()
)
print(state_funnel.head(10))"""

funnel_ordered.to_csv("funnel_stage_counts.csv")
priority_funnel.to_csv("funnel_priority_stage_counts.csv")