from firebase_admin import credentials, firestore, initialize_app
import pandas as pd

# Firebase初期化
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

# DiveSessionデータ取得
sessions_ref = db.collection_group("divesessions")
docs = sessions_ref.stream()

rows = []
for doc in docs:
    data = doc.to_dict()
    if data.get("labelSource") != "manual":
        continue
    for s in data.get("dcSamplesInline", []):
        max_pct = max([t.get("pctM", 0.0) for t in s.get("tissues", [])])
        rows.append({
            "heart_rate": s.get("hr"),
            "depth": s.get("depthM"),
            "max_percent_m": max_pct,
            "label": data.get("riskLevel")
        })

df = pd.DataFrame(rows)
df.dropna(inplace=True)

# 特徴量とターゲット分離
X = df[["heart_rate", "depth", "max_percent_m"]]
y = df["label"]

# データ分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# モデル学習
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 評価出力
y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("📊 Classification Report:\n", classification_report(y_test, y_pred))

# 保存
joblib.dump(model, args.output)
print(f"✅ Model saved to {args.output}")
