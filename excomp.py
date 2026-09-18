import pandas as pd

# =====================================================
# FILE PATHS
# =====================================================
file1_path = r"C:\Users\SutrayeSaiAkhil\OneDrive - alphastream.ai\Desktop\LPA TEST\before_Spot\AP Ulysses Co-Invest, L.P. - LPA (2nd A&R) (2021-03-08).xlsx"
file2_path = r"C:\Users\SutrayeSaiAkhil\OneDrive - alphastream.ai\Desktop\LPA TEST\after_spot\AP Ulysses Co-Invest, L.P. - LPA (2nd A&R) (2021-03-08).xlsx"
output_path = r"C:\Users\SutrayeSaiAkhil\OneDrive - alphastream.ai\Desktop\LPA TEST\after_spot\AP Ulysses Co-Investcomparison_output.xlsx"

# =====================================================
# STEP 1: READ EXCEL FILES
# =====================================================
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

# Normalize column names
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Rename value columns for clarity
df1 = df1.rename(columns={"Value": "Value_Excel_1"})
df2 = df2.rename(columns={"Value": "Value_Excel_2"})

# =====================================================
# STEP 2: MERGE ON SECTION + DATAPOINT
# =====================================================
merged_df = pd.merge(
    df1,
    df2,
    on=["Section", "Datapoint"],
    how="outer"
)

# =====================================================
# STEP 3: COMPARE VALUES
# =====================================================
def compare_values(row):
    v1 = row["Value_Excel_1"]
    v2 = row["Value_Excel_2"]

    if pd.isna(v1) and pd.notna(v2):
        return "ONLY_IN_EXCEL_2"
    if pd.notna(v1) and pd.isna(v2):
        return "ONLY_IN_EXCEL_1"
    if pd.isna(v1) and pd.isna(v2):
        return "BOTH_EMPTY"
    if str(v1).strip() == str(v2).strip():
        return "MATCH"
    return "MISMATCH"

merged_df["Compare_Result"] = merged_df.apply(compare_values, axis=1)

# =====================================================
# STEP 4: SORT FOR READABILITY
# =====================================================
merged_df = merged_df.sort_values(
    by=["Section", "Datapoint"],
    na_position="last"
)

# =====================================================
# STEP 5: SAVE OUTPUT
# =====================================================
merged_df.to_excel(output_path, index=False)

print("✅ Comparison completed successfully")
print(f"📄 Output saved to: {output_path}")
 