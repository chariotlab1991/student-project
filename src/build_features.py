import pandas as pd, numpy as np

students = pd.read_csv("data/students.csv")
courses = pd.read_csv("data/courses.csv")
enrollments = pd.read_csv("data/enrollments.csv")
agg = pd.read_csv("data/agg_events.csv")
outcomes = pd.read_csv("data/outcomes.csv")

df = (enrollments
      .merge(students, left_on="student_id", right_on="id", how="left")
      .merge(courses, left_on="course_id", right_on="id", how="left", suffixes=("","_crs"))
      .merge(agg, on=["student_id","course_id"], how="left")
      .merge(outcomes, on=["student_id","course_id"], how="left"))

df = df.fillna(0)

num_cols = ["age","est_hours","secs_total","active_days","avg_quiz_delta","quiz_count"]
cat_cols = ["locale","device_type","subject","level","cohort"]

X_num = df[num_cols].astype(float)
X_cat = pd.get_dummies(df[cat_cols], drop_first=True)

X = np.hstack([X_num.to_numpy(), X_cat.to_numpy()])
y_mastery = df["final_mastery_pct"].to_numpy()
y_dropout = df["dropped"].astype(int).to_numpy()

np.savez("data/features_mastery.npz", X=X, y=y_mastery)
np.savez("data/features_dropout.npz", X=X, y=y_dropout)
