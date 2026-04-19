import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# ---------------- SYNTHETIC DATA ----------------
np.random.seed(42)
n = 500

df = pd.DataFrame({
    "age": np.random.randint(21, 60, n),
    "experience": np.random.randint(1, 20, n),
    "department": np.random.choice(["HR", "IT", "Sales"], n),
    "salary": np.random.randint(20000, 150000, n),
    "training_hours": np.random.randint(5, 100, n),
    "projects": np.random.randint(1, 10, n),
    "attendance": np.random.uniform(0.6, 1.0, n),
    "feedback_score": np.random.uniform(1, 5, n)
})

df["performance"] = np.where(
    (df["feedback_score"] > 4) & (df["attendance"] > 0.9),
    "High",
    np.where(df["feedback_score"] > 3, "Medium", "Low")
)

le_dep = LabelEncoder()
le_perf = LabelEncoder()

df["department"] = le_dep.fit_transform(df["department"])
df["performance"] = le_perf.fit_transform(df["performance"])

X = df.drop("performance", axis=1)
y = df["performance"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

joblib.dump(model, "model.pkl")
joblib.dump(le_dep, "le_department.pkl")
joblib.dump(le_perf, "le_performance.pkl")

print("Model trained successfully")