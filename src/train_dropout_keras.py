import numpy as np, tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

d = np.load("data/features_dropout.npz", allow_pickle=True)
X, y = d["X"], d["y"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

sc = StandardScaler(with_mean=False)
Xtr = sc.fit_transform(Xtr).astype("float32")
Xte = sc.transform(Xte).astype("float32")

model = tf.keras.Sequential([
  tf.keras.layers.Input(shape=(Xtr.shape[1],)),
  tf.keras.layers.Dense(128, activation="relu"),
  tf.keras.layers.Dropout(0.3),
  tf.keras.layers.Dense(64, activation="relu"),
  tf.keras.layers.Dense(1, activation="sigmoid")
])
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy", "AUC"])
model.fit(Xtr, ytr, epochs=15, batch_size=32, validation_split=0.2, verbose=0)
print("Keras test metrics:", model.evaluate(Xte, yte, verbose=0))
