import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

np.random.seed(42)

# Synthetic dataset
data = pd.DataFrame({
    "amount": np.random.lognormal(mean=7, sigma=0.5, size=2000),
    "hour": np.random.randint(0, 24, 2000),
    "tx_count_24h": np.random.poisson(3, 2000)
})

# Scale data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

# Isolation Forest
model = IsolationForest(n_estimators=200, contamination=0.04, random_state=42)
model.fit(X_scaled)

# Save model & scaler
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✔ FraudSense AI model trained successfully")

