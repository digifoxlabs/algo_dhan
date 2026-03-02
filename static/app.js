function showData(data) {
    document.getElementById("output").innerText =
        JSON.stringify(data, null, 2);
}

// Data Loaders
function loadOrders() {
    fetch("/api/orders").then(res => res.json()).then(showData);
}

function loadTrades() {
    fetch("/api/trades").then(res => res.json()).then(showData);
}

function loadPositions() {
    fetch("/api/positions").then(res => res.json()).then(showData);
}

function loadHoldings() {
    fetch("/api/holdings").then(res => res.json()).then(showData);
}

// Kill Switch
function checkKillStatus() {
    fetch("/api/kill-status")
        .then(res => res.json())
        .then(data => {
            document.getElementById("killStatus").innerText =
                JSON.stringify(data);
        });
}

function activateKill() {
    fetch("/api/kill-activate", { method: "POST" })
        .then(res => res.json())
        .then(() => {
            alert("Kill Switch Activated");
            checkKillStatus();
        });
}

function deactivateKill() {
    fetch("/api/kill-deactivate", { method: "POST" })
        .then(res => res.json())
        .then(() => {
            alert("Kill Switch Deactivated");
            checkKillStatus();
        });
}

// P&L Summary
function loadPnlSummary() {
    fetch("/api/pnl-summary")
        .then(res => res.json())
        .then(data => {
            document.getElementById("openPnl").innerText = data.open_pnl;
            document.getElementById("realizedPnl").innerText = data.realized_pnl;

            let total = parseFloat(data.total_pnl);
            let totalEl = document.getElementById("totalPnl");

            totalEl.innerText = total;

            if (total > 0) {
                totalEl.style.color = "lime";
            } else if (total < 0) {
                totalEl.style.color = "red";
            } else {
                totalEl.style.color = "white";
            }
        });
}

// Auto Load
window.onload = function () {
    loadOrders();
    checkKillStatus();
    loadPnlSummary();

    setInterval(loadPnlSummary, 5000);
};