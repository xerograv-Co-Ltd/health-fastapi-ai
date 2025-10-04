import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("data/poc_divelog.csv")
df = df[df["label"].notnull() & (df["label"] != "")]

X = df[["heart_rate", "oxygen_saturation", "temperature", "depth", "max_percent_m"]].fillna(0)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("✅ Train accuracy:", model.score(X_train, y_train))
print("✅ Test accuracy:", model.score(X_test, y_test))

joblib.dump(model, "risk_model.pkl")
print("📦 Model saved to risk_model.pkl")
