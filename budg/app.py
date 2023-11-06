from flask import Flask, render_template, request, redirect, url_for
from budg.core import get_dollar_value, calculate as budg_calculate

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("submit.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    plan = request.args.get("plan")
    amount = request.args.get("amount")
    amount_val = get_dollar_value(amount)
    table = budg_calculate(plan, amount_val)
    table_lines = table.split("\n")
    return str.join("<br>", table_lines)

    # return render_template("result.html", table_lines=table_lines)

if __name__ == "__main__":
    app.run(debug=True)
