# train_diabetes_model.py
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Binarizer
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd

# Load the diabetes dataset
data = load_diabetes(as_frame=True)
X = data.data
y_continuous = data.target

# Convert regression target to binary (for classification)
# 1 if target > 140, else 0
binarizer = Binarizer(threshold=140)
y = binarizer.fit_transform(y_continuous.values.reshape(-1, 1)).ravel()

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model
joblib.dump(model, "diabetes_model.pkl")
joblib.dump(list(X.columns), "feature_names.pkl")
