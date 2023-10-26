from flask import Flask, render_template, request, redirect, url_for
import budg

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("submit.html")

@app.route("/calculate")
def calculate():
    plan = request.args.get("plan")
    amount = request.args.get("amount")
    amount_val = budg.get_dollar_value(amount)
    table = budg.calculate(plan, amount_val)
    table_lines = table.split("\n")

    return render_template("result.html", table_lines=table_lines)

if __name__ == "__main__":
    app.run(debug=True)