import pandas as pd

try:
    file_path = "../Task_1/clean_students.csv"

    df = pd.read_csv(file_path)

    print("\nclean_students.csv loaded successfully")
    print(df.head())# displays only first n rows, by default 5

    # passed column
    df["passed"] = df["score"] >= 50

    # score category 'High' (≥80), 'Medium' (50–79), 'Low' (<50)
    def score_category(score):
        if score>=80:
            return "High"
        elif score>=50:
            return "Medium"
        else:
            return "Low"
        
    df["score_category"] = df["score"].apply(score_category)

    # ranking students
    df["rank"] = df["score"].rank(ascending=False,method="min").astype(int)

    # group by grade
    print("\nGRADE SUMMARY")
    grade_summary = df.groupby("grade").agg(
        count=("score", "count"),
        mean_score=("score", "mean"),
        min_score=("score", "min"),
        max_score=("score", "max")
    )

    print(grade_summary)

    # adding subject column
    subjects = [
    "Math",
    "Science",
    "English",
    "Computer",
    "Physics"
    ]

    # Repeat subjects for all rows
    df["subject"] = [
        subjects[i % len(subjects)]
        for i in range(len(df))
    ]

    # pivot table
    print("\nPIVOT TABLE\n")

    pivot_table = pd.pivot_table(
        df,
        values="score",
        index="grade",
        columns="subject",
        aggfunc="mean",
        fill_value=0
    )

    print(pivot_table)

    # sort by rank and reset index
    df = df.sort_values(by="rank").reset_index(drop=True)

    print("\nFINAL DATAFRAME INFO")
    print(df.info())

    # save enriched CSV
    output_file = "enriched_students.csv"
    df.to_csv(output_file, index=False)

    print("\nEnriched CSV saved successfully!")
    print(f"File Name: {output_file}")

    # Print Top 5 Ranked Students
    print("\nTOP 5 RANKED STUDENTS: \n")
    print(df.head(5))

except Exception as e:
    print(f"Unexpected Error: {e}")