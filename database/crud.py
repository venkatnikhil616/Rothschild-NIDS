from sqlalchemy import func
from database.models import Log, Alert
from database.db import SessionLocal


# =========================
# INSERT LOG
# =========================
def insert_log(data: dict):
    session = SessionLocal()
    try:
        # 🔒 Filter only valid columns
        allowed_fields = {c.name for c in Log.__table__.columns}
        filtered_data = {k: v for k, v in data.items() if k in allowed_fields}

        log = Log(**filtered_data)
        session.add(log)
        session.commit()
        session.refresh(log)
        return log

    except Exception as e:
        session.rollback()
        print(f"DB Insert Error: {e}")
        return None

    finally:
        session.close()


# =========================
# INSERT ALERT
# =========================
def insert_alert(data: dict):
    session = SessionLocal()
    try:
        allowed_fields = {c.name for c in Alert.__table__.columns}
        filtered_data = {k: v for k, v in data.items() if k in allowed_fields}

        alert = Alert(**filtered_data)
        session.add(alert)
        session.commit()
        session.refresh(alert)
        return alert

    except Exception as e:
        session.rollback()
        print(f"DB Alert Insert Error: {e}")
        return None

    finally:
        session.close()


# =========================
# GET RECENT LOGS
# =========================
def get_recent_logs(limit: int = 20):
    session = SessionLocal()
    try:
        logs = (
            session.query(Log)
            .order_by(Log.timestamp.desc())
            .limit(limit)
            .all()
        )
        return logs or []

    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []

    finally:
        session.close()


# =========================
# GET RECENT ALERTS
# =========================
def get_recent_alerts(limit: int = 20):
    session = SessionLocal()
    try:
        alerts = (
            session.query(Alert)
            .order_by(Alert.timestamp.desc())
            .limit(limit)
            .all()
        )
        return alerts or []

    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return []

    finally:
        session.close()


# =========================
# GET ATTACK STATS (FINAL)
# =========================
def get_attack_stats():
    session = SessionLocal()
    try:
        stats = (
            session.query(Log.attack_type, func.count(Log.id))
            .group_by(Log.attack_type)
            .all()
        )

        # Convert to dict
        result = {attack: count for attack, count in stats}

        total = sum(result.values())
        normal = result.get("normal", 0)
        attacks = total - normal

        return {
            "total": total,
            "attacks": attacks,
            "normal": normal,
            "details": result
        }

    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {
            "total": 0,
            "attacks": 0,
            "normal": 0,
            "details": {}
        }

    finally:
        session.close()
