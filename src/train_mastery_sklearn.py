import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

d = np.load("data/features_mastery.npz", allow_pickle=True)
X, y = d["X"], d["y"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

pipe = Pipeline([("scaler", StandardScaler(with_mean=False)),
                 ("rf", RandomForestRegressor(n_estimators=200))])
pipe.fit(Xtr, ytr)
pred = pipe.predict(Xte)
rmse = mean_squared_error(yte, pred) ** 0.5
print("RMSE:", rmse)
print("R²:", r2_score(yte, pred))
