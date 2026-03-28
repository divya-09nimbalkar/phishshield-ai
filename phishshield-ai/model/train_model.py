import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv(r"C:\Users\HP\Downloads\NIT_DATA_SCIENCE\AI-Phishing_detection\phishshield-ai\dataset\raw\phishing.csv")

print("Dataset Loaded")
print(data.head())

# Drop index column
data = data.drop(["Index"], axis=1)

# Features and label
X = data.drop("class", axis=1)
y = data["class"]

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier()

model.fit(X_train, y_train)

print("Model trained successfully")

# Save model
model_path = r"C:\Users\HP\Downloads\NIT_DATA_SCIENCE\AI-Phishing_detection\phishshield-ai\model\phishing_model.pkl"

pickle.dump(model, open(model_path, "wb"))

print("Model saved successfully at:")
print(model_path)