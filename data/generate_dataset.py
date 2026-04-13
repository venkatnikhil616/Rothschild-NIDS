import pandas as pd                                   
import random
import os

OUTPUT_PATH = "data/raw/nsl_kdd.csv"
                                                   
protocols = ["tcp", "udp", "icmp"]
services = ["http", "ftp", "smtp", "domain_u", "eco_i"]
flags = ["SF", "S0", "REJ", "RSTR"]

labels = ["normal", "neptune", "smurf", "guess_passwd", "warezclient"]


def generate_row():
    return {
        "duration": random.randint(0, 10),
        "protocol_type": random.choice(protocols),
        "service": random.choice(services),
        "flag": random.choice(flags),
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
        "label": random.choice(labels)
    }


def generate_dataset(n=1000):
    data = [generate_row() for _ in range(n)]
    df = pd.DataFrame(data)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f" Dataset generated at {OUTPUT_PATH} with {n} rows")

if __name__ == "__main__":
    generate_dataset(1500)
