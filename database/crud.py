from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Log
from database.db import SessionLocal                    

# INSERT LOG

def insert_log(data: dict):
    session = SessionLocal()

    try:
        log = Log(**data)
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


# GET RECENT LOGS

def get_recent_logs(limit: int = 20):
    session = SessionLocal()

    try:
        logs = (
            session.query(Log)
            .order_by(Log.timestamp.desc())
            .limit(limit)
            .all()
        )
        return logs

    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []

    finally:
        session.close()

# GET ATTACK STATS

def get_attack_stats():
    session = SessionLocal()

    try:
        stats = (
            session.query(Log.attack_type, func.count(Log.id))
            .group_by(Log.attack_type)
            .all()
        )

        return {attack: count for attack, count in stats}

    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {}

    finally:
        session.close()
