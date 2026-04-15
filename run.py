import threading

from app.main import create_app
from streaming.traffic_simulator import TrafficSimulator
from streaming.stream_processor import StreamProcessor
from database.db import init_db
from utils.logger import log_info, log_error
from utils.constants import DEFAULT_STREAM_INTERVAL


# ---------------------------
# CREATE APP
# ---------------------------
app = create_app()


# ---------------------------
# SIMULATION THREAD
# ---------------------------
def start_simulation():
    try:
        simulator = TrafficSimulator(interval=DEFAULT_STREAM_INTERVAL)
        processor = StreamProcessor()

        log_info("📡 Starting traffic simulation...")
        simulator.start(processor.process_event)

    except Exception as e:
        log_error(f"Simulation failed: {str(e)}")


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    # Init DB
    init_db()
    log_info("✅ Database initialized")

    # Start simulation
    sim_thread = threading.Thread(target=start_simulation, daemon=True)
    sim_thread.start()

    # Run Flask
    app.run(host="0.0.0.0", port=5000, debug=True)
