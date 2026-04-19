import streamlit as st
import pandas as pd
import joblib
import sqlite3
import hashlib
import seaborn as sns
import matplotlib.pyplot as plt

# ================= CONFIG =================
st.set_page_config(page_title="HR Analytics System", layout="wide")

# ================= DATABASE =================
conn = sqlite3.connect("employee.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    security_question TEXT,
    security_answer TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    action TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    age INTEGER,
    experience INTEGER,
    department TEXT,
    salary INTEGER,
    training_hours INTEGER,
    projects INTEGER,
    attendance REAL,
    feedback_score REAL,
    prediction TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# ================= HELPERS =================
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def log(user, action):
    cursor.execute("INSERT INTO logs (username, action) VALUES (?,?)", (user, action))
    conn.commit()

def save_prediction(user, age, exp, dept, sal, train, proj, att, fb, pred):
    cursor.execute("""
    INSERT INTO predictions VALUES (NULL,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)
    """, (user, age, exp, dept, sal, train, proj, att, fb, pred))
    conn.commit()

def login(user, pwd):
    cursor.execute("SELECT password FROM users WHERE username=?", (user,))
    res = cursor.fetchone()
    if res and res[0] == hash_password(pwd):
        log(user, "LOGIN SUCCESS")
        return True
    log(user, "LOGIN FAILED")
    return False

# ================= DEFAULT USER =================
cursor.execute("SELECT * FROM users WHERE username='admin'")
if not cursor.fetchone():
    cursor.execute("""
    INSERT INTO users (username, password, security_question, security_answer)
    VALUES (?,?,?,?)
    """, ("admin", hash_password("admin123"), "Color?", hash_password("blue")))
    conn.commit()

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

# ================= LOGIN UI (PREMIUM DESIGN) =================
if not st.session_state.logged_in:

    st.markdown("""
    <style>
    .login-box {
        width: 420px;
        margin: auto;
        margin-top: 120px;
        padding: 35px;
        background: white;
        border-radius: 15px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.15);
    }

    .title {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #1f4e79;
    }

    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="title">🏢 HR Analytics Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Employee Performance System</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.user = username
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# ================= LOAD MODEL =================
model = joblib.load("model.pkl")
le_dep = joblib.load("le_department.pkl")
le_perf = joblib.load("le_performance.pkl")

# ================= SIDEBAR =================
st.sidebar.title("HR Panel")

if st.sidebar.button("Logout"):
    log(st.session_state.user, "LOGOUT")
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.write(f"User: {st.session_state.user}")

# ================= TABS =================
tab1, tab2, tab3, tab4 = st.tabs([
    "Predict", "CSV Upload", "Dashboard", "Logs"
])

# ================= PREDICTION =================
with tab1:

    st.header("Employee Performance Prediction")

    age = st.slider("Age", 21, 60, 30)
    exp = st.slider("Experience", 1, 20, 5)
    dept = st.selectbox("Department", ["HR","IT","Sales"])
    salary = st.number_input("Salary", 20000, 150000, 50000)
    training = st.slider("Training Hours", 5, 100, 20)
    projects = st.slider("Projects", 1, 10, 3)
    attendance = st.slider("Attendance", 0.6, 1.0, 0.8)
    feedback = st.slider("Feedback Score", 1.0, 5.0, 3.5)

    if st.button("Predict"):

        dept_enc = le_dep.transform([dept])[0]

        data = pd.DataFrame([[
            age, exp, dept_enc, salary,
            training, projects, attendance, feedback
        ]], columns=[
            "age","experience","department","salary",
            "training_hours","projects","attendance","feedback_score"
        ])

        pred = model.predict(data)[0]
        result = le_perf.inverse_transform([pred])[0]

        st.success(f"Prediction: {result}")

        save_prediction(
            st.session_state.user,
            age, exp, dept, salary,
            training, projects, attendance,
            feedback, result
        )

        log(st.session_state.user, "PREDICTION")

# ================= CSV UPLOAD =================
with tab2:

    st.header("Bulk Prediction")

    file = st.file_uploader("Upload CSV")

    if file:

        df = pd.read_csv(file)
        df["department"] = le_dep.transform(df["department"])

        preds = model.predict(df)
        df["Prediction"] = le_perf.inverse_transform(preds)

        st.dataframe(df)

        log(st.session_state.user, "CSV UPLOAD")

# ================= DASHBOARD (AUTO DB) =================
with tab3:

    st.header("Live HR Dashboard")

    cursor.execute("SELECT * FROM predictions")
    data = cursor.fetchall()

    if len(data) == 0:
        st.warning("No data yet")
    else:

        df = pd.DataFrame(data, columns=[
            "id","user","age","exp","dept","salary",
            "training","projects","attendance",
            "feedback","prediction","time"
        ])

        col1, col2, col3 = st.columns(3)
        col1.metric("Total", len(df))
        col2.metric("High", len(df[df["prediction"]=="High"]))
        col3.metric("Low", len(df[df["prediction"]=="Low"]))

        st.bar_chart(df["prediction"].value_counts())

        fig, ax = plt.subplots()
        sns.boxplot(x=df["prediction"], y=df["salary"], ax=ax)
        st.pyplot(fig)

        st.dataframe(df)

# ================= LOGS =================
with tab4:

    st.header("Activity Logs")

    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")
    logs = cursor.fetchall()

    df_logs = pd.DataFrame(logs, columns=["ID","User","Action","Time"])
    st.dataframe(df_logs)