from flask import Flask, render_template, jsonify
import requests
from config import CLIENT_ID, ACCESS_TOKEN, BASE_URL

app = Flask(__name__)

HEADERS = {
    "access-token": ACCESS_TOKEN,
    "client-id": CLIENT_ID,
    "Content-Type": "application/json"
}

# ==============================
# DHAN API FUNCTIONS
# ==============================

def fetch_orders():
    return requests.get(f"{BASE_URL}/orders", headers=HEADERS).json()

def fetch_trades():
    return requests.get(f"{BASE_URL}/trades", headers=HEADERS).json()

def fetch_positions():
    return requests.get(f"{BASE_URL}/positions", headers=HEADERS).json()

def fetch_holdings():
    return requests.get(f"{BASE_URL}/holdings", headers=HEADERS).json()

def get_kill_switch_status():
    return requests.get(f"{BASE_URL}/killSwitch", headers=HEADERS).json()

def activate_kill_switch():
    return requests.post(f"{BASE_URL}/killSwitch", headers=HEADERS).json()

def deactivate_kill_switch():
    return requests.delete(f"{BASE_URL}/killSwitch", headers=HEADERS).json()

# ==============================
# P&L CALCULATION
# ==============================

def calculate_pnl_summary():
    positions = fetch_positions()

    open_pnl = 0
    realized_pnl = 0

    if isinstance(positions, list):
        for pos in positions:
            open_pnl += float(pos.get("unrealizedProfit", 0))
            realized_pnl += float(pos.get("realizedProfit", 0))

    total_pnl = open_pnl + realized_pnl

    return {
        "open_pnl": round(open_pnl, 2),
        "realized_pnl": round(realized_pnl, 2),
        "total_pnl": round(total_pnl, 2)
    }

def fetch_profile():
    try:
        response = requests.get(f"{BASE_URL}/profile", headers=HEADERS, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# ==============================
# ROUTES
# ==============================

@app.route("/")
def dashboard():
    profile = fetch_profile()
    name = profile.get("dhanClientId", "Trader")
    return render_template("dashboard.html", name=name)

@app.route("/api/orders")
def api_orders():
    return jsonify(fetch_orders())

@app.route("/api/trades")
def api_trades():
    return jsonify(fetch_trades())

@app.route("/api/positions")
def api_positions():
    return jsonify(fetch_positions())

@app.route("/api/holdings")
def api_holdings():
    return jsonify(fetch_holdings())

@app.route("/api/kill-status")
def api_kill_status():
    return jsonify(get_kill_switch_status())

@app.route("/api/kill-activate", methods=["POST"])
def api_kill_activate():
    return jsonify(activate_kill_switch())

@app.route("/api/kill-deactivate", methods=["POST"])
def api_kill_deactivate():
    return jsonify(deactivate_kill_switch())

@app.route("/api/pnl-summary")
def api_pnl_summary():
    return jsonify(calculate_pnl_summary())

@app.route("/api/profile")
def api_profile():
    return jsonify(fetch_profile())

# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":
    app.run(debug=True)