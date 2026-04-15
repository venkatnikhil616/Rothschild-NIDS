import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# ---------------------------
# PATHS ✅ FIXED
# ---------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset.csv")   # ✅ your current dataset
MODEL_DIR = BASE_DIR

MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "encoder.pkl")

# ---------------------------
# LOAD DATA
# ---------------------------

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"❌ Dataset not found at {DATA_PATH}")

    print("Reading from:", DATA_PATH)

    df = pd.read_csv(DATA_PATH)

    if df.empty:
        raise ValueError("❌ Dataset is empty")

    print(f"✅ Dataset loaded: {df.shape[0]} rows")

    return df


# ---------------------------
# PREPROCESS
# ---------------------------

def preprocess(df):
    df = df.copy()

    # Rename target if needed
    if "attack_type" in df.columns:
        df.rename(columns={"attack_type": "label"}, inplace=True)

    if "label" not in df.columns:
        raise ValueError("❌ Dataset must contain 'label' or 'attack_type'")

    # Fill missing
    df.fillna(0, inplace=True)

    # Encode categorical columns (safe)
    for col in ["protocol_type", "service", "flag"]:
        if col in df.columns:
            df[col] = df[col].astype(str).astype("category").cat.codes

    # Split
    X = df.drop(columns=["label"])
    y = df["label"]

    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    return X, y_encoded, label_encoder


# ---------------------------
# TRAIN MODEL
# ---------------------------

def train_model():
    print("📥 Loading dataset...")
    df = load_data()

    print("⚙️ Preprocessing...")
    X, y, encoder = preprocess(df)

    print("🔀 Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    print("📏 Scaling...")
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    print("🤖 Training model...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    print("📊 Evaluating...")
    y_pred = model.predict(X_test)

    print("\nAccuracy:", accuracy_score(y_test, y_pred))
    print("\nReport:\n", classification_report(y_test, y_pred))

    # Save
    print("💾 Saving model...")
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)

    with open(ENCODER_PATH, "wb") as f:
        pickle.dump(encoder, f)

    print("\n✅ DONE — Model Ready!")
    print("📁 Saved in:", MODEL_DIR)


# ---------------------------
# RUN
# ---------------------------

if __name__ == "__main__":
    train_model()
