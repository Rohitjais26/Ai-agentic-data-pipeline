import pandas as pd

df = pd.read_csv("final_ready_for_outreach.csv")
print("Loaded successfully")

#print("Shape:", df.shape)

#Making the segment columns
df["user_segment"] = "General_Active"

# 1. segment: Ready_To_Enroll
df.loc[
    (df["user_status"] == "Active") &
    (df["priority"] == "High") &
    (df["current_stage"].isin(["Interested", "Registered"])),
    "user_segment"
] = "Ready_To_Enroll"
print("Ready_To_Enroll")

# Phase 2: Post-drop segmentation (only if data exists)
if df["drop_reason"].notna().any():

    df.loc[
        (df["user_status"] == "Dropped") &
        (df["drop_reason"] == "Docs pending"),
        "user_segment"
    ] = "Docs_Support_Needed"

    df.loc[
        (df["user_status"] == "Dropped") &
        (df["drop_reason"] == "OTP failed"),
        "user_segment"
    ] = "OTP_or_Tech_Issue"

    df.loc[
        (df["user_status"] == "Dropped") &
        (df["drop_reason"].isin(["Lost interest", "No response"])),
        "user_segment"
    ] = "Low_Interest"

    df.loc[
        (df["user_status"] == "Dropped") &
        (df["drop_reason"] == "Phone unreachable"),
        "user_segment"
    ] = "Unreachable"



print("\nUser Segment Distribution:")
print(df["user_segment"].value_counts())


print(df.to_csv("segmented_users.csv", index=False))

print("/n Segmentation Completeed ")