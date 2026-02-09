function calculate() {
    fetch('/api/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            manual_minutes: Number(document.getElementById('manual_minutes').value),
            frequency: document.getElementById('frequency').value,
            users: Number(document.getElementById('users').value),
            dev_hours: Number(document.getElementById('dev_hours').value),
            maintenance_hours: Number(document.getElementById('maintenance_hours').value),
            cost_per_hour: Number(document.getElementById('cost_per_hour').value)
        })
    })
    .then(response => response.json())
    .then(data => {
        let diffText = data.difference >= 0
            ? "Monthly Savings: ₹" + data.difference
            : "Monthly Loss: ₹" + Math.abs(data.difference);

        document.getElementById('result').innerHTML =
            "<strong>Cost Comparison (Per Month)</strong><br>" +
            "Manual Cost: ₹" + data.manual_cost + "<br>" +
            "Automation Cost: ₹" + data.automation_cost + "<br>" +
            diffText + "<br><br>" +
            "ROI: " + data.roi + "%<br>" +
            "Decision: <strong>" + data.decision + "</strong>";
    })
    .catch(() => {
        document.getElementById('result').innerText = "Error calculating result";
    });
}
