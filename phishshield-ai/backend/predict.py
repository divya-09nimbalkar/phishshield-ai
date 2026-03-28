from backend.utils import predict_url

def get_prediction(url):

    result = predict_url(url)

    if result == "phishing":
        return {
            "url": url,
            "prediction": "Phishing Website",
            "status": "Danger"
        }

    else:
        return {
            "url": url,
            "prediction": "Legitimate Website",
            "status": "Safe"
        }
