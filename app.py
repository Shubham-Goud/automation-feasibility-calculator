from flask import Flask, request, jsonify, render_template, send_file
import sqlite3
import pandas as pd
import os

app = Flask(__name__)

DB_NAME = "calculator.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manual_cost REAL,
            automation_cost REAL,
            roi REAL,
            decision TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json

    manual_minutes = data['manual_minutes']
    frequency = data['frequency']
    users = data['users']
    dev_hours = data['dev_hours']
    maintenance_hours = data['maintenance_hours']
    cost_per_hour = data['cost_per_hour']

    if frequency == "Daily":
        runs = 22
    elif frequency == "Weekly":
        runs = 4
    else:
        runs = 1

    monthly_manual_hours = (manual_minutes * runs * users) / 60
    manual_cost = monthly_manual_hours * cost_per_hour

    automation_cost = ((dev_hours * cost_per_hour) / 12) + (maintenance_hours * cost_per_hour)

    difference = manual_cost - automation_cost
    roi = (difference / automation_cost) * 100

    if roi > 30:
        decision = "Automate"
    elif roi >= 10:
        decision = "Re-evaluate"
    else:
        decision = "Not Recommended"

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO calculations (manual_cost, automation_cost, roi, decision) VALUES (?, ?, ?, ?)",
        (manual_cost, automation_cost, roi, decision)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "manual_cost": round(manual_cost, 2),
        "automation_cost": round(automation_cost, 2),
        "difference": round(difference, 2),
        "roi": round(roi, 2),
        "decision": decision
    })

@app.route('/export')
def export_excel():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM calculations", conn)
    conn.close()

    os.makedirs("exports", exist_ok=True)
    file_path = "exports/results.xlsx"
    df.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
