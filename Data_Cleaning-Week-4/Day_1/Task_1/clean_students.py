import pandas as pd

# load csv file into dataframe
df = pd.read_csv("messy_students.csv")

# print original data
print("\n Original Data")
print(df)

# show problems
print("\nData info")
print(df.info())

# show null values
print("\n Null values")
print(df.isnull().sum())

# show original raw count
before_rows = len(df)
print(before_rows)

# cleaning report counters
null_fixed = 0
duplicates_removed = 0
invalid_score_fixed = 0
whitespace_fixed = 0
casing_fixed = 0

# fix null values
# remove rows with missing student names
null_fixed = df["name"].isnull().sum()

df = df.dropna(subset=["name"]).reset_index(drop=True)

# fix whitespace in all string columns
before_whitespace = df.copy()

for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

whitespace_fixed = (
    before_whitespace.astype(str) != df.astype(str)
).sum().sum()

# fix casing
before_case = df["name"].copy()
df["name"] = df["name"].str.title()

casing_fixed = (before_case != df["name"]).sum()

# convert score to numeric
df["score"] = pd.to_numeric(df["score"], errors="coerce")

# count invlaid values
invalid_score_fixed = df["score"].isnull().sum()

# replace invalid scores with 0
df["score"] = df["score"].fillna(0)

# replace negative score with 0
negative_score = (df["score"]<0).sum()
df.loc[df["score"]<0, "score"] = 0

invalid_score_fixed += negative_score

# remove duplicates
before_duplicates = len(df)
df = df.drop_duplicates(subset=["name", "score"])

duplicates_removed = before_duplicates - len(df)

# reset student IDs
df = df.reset_index(drop=True)

df["id"] = range(1, len(df) + 1)

# ADD GRADE COLUMN
def calculate_grade(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "F"

df["grade"] = df["score"].apply(calculate_grade)

# save changed file
df.to_csv("clean_students.csv", index=False)

after_rows = len(df)

# FINAL OUTPUT
print("\nCLEANED DATA")
print(df)

print("\nCLEANING REPORT")
print(f"Null names fixed: {null_fixed}")
print(f"Whitespace issues fixed: {whitespace_fixed}")
print(f"Casing issues fixed: {casing_fixed}")
print(f"Invalid scores fixed: {invalid_score_fixed}")
print(f"Duplicate rows removed: {duplicates_removed}")

print("\nROW COUNT")
print(f"Before Cleaning: {before_rows}")
print(f"After Cleaning: {after_rows}")

print("\n Cleaned CSV saved as clean_students.csv")