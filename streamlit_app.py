import streamlit as st
import pandas as pd
import sqlite3
import os

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Automation Feasibility Calculator",
    layout="centered"
)

DB_NAME = "calculator.db"

# -------------------- DATABASE --------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manual_cost REAL,
            automation_cost REAL,
            difference REAL,
            roi REAL,
            decision TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_result(manual_cost, automation_cost, difference, roi, decision):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO calculations (manual_cost, automation_cost, difference, roi, decision) VALUES (?, ?, ?, ?, ?)",
        (manual_cost, automation_cost, difference, roi, decision)
    )
    conn.commit()
    conn.close()

def load_results():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM calculations", conn)
    conn.close()
    return df

# -------------------- APP UI --------------------
st.title("Automation Feasibility Calculator")
st.caption("Decision-support tool to evaluate whether a process is worth automating")

init_db()

st.subheader("Enter Process Details")

manual_minutes = st.number_input(
    "Manual effort per task (minutes)",
    min_value=1,
    step=1
)

frequency = st.selectbox(
    "Frequency",
    ["Daily", "Weekly", "Monthly"]
)

users = st.number_input(
    "Number of users",
    min_value=1,
    step=1
)

dev_hours = st.number_input(
    "Automation development effort (hours)",
    min_value=1,
    step=1
)

maintenance_hours = st.number_input(
    "Maintenance effort per month (hours)",
    min_value=0,
    step=1
)

cost_per_hour = st.number_input(
    "Cost per hour",
    min_value=1,
    step=50
)

# -------------------- CALCULATION --------------------
if st.button("Calculate Feasibility"):

    # Convert frequency to monthly runs
    if frequency == "Daily":
        runs = 22
    elif frequency == "Weekly":
        runs = 4
    else:
        runs = 1

    # Manual cost calculation
    manual_hours = (manual_minutes * runs * users) / 60
    manual_cost = manual_hours * cost_per_hour

    # Automation cost calculation
    automation_cost = ((dev_hours * cost_per_hour) / 12) + (maintenance_hours * cost_per_hour)

    # Difference & ROI
    difference = manual_cost - automation_cost
    roi = (difference / automation_cost) * 100

    # Decision logic
    if roi > 30:
        decision = "Automate"
        st.success("Decision: Automate")
    else:
        decision = "Not Recommended"
        st.error("Decision: Not Recommended")

    # Save to DB
    save_result(manual_cost, automation_cost, difference, roi, decision)

    # -------------------- OUTPUT --------------------
    st.subheader("Cost Comparison (Monthly)")

    st.write(f"**Manual Cost:** ₹{manual_cost:,.2f}")
    st.write(f"**Automation Cost:** ₹{automation_cost:,.2f}")

    if difference >= 0:
        st.write(f"**Monthly Savings:** ₹{difference:,.2f}")
    else:
        st.write(f"**Monthly Loss:** ₹{abs(difference):,.2f}")

    st.write(f"**ROI:** {roi:.2f}%")

# -------------------- EXPORT SECTION --------------------
st.divider()
st.subheader("Export Calculation History")

df = load_results()

if not df.empty:
    st.dataframe(df, use_container_width=True)

    excel_file = "automation_results.xlsx"
    df.to_excel(excel_file, index=False)

    with open(excel_file, "rb") as f:
        st.download_button(
            label="Download Excel Report",
            data=f,
            file_name="automation_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("No calculations available for export yet.")
