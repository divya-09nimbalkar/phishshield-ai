from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "PhishShield API Running"}

@app.post("/predict")
def predict(data: dict):

    url = data.get("url","").lower()

    phishing_keywords = [
        "login",
        "signin",
        "verify",
        "update",
        "secure",
        "account",
        "bank",
        "password",
        "confirm",
        "wallet",
        "paypal",
        "amazon",
        "ebay"
    ]

    if any(word in url for word in phishing_keywords):
        prediction = "Phishing Website"
    else:
        prediction = "Legitimate Website"

    print(f"Checked URL: {url} → {prediction}")

    return {"prediction": prediction}