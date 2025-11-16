# backend/ml/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score
import joblib
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "ml", "model_store")
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "rf_model.joblib")
FEATURE_ORDER = ["attendance_rate", "avg_assignment_score", "midterm_score", "missing_assignments", "participation", "lms_hours"]


def load_data(csv_path):
    df = pd.read_csv(csv_path)
    # assume csv has all features + 'passed' 1/0
    df = df.dropna(subset=FEATURE_ORDER + ["passed"])
    X = df[FEATURE_ORDER].astype(float)
    y = df["passed"].astype(int)
    return X, y


def train(csv_path):
    X, y = load_data(csv_path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    print(classification_report(y_test, preds))
    # save model
    joblib.dump(clf, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to training CSV")
    args = parser.parse_args()
    train(args.csv)
