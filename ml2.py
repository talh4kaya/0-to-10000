import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns

df = pd.read_csv("cars.csv")

print(df.head())

print(df.describe,"\n\n\n",df.info())
df = df.dropna()

print()
print(df["origin"].unique())


from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df["origin_encoded"] = le.fit_transform(df["origin"])

print(df[["origin", "origin_encoded"]].head())


print(df)


from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Feature ve target seç
X = df.drop(columns=["mpg", "name","origin"])  
y = df["mpg"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeller
models = {
    "Linear Regression": LinearRegression(),
    "Ridge": Ridge(),
    "Lasso": Lasso(),
    "ElasticNet": ElasticNet(),
    "RandomForest": RandomForestRegressor(),
    "GradientBoosting": GradientBoostingRegressor()
}

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"{name} → MSE: {mse:.2f}, R²: {r2:.3f}")


from lazypredict.Supervised import LazyRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# NaN değerleri ortalama ile dolduralım
df = df.fillna(df.mean(numeric_only=True))

# Hedef değişken (örnek: mpg)
X = df.drop(["mpg", "name", "origin"], axis=1)
y = df["mpg"]

# Train-test ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1️⃣ Ham veri LazyPredict
print("📌 Ham veri ile LazyPredict sonuçları:")
reg = LazyRegressor(verbose=0, ignore_warnings=True)
models_raw, _ = reg.fit(X_train, X_test, y_train, y_test)

# 2️⃣ Standardize edilmiş veri LazyPredict
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n📌 Standardize edilmiş veri ile LazyPredict sonuçları:")
reg_scaled = LazyRegressor(verbose=0, ignore_warnings=True)
models_scaled, _ = reg_scaled.fit(X_train_scaled, X_test_scaled, y_train, y_test)

# 3️⃣ Yan yana karşılaştırma
comparison = pd.concat(
    [models_raw["R-Squared"], models_scaled["R-Squared"]],
    axis=1
)
comparison.columns = ["Raw R²", "Scaled R²"]

print("\n📊 Karşılaştırma Tablosu:")
print(comparison.sort_values("Scaled R²", ascending=False))
