
from flask import Flask, render_template, request, send_file
import pandas as pd
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        urban_pop = float(request.form["urban_pop"])
        rural_pop = float(request.form["rural_pop"])
        urban_lpcd = float(request.form["urban_lpcd"])
        rural_lpcd = float(request.form["rural_lpcd"])
        growth = float(request.form["growth"])
        years = int(request.form["years"])

        future_urban = urban_pop * ((1 + growth/100) ** years)
        future_rural = rural_pop * ((1 + growth/100) ** years)

        urban_demand = future_urban * urban_lpcd / 1000
        rural_demand = future_rural * rural_lpcd / 1000
        total_demand = urban_demand + rural_demand

        esr_capacity = total_demand * 0.4
        discharge = total_demand / 24
        pipe_diameter = math.sqrt((4 * discharge) / (3.14 * 1)) * 1000

        # Bar Chart
        plt.figure()
        plt.bar(["Urban", "Rural"], [urban_demand, rural_demand])
        plt.xlabel("Category")
        plt.ylabel("Water Demand (m3/day)")
        plt.title("Urban vs Rural Water Demand")
        chart_path = "static/chart.png"
        plt.savefig(chart_path)
        plt.close()

        # Excel file
        data = {
            "Category": ["Urban", "Rural", "Total"],
            "Demand (m3/day)": [urban_demand, rural_demand, total_demand]
        }
        df = pd.DataFrame(data)
        excel_path = "static/water_demand.xlsx"
        df.to_excel(excel_path, index=False)

        result = {
            "urban_demand": round(urban_demand,2),
            "rural_demand": round(rural_demand,2),
            "total_demand": round(total_demand,2),
            "esr_capacity": round(esr_capacity,2),
            "pipe_diameter": round(pipe_diameter,2)
        }

    return render_template("index.html", result=result)

@app.route("/download")
def download():
    return send_file("static/water_demand.xlsx", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
