

# DATA CLEANING PIPELINE
# Internship AI Agentic Project


import pandas as pd

# -----------------------------------------
# 1. Load Raw Dataset
# -----------------------------------------
df = pd.read_excel("ai_agent_dummy_dataset_500_leads.xlsx")

print("Dataset loaded successfully")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# -----------------------------------------
# 2. Normalize Column Names
# -----------------------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("Column names normalized")


# -----------------------------------------
# 3. Duplicate Check (No Removal)
# -----------------------------------------
print("Duplicate rows found:", df.duplicated().sum())


# -----------------------------------------
# 4. Normalize YES / NO Fields
# -----------------------------------------
yes_no_map = {
    "y": "Y",
    "yes": "Y",
    "true": "Y",
    "1": "Y",
    "n": "N",
    "no": "N",
    "false": "N",
    "0": "N"
}

df["has_whatsapp"] = (
    df["has_whatsapp"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map(yes_no_map)
    .fillna("N")
)

print("YES/NO fields normalized")


# -----------------------------------------
# 5. Handle Missing Values (Safe Defaults)
# -----------------------------------------
df["education_level"] = df["education_level"].fillna("Unknown")
df["state"] = df["state"].fillna("Unknown")
df["consent_status"] = df["consent_status"].fillna("Not Consented")
df["drop_reason"] = df["drop_reason"].fillna("")

print("Missing values handled")


# -----------------------------------------
# 6. Age Cleaning (NO FILTERING)
# -----------------------------------------
df["age"] = df["age"].astype(int)

df["age_group"] = pd.cut(
    df["age"],
    bins=[0, 17, 21, 25, 35, 100],
    labels=["<18", "18-21", "22-25", "26-35", "36+"]
)

print("Age cleaned (no rows removed)")


# -----------------------------------------
# 7. Drop Reason Cleaning (Semantic Prep)
# -----------------------------------------
df["drop_reason_raw"] = df["drop_reason"]

df["drop_reason_clean"] = (
    df["drop_reason_raw"]
    .astype(str)
    .str.strip()
    .str.lower()
)

drop_reason_map = {
    "no documents": "documentation",
    "missing documents": "documentation",
    "not interested": "interest",
    "lost interest": "interest",
    "language issue": "language",
    "financial issue": "financial",
    "busy": "follow-up needed",
    "call later": "follow-up needed",
    "phone switched off": "contact issue",
    "wrong number": "contact issue"
}

df["drop_category"] = df["drop_reason_clean"].map(drop_reason_map)

print("Drop reason standardized (no forced default)")


# -----------------------------------------
# 8. User Status (Core Semantic Column)
# -----------------------------------------
df["user_status"] = "active"
df.loc[df["drop_reason_raw"] != "", "user_status"] = "dropped"

print("User status assigned")


# -----------------------------------------
# 9. Final Dataset Check
# -----------------------------------------
print("Final dataset shape:", df.shape)
print(df["user_status"].value_counts())


# -----------------------------------------
# 10. Export Clean Dataset
# -----------------------------------------
df.to_csv("clean_full_dataset.csv", index=False)

print("Clean dataset saved successfully 🚀")
