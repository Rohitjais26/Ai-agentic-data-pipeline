import pandas as pd

df = pd.read_excel("ai_agent_dummy_dataset_500_leads.xlsx")
#print("Dataset Loaded successfully ")

"""print(df.head())          #Gives the header name only 
print(df.shape)           #Give the size of dataset ()
print(df.head)           #Give the whole header name 
print(df.columns)        #Give the whole columns names
print(df["state"])       #Gives only the whole info about state column
print(df.loc[0])         #Gives the info about a specific Row"""


df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

#Checking for  Duplicated Data 
#print(df.duplicated().sum())


# STEP 4: Normalize YES / NO fields
yes_no_map = {
    "y": "Y",
    "yes": "Y",
    "true": "Y",
    "n": "N",
    "no": "N",
    "false": "N"
}

df["has_whatsapp"] = (
    df["has_whatsapp"]
    .astype(str)
    .str.lower()
    .map(yes_no_map)
)

#print(df.isna().sum())


# STEP 5: Handle Missing Values (Logical Defaults)
df["drop_reason"] = df["drop_reason"].fillna("")
df["education_level"] = df["education_level"].fillna("Unknown")
df["state"] = df["state"].fillna("Unknown")
df["consent_status"] = df["consent_status"].fillna("Not Consented")

#print("Missing values after handling:")
#print(df.isna().sum())



# STEP 6: Age Validation (Eligibility Control)

df = df[df["age"].between(15, 35)]
df["age"] = df["age"].astype(int)


# Age group
df["age_group"] = pd.cut(
    df["age"],
    bins=[14, 21, 25, 35],
    labels=["18-21", "22-25", "26+"]
)

# STEP 8: Drop Reason Segmentation (CORE UPGRADE)

# Preserve raw text
df["drop_reason_raw"] = df["drop_reason"]

# Clean text
df["drop_reason_clean"] = (
    df["drop_reason_raw"]
    .str.lower()
    .str.strip()
)

# Define controlled categories
drop_reason_map = {
    "no documents": "Documentation",
    "missing documents": "Documentation",

    "not interested": "Interest",
    "lost interest": "Interest",

    "language issue": "Language",

    "financial issue": "Financial",

    "busy": "Follow-up Needed",
    "call later": "Follow-up Needed",

    "phone switched off": "Contact Issue",
    "wrong number": "Contact Issue"
}

df["drop_category"] = df["drop_reason_clean"].map(drop_reason_map)
df["drop_category"] = df["drop_category"].fillna("None")


# STEP 9: User Status (Active vs Dropped)
df["user_status"] = "Active"
df.loc[df["drop_reason_raw"] != "", "user_status"] = "Dropped"

# STEP 10: Priority Logic (Business Rules)
df["priority"] = "Normal"

high_priority_mask = (
    (df["benefit_score"] >= 7) &
    (df["has_whatsapp"] == "Y") &
    (df["consent_status"] == "Consented") &
    (df["user_status"] == "Active")
)

df.loc[high_priority_mask, "priority"] = "High"

# Numeric rank for sorting / ML
df["priority_rank"] = df["priority"].map({
    "High": 1,
    "Normal": 0
})

#print("Priority distribution:")
#print(df["priority"].value_counts())

# STEP 11: Recovery Strategy Mapping (Agent Brain)
strategy_map = {
    "Documentation": "Explain documents + checklist",
    "Language": "Switch to local language",
    "Financial": "Highlight free/subsidy benefits",
    "Follow-up Needed": "Schedule reminder",
    "Contact Issue": "Try alternate channel",
    "Interest": "Soft re-engagement",
    "None": "No action needed"
}

df["recovery_strategy"] = df["drop_category"].map(strategy_map)

# STEP 12: Dropout Risk (Analytics Layer)
risk_map = {
    "Documentation": "Medium",
    "Language": "Medium",
    "Financial": "High",
    "Follow-up Needed": "Low",
    "Contact Issue": "High",
    "Interest": "High",
    "None": "Low"
}

df["dropout_risk"] = df["drop_category"].map(risk_map)

# STEP 13: Sort for Outreach Priority
df_sorted = df.sort_values(
    by=["priority_rank", "benefit_score"],
    ascending=[False, False]
)


ready_df = df_sorted[
    (df_sorted["has_whatsapp"] == "Y") &
    (df_sorted["consent_status"] == "Consented") &
    (df_sorted["user_status"] == "Active")
]

print("Final outreach dataset shape:", ready_df.shape)

df.to_csv("clean_full_dataset.csv", index=False)
ready_df.to_csv("full_final_ready_for_outreach.csv", index=False)

print(" Data cleaning & segmentation pipeline completed successfully.")