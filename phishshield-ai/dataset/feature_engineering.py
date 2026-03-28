from urllib.parse import urlparse

def extract_features(url):

    parsed = urlparse(url)

    features = {
        "url_length": len(url),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_slashes": url.count("/"),
        "num_question": url.count("?"),
        "num_equal": url.count("="),
        "num_at": url.count("@"),
        "has_https": 1 if "https" in url else 0,
        "domain_length": len(parsed.netloc)
    }

    return list(features.values())
