import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# 明示的にカンマ区切り（必要に応じて修正）
df = pd.read_csv("data/poc_divelog.csv", sep=",", engine="python")

# 列名が正しいかチェック
print("📊 Columns:", df.columns.tolist())

# label列が存在するか確認し、フィルタリング
if "label" not in df.columns:
    raise ValueError("❌ 'label' column not found in CSV")

df = df[df["label"].notnull() & (df["label"] != "")]

# 特徴量と目的変数
X = df[["heart_rate", "oxygen_saturation", "temperature", "depth", "max_percent_m"]].fillna(0)
y = df["label"]

# データ分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# モデル学習
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 精度確認
print("✅ Train accuracy:", model.score(X_train, y_train))
print("✅ Test accuracy:", model.score(X_test, y_test))

# モデル保存
joblib.dump(model, "risk_model.pkl")
print("📦 Model saved to risk_model.pkl")
