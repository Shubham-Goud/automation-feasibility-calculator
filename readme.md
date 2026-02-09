# Automation Feasibility Calculator

The Automation Feasibility Calculator is a decision-support tool designed to help teams evaluate whether a business process is worth automating. It compares the cost of performing a process manually with the cost of automation and provides a clear recommendation based on ROI.

---

## 🔗 Live Application (Streamlit Deployment)

👉 **Live Demo:**  
https://automation-feasibility-calculator-frvbnauwjdjx23app7wxgkr.streamlit.app/

The application is deployed using **Streamlit Cloud**, with source code hosted on GitHub.

---

## 📌 Problem Statement

In many organizations, teams initiate automation without evaluating its feasibility. As a result, they often face high automation costs, low ROI, and wasted development effort.  
Teams lack a structured, data-driven mechanism to determine whether a process is actually worth automating.

---

## 💡 Solution Overview

This project provides a simple and logical approach to evaluate automation feasibility by:
- Calculating monthly manual process cost
- Calculating monthly automation cost
- Comparing both costs
- Computing ROI
- Providing a clear recommendation:
  - **Automate**
  - **Not Recommended**

---

## ⚙️ Key Features

- Monthly manual cost calculation
- Monthly automation cost calculation
- Cost difference (savings or loss)
- ROI-based decision logic
- Result persistence using SQLite
- Excel export for reporting
- Deployed and accessible via Streamlit

---

## 🧮 Logic & Calculations

- **Manual Cost (Monthly):**  
  (Effort × Frequency × Users ÷ 60) × Cost per Hour

- **Automation Cost (Monthly):**  
  (Development Cost ÷ 12) + Monthly Maintenance Cost

- **ROI (%):**  
  (Manual Cost − Automation Cost) ÷ Automation Cost × 100

- **Decision Rule:**  
  - ROI > 30% → Automate  
  - ROI ≤ 30% → Not Recommended

---

## 🧠 Assumptions

- 22 working days per month
- Development cost amortized over 12 months
- Cost per hour remains constant
- Maintenance cost is recurring monthly

---

## 🛠️ Technologies Used

- **Programming Language:** Python  
- **Framework:** Streamlit  
- **Database:** SQLite  
- **Data Handling:** Pandas  
- **Reporting:** Excel (openpyxl)  
- **Version Control:** Git & GitHub  

All technologies used are as per the assignment guidelines.

---

## ▶️ How to Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
