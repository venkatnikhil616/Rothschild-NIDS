import os
from flask import Blueprint, render_template
from flask_login import login_required
from database.crud import get_recent_logs, get_attack_stats, get_recent_alerts

# ---------------------------
# BASE DIR
# ---------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# ---------------------------
# BLUEPRINT
# ---------------------------
dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    template_folder=os.path.join(BASE_DIR, "dashboard/templates"),
    static_folder=os.path.join(BASE_DIR, "dashboard/static"),
    static_url_path="/dashboard/static"
)


# ---------------------------
# MAIN DASHBOARD
# ---------------------------
@dashboard_bp.route("/")
@login_required
def dashboard():
    logs = get_recent_logs()
    stats = get_attack_stats()
    alerts = get_recent_alerts()

    # ✅ FORMAT ALERTS (safe for JSON)
    alerts_data = [
        {
            "attack_type": a.attack_type or "unknown",
            "severity": (a.severity or "LOW").upper(),
            "confidence": getattr(a, "confidence", 0),
            "timestamp": str(a.timestamp)
        }
        for a in alerts
    ]

    return render_template(
        "index.html",
        logs=logs,
        stats=stats,
        alerts=alerts_data
    )


# ---------------------------
# 🔥 LIVE DATA API (REQUIRED)
# ---------------------------
@dashboard_bp.route("/dashboard_data")
@login_required
def dashboard_data():
    logs = get_recent_logs()
    stats = get_attack_stats()
    alerts = get_recent_alerts()

    # ✅ SERIALIZE LOGS
    logs_data = [
        {
            "attack_type": l.attack_type or "unknown",
            "confidence": l.confidence or 0,
            "timestamp": str(l.timestamp)
        }
        for l in logs
    ]

    # ✅ SERIALIZE ALERTS
    alerts_data = [
        {
            "attack_type": a.attack_type or "unknown",
            "severity": (a.severity or "LOW").upper(),
            "confidence": getattr(a, "confidence", 0),
            "timestamp": str(a.timestamp)
        }
        for a in alerts
    ]

    # ✅ SAFE STATS (matches frontend)
    stats_data = {
        "total": stats.get("total", 0),
        "attacks": stats.get("attacks", 0),
        "normal": stats.get("normal", 0)
    }

    return {
        "logs": logs_data,
        "alerts": alerts_data,
        "stats": stats_data
    }
