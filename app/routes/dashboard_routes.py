import os
from flask import Blueprint, render_template
from database.crud import get_recent_logs, get_attack_stats, get_recent_alerts

# ✅ DEFINE FIRST
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    template_folder=os.path.join(BASE_DIR, "dashboard/templates"),
    static_folder=os.path.join(BASE_DIR, "dashboard/static"),
    static_url_path="/dashboard/static"
)

# ✅ THEN USE IT
@dashboard_bp.route("/")
def dashboard():
    logs = get_recent_logs()
    stats = get_attack_stats()
    alerts = get_recent_alerts()

    # ✅ FIX JSON ISSUE
    alerts_data = []
    for a in alerts:
        alerts_data.append({
            "attack_type": a.attack_type or "unknown",
            "severity": (a.severity or "LOW").upper(),
            "confidence": getattr(a, "confidence", 0),
            "timestamp": str(a.timestamp)
        })

    return render_template(
        "index.html",
        logs=logs,
        stats=stats,
        alerts=alerts_data
    )
