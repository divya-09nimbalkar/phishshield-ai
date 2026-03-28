from urllib.parse import urlparse

def extract_features(url):

    parsed = urlparse(url)

    features = {}

    features["url_length"] = len(url)
    features["num_dots"] = url.count(".")
    features["num_hyphens"] = url.count("-")
    features["num_slashes"] = url.count("/")
    features["num_question"] = url.count("?")
    features["num_equal"] = url.count("=")
    features["num_at"] = url.count("@")
    features["has_https"] = 1 if "https" in url else 0
    features["domain_length"] = len(parsed.netloc)

    return list(features.values())
