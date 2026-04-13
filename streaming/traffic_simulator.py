import time
import random
import threading
from typing import Dict, Generator, Optional
from datetime import datetime


class TrafficSimulator:
    """
    Simulates real-time network traffic for NIDS testing
    """

    def __init__(self, interval: float = 2.0, max_events: Optional[int] = None):
        self.interval = interval
        self.max_events = max_events
        self._running = False
        self._thread = None

        # Predefined realistic values
        self.protocols = ["tcp", "udp", "icmp"]
        self.services = ["http", "ftp", "smtp", "domain_u", "eco_i"]
        self.flags = ["SF", "S0", "REJ", "RSTR"]

    # GENERATE SINGLE TRAFFIC EVENT

    def generate_event(self) -> Dict:
        return {
            "duration": random.randint(0, 10),
            "protocol_type": random.choice(self.protocols),
            "service": random.choice(self.services),
            "flag": random.choice(self.flags),
            "src_bytes": random.randint(0, 5000),
            "dst_bytes": random.randint(0, 5000),
            "wrong_fragment": 0,
            "urgent": 0,
            "hot": random.randint(0, 5),
            "num_failed_logins": random.randint(0, 3),
            "logged_in": random.randint(0, 1),
            "num_compromised": random.randint(0, 2),
            "root_shell": 0,
            "su_attempted": 0,
            "num_root": random.randint(0, 2),
            "num_file_creations": random.randint(0, 2),
            "num_shells": 0,
            "num_access_files": random.randint(0, 2),
            "num_outbound_cmds": 0,
            "is_host_login": 0,
            "is_guest_login": random.randint(0, 1),
            "count": random.randint(1, 100),
            "srv_count": random.randint(1, 100),
            "serror_rate": round(random.uniform(0, 1), 2),
            "srv_serror_rate": round(random.uniform(0, 1), 2),
            "rerror_rate": round(random.uniform(0, 1), 2),
            "srv_rerror_rate": round(random.uniform(0, 1), 2),
            "same_srv_rate": round(random.uniform(0, 1), 2),
            "diff_srv_rate": round(random.uniform(0, 1), 2),
            "srv_diff_host_rate": round(random.uniform(0, 1), 2),
            "timestamp": datetime.utcnow().isoformat()
        }

    # GENERATOR (STREAM)
  
    def stream(self) -> Generator[Dict, None, None]:
        count = 0

        while self._running:
            event = self.generate_event()
            yield event

            count += 1
            if self.max_events and count >= self.max_events:
                break

            time.sleep(self.interval)

    # START STREAM (THREAD)
  
    def start(self, callback):
        """
        Start streaming in a separate thread

        callback: function to process each event
        """
        if self._running:
            print("⚠️ Simulator already running")
            return

        self._running = True

        def run():
            print("🚀 Traffic simulation started...")
            try:
                for event in self.stream():
                    callback(event)
            except Exception as e:
                print(f"[SIMULATOR ERROR] {str(e)}")
            finally:
                self._running = False
                print("🛑 Traffic simulation stopped")

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()
      
    # STOP STREAM
  
    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
