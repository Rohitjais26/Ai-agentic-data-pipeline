
# SEGMENTATION LAYER
# Internship AI Agentic Project


import pandas as pd


# 1. Load Clean Dataset

df = pd.read_csv("clean_full_dataset.csv")

print("Clean dataset loaded")
print("Rows:", df.shape[0])



# 2. Text Normalization Helper

def normalize_text(series):
    """
    Normalizes text for consistent rule matching.
    """
    return (
        series
        .astype(str)
        .str.strip()
        .str.lower()
    )


# 3. Core Segment Columns

df["user_status_seg"] = normalize_text(df["user_status"])
df["drop_category_seg"] = normalize_text(df["drop_category"])

print("Core segments created")



# 4. Funnel Stage Segmentation

def assign_funnel_stage(row):
    """
    Assigns a controlled funnel stage based on current_stage.
    Dropped users are handled separately.
    """
    stage = str(row["current_stage"]).strip().lower()

    if stage in ["new", "lead"]:
        return "new"
    elif stage in ["interested", "inquiry"]:
        return "interested"
    elif stage in ["registered", "application_submitted"]:
        return "registered"
    elif stage in ["enrolled", "joined"]:
        return "enrolled"
    else:
        return "unknown"


df["funnel_stage_seg"] = df.apply(assign_funnel_stage, axis=1)



# 5. Freeze Funnel Stage for Dropped Users

df.loc[df["user_status_seg"] == "dropped", "funnel_stage_seg"] = "dropped"

print("Funnel stage segmentation completed")



# 6. Value Tier Segmentation

df["value_tier"] = pd.cut(
    df["benefit_score"],
    bins=[-1, 50, 70, 85, 100],
    labels=["Low", "Medium", "High", "Very High"]
)

# Normalize casing for consistency
df["value_tier"] = df["value_tier"].astype(str).str.lower()

print("Value tier segmentation completed")


# 7. Segmentation Validation (Sanity Checks)

print("\nUser Status Distribution:")
print(df["user_status_seg"].value_counts())

print("\nFunnel Stage Distribution:")
print(df["funnel_stage_seg"].value_counts())

print("\nValue Tier Distribution:")
print(df["value_tier"].value_counts())



# 8. Export Segmented Dataset
df.to_csv("segmented_dataset.csv", index=False)

print("\nSegmented dataset saved successfully 🚀")

