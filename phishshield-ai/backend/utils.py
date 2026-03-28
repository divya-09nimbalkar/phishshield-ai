import pickle
from model.feature_extraction import extract_features

# Load trained model
model = pickle.load(open("model/phishing_model.pkl", "rb"))

def predict_url(url):

    features = extract_features(url)

    prediction = model.predict([features])[0]

    return prediction
