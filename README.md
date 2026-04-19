# employee-performance-predictor
AI-powered HR analytics system that predicts employee performance using machine learning, with explainable AI (SHAP), authentication, and real-time dashboard.

# 🏢 Employee Performance Predictor using Data Analytics

An end-to-end **HR Analytics and Machine Learning system** that predicts employee performance (High / Medium / Low) using behavioral, productivity, and engagement data.  
The system includes **authentication, real-time dashboard, SHAP explainability, and SQLite database tracking**.

---

## 🚀 Project Overview

This project simulates a real-world **HR decision support system** used in organizations to:

- Predict employee performance
- Identify high and low performers
- Support promotions and training decisions
- Improve workforce productivity
- Provide explainable AI insights (WHY a prediction was made)

---

## 🎯 Problem Statement

Companies struggle to:
- Identify employees who may underperform
- Understand reasons behind performance drop
- Make unbiased HR decisions
- Track employee performance consistently

👉 This project solves these problems using Machine Learning + Data Analytics.

---

## 🧠 Features

✔ Employee performance prediction (High / Medium / Low)  
✔ Secure login system (HR authentication)  
✔ SQLite database for storage  
✔ Activity logging system  
✔ Real-time HR dashboard  
✔ CSV bulk prediction  
✔ SHAP explainability (AI transparency)  
✔ Interactive Streamlit UI  

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas, NumPy
- Scikit-learn
- Matplotlib, Seaborn
- SHAP (Explainable AI)
- SQLite Database
- Joblib (Model persistence)

---

## 🏗️ System Architecture


User Login
↓
Employee Input / CSV Upload
↓
Data Preprocessing
↓
ML Model (Random Forest)
↓
Prediction (High / Medium / Low)
↓
SHAP Explainability
↓
SQLite Storage
↓
HR Dashboard Visualization


---

## 📊 Dataset Features

- Age
- Experience
- Department
- Salary
- Training Hours
- Projects Completed
- Attendance Rate
- Feedback Score

---

## ⚙️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-username/employee-performance-predictor.git
cd employee-performance-predictor
2. Create Virtual Environment
python -m venv venv
3. Activate Environment

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
4. Install Dependencies
pip install -r requirements.txt
▶️ Run Project
Step 1: Train Model
python train_model.py
Step 2: Run App
streamlit run app.py
🔐 Default Login
Username: admin
Password: admin123
📊 Dashboard Features
Total Employees analyzed
High / Medium / Low performers
Salary distribution analysis
Performance trends
Real-time logs
🧠 Explainable AI (SHAP)

This project uses SHAP to explain:

✔ Why an employee is marked High/Low performer
✔ Which features influenced the decision
✔ Feature contribution visualization

📸 Screenshots

(Add screenshots here)

Login Page
Dashboard
Prediction Page
SHAP Explanation Graph
📈 Business Impact
Improves HR decision-making
Reduces bias in evaluation
Helps in employee retention
Identifies training needs
Saves operational cost
🚀 Future Improvements
Deploy on cloud (Streamlit Cloud / AWS)
Add role-based access (HR/Admin/Manager)
Add email alerts for low performers
Integrate real HR dataset
Add deep learning model
👨‍💻 Author

Ishwari Belhekar
