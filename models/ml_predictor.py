import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


def add_features(df):
    """
    Feature engineering — create smart inputs for the ML model.
    Uses lag features (past demand) which you know from regression!
    """
    df = df.copy()
    df["lag_1h"]  = df["demand"].shift(1).fillna(0)   # 1 hour ago
    df["lag_3h"]  = df["demand"].shift(3).fillna(0)   # 3 hours ago
    df["lag_24h"] = df["demand"].shift(24).fillna(0)  # same hour yesterday
    df["lag_168h"]= df["demand"].shift(168).fillna(0) # same hour last week
    df["rolling_mean_6h"] = (
        df["demand"].rolling(6).mean().fillna(0)       # 6hr average
    )
    return df


FEATURES = [
    "hour_of_day", "day_of_week", "is_weekend",
    "is_holiday", "active_devices",
    "lag_1h", "lag_3h", "lag_24h", "lag_168h",
    "rolling_mean_6h"
]


def train(df):
    """Train Random Forest demand predictor."""
    df = add_features(df)

    X = df[FEATURES]
    y = df["demand"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
        # shuffle=False keeps time order intact — important for time series!
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1        # use all CPU cores
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse  = np.sqrt(mean_squared_error(y_test, preds))
    r2    = r2_score(y_test, preds)

    print(f"\n[ML] Model trained on {len(X_train)} samples")
    print(f"[ML] RMSE : {rmse:.2f} requests")
    print(f"[ML] R²   : {r2:.4f}")
    print(f"[ML] Feature importances:")
    for feat, imp in sorted(
        zip(FEATURES, model.feature_importances_),
        key=lambda x: -x[1]
    )[:5]:
        print(f"     {feat:<22} {imp:.3f}")

    return model, df, X_test, y_test, preds