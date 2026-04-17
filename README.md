Rothschild NIDS

A Real-Time Network Intrusion Detection System

---

 About the Project

Rothschild NIDS is a real-time network intrusion detection system built to simulate how a modern Security Operations Center (SOC) monitors and detects suspicious activity.

The goal of this project was to go beyond a basic ML model and build a complete pipeline — from data ingestion to detection, alerting, and visualization.

It processes network-like traffic, classifies it using a machine learning model, stores the results, and displays everything in an interactive dashboard.

---

 What it does

- Simulates real-time network traffic
- Cleans and preprocesses incoming data
- Uses a trained ML model to classify traffic (normal vs attack)
- Stores logs and alerts in a database
- Displays results on a SOC-style dashboard

---

Tech Stack

- Backend: Flask
- Database: SQLite (SQLAlchemy ORM)
- Machine Learning: Random Forest (scikit-learn)
- Frontend: HTML, CSS, JavaScript
- Authentication: Flask-Login
- Streaming: Custom event pipeline

---

 Project Structure

Rothschild-NIDS/
│
├── app/                # Flask app (routes, services)
├── dashboard/          # UI (templates + static files)
├── database/           # Models, DB config, CRUD
├── detection/          # ML detection logic
├── streaming/          # Real-time processing
├── models/             # Trained model + dataset
├── utils/              # Helpers & logging
├── run.py              # Entry point
└── create_user.py      # Create login user

---

 How to Run

1. Clone the repository

 git clone https://github.com/venkatnikhil616/Rothschild-NIDS.git                             
 cd Rothschild-NIDS

---

2. Create virtual environment

python3 -m venv venv
source venv/bin/activate

---

3. Install dependencies

pip install -r requirements.txt --break-system-packages

---

4. Clear Python cache

find . -name "__pycache__" -type d -exec rm -r {} +

This step avoids old cached files causing import errors.

---

5. Train the model 

python -m models.train_model

This generates:

- "model.pkl"
- "scaler.pkl"
- "encoder.pkl"

---

6. Start the app (initializes database)

python run.py

Stop it once (CTRL+C) after DB is created. db.py will be created 

---

7. Create a user

python create_user.py
if you want you can register your username and password by modifying the code.

--- 

8. Run the project

python run.py

---

 Login

Use the username and password you created using "create_user.py".

---

 Dashboard

After logging in, you’ll see:

- Live traffic logs
- Attack alerts
- Radar visualization
- Matrix-style animated background

---

 Notes

- Traffic is simulated (not real packet capture yet)
- Alerts depend on model predictions
- Make sure you train the model before running
- The Network scanner is refreshed automatically after every 5 seconds.

---

 Future Improvements

- Real packet sniffing (Scapy integration)
- WebSocket-based real-time dashboard
- Advanced attack classification (DoS, Probe, etc.)
- Geo-IP visualization
- Improved anomaly scoring

---

 Why I Built This

I wanted to build something closer to a real-world cybersecurity system rather than just a standalone ML model.

This project helped me understand how backend systems, machine learning, and visualization come together in a practical scenario.

---

👨‍💻
Author

Built as a hands-on cybersecurity + machine learning project.

---

Support

If you found this useful, consider giving it a star or building on top of it.
