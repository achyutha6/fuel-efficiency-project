import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

try:
    from tensorflow import keras
    from tensorflow.keras import layers
except ImportError:
    import keras
    from keras import layers

# =========================
# LOAD DATASET
# =========================

df = pd.read_csv("auto-mpg.csv")

print("✅ Dataset Loaded")
print(df.head())

# =========================
# CLEAN DATA
# =========================

# Convert horsepower to numeric
df['horsepower'] = pd.to_numeric(
    df['horsepower'],
    errors='coerce'
)

# Fill missing horsepower values
df['horsepower'] = df['horsepower'].fillna(
    df['horsepower'].median()
)

# Remove missing rows
df = df.dropna()

# =========================
# FEATURES & TARGET
# =========================

X = df.drop(['mpg', 'car name'], axis=1)
y = df['mpg']

# Convert origin if categorical
if X['origin'].dtype == 'object':
    X['origin'] = X['origin'].astype(
        'category'
    ).cat.codes

# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================
# FEATURE SCALING
# =========================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save scaler
joblib.dump(scaler, "scaler.pkl")

print("✅ Scaler Saved")

# =========================
# BUILD MODEL
# =========================

model = keras.Sequential([

    layers.Input(shape=(X_train.shape[1],)),

    layers.Dense(
        128,
        activation='relu'
    ),

    layers.Dense(
        64,
        activation='relu'
    ),

    layers.Dense(1)

])

# =========================
# COMPILE MODEL
# =========================

model.compile(
    optimizer='adam',
    loss='mse',
    metrics=['mae']
)

# =========================
# TRAIN MODEL
# =========================

print("🚀 Training Started...")

history = model.fit(
    X_train,
    y_train,
    epochs=50,
    validation_split=0.2,
    verbose=1
)

# =========================
# SAVE MODEL
# =========================

model.save("fuel_efficiency_model.keras")

print("✅ Model Trained Successfully")
print("✅ Model Saved")