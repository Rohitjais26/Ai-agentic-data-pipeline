import pandas as pd
df = pd.read_excel("ai_agent_dummy_dataset_500_leads.xlsx")
#print(df.head())          #Gives the header name only 
#print(df.shape)           #Give the size of dataset ()
#print(df.head)           #Give the whole header name 
#print(df.columns)        #Give the whole columns names
#print(df["state"])       #Gives only the whole info about state column
#print(df.loc[0])         #Gives the info about a specific Row


#Filtering of Data 
#let take example about bihar 
bihar_df = df[df["state"] == "Bihar"]  #Declaring specialy for bihar state
print(bihar_df)

print(bihar_df.shape)
print(bihar_df.columns)


print(df[df["age"] > 21])         #this is for where age > 21 in whole dataset
print(df[df["age"] < 21])

#Condition filtering
eligible_df = df[
    (df["has_whatsapp"] == "Y") &
    (df["consent_status"] == "Consented")
]


eligible_df.to_csv("eligible_for_whatsapp.csv", index=False)
print("Total  youth eligible for WhatsApp:",
      len(eligible_df))



#Finding Bihar youth whi are undergraduate and uses Whatsapp (Practise Purpose)
bihar_youth_whatsapp_df = df[
    (df["state"] == "Bihar") &
    (df["has_whatsapp"] == "Y") &
    (df["consent_status"] == "Consented") &
    (df["age"] >= 18) &
    (df["age"] <= 35)&
    (df["education_level"] == "Undergraduate")
]


bihar_youth_whatsapp_df.to_csv(
    "bihar_youth_eligible_for_graduate_ug.csv",
    index=False
    )

print("Total Bihar youth eligible for WhatsApp:",
      len(bihar_youth_whatsapp_df))

#Missing Value
print(df.isna().sum())


#Making a new column for age 
df["age_group"] = "unknown"
print(df[["age","age_group"]].head())

df.loc[df["age"] <= 21 , "age_group"] = "18-21"   #making the youth age under 18-21
df.loc[
    (df["age"] >=22) & (df["age"] <=25), "age_group"
] = "22-25"

df.loc[df["age"] > 25, "age_group"] = "26+"

print(df[["age", "age_group"]].head(10))


#Making column for 'priority'
df["priority"] = "Normal"

df.loc[
    (df["benefit_score"] >= 7) &
    (df["has_whatsapp"] == "Y") &
    (df["consent_status"] == "Consented"),
    "priority"
] = "High"

print(df["priority"].value_counts())

df_sorted = df.sort_values(by="benefit_score", ascending=False)
print(df_sorted[["lead_id", "benefit_score"]].head(10))

df["priority_rank"] = 0
df.loc[df["priority"] == "High", "priority_rank"] = 1   #whose priority is high rank them 1

#If drop_reason is EMPTY → user is active
#If drop_reason has value → user dropped
df["user_status"] = "Active"
df.loc[df["drop_reason"].notna(), "user_status"] = "Dropped"
print(df["user_status"].value_counts())


#Sorting using two columns- "priority_rank", "benefits_score"
df_sorted = df.sort_values(
    by=["priority_rank", "benefit_score"],
    ascending=[False, False]
)

print(df_sorted[
    ["lead_id", "priority", "benefit_score"]
].head(15)
)



ready_df = df_sorted[
    (df_sorted["has_whatsapp"] == "Y") &
    (df_sorted["consent_status"] == "Consented") &
    (df_sorted["user_status"] == "Active")
]


print(ready_df.shape)
print(ready_df.head())

#Save the final clear dataset
print(ready_df.to_csv("final_ready_for_outreach.csv", index=False))



