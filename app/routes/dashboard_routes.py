from flask import Blueprint, render_template
from database.crud import get_recent_logs, get_attack_stats
                                                        dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    template_folder="../../dashboard/templates",
    static_folder="../../dashboard/static"              )


@dashboard_bp.route("/")
def dashboard():
    logs = get_recent_logs()
    stats = get_attack_stats()

    return render_template(
        "index.html",
        logs=logs,
        stats=stats
    )
