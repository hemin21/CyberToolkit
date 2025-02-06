import requests
import whois
import tldextract
from urllib.parse import urlparse

def is_https(url):
    """Check if the URL uses HTTPS."""
    return url.startswith("https://")

def has_suspicious_keywords(url):
    """Check if the URL contains suspicious keywords."""
    suspicious_keywords = ['login', 'secure', 'account', 'signin', 'verify', 'update', 'free']
    # Avoid flagging legitimate websites (e.g., Instagram, Facebook) by checking the domain
    domain = tldextract.extract(url).domain
    if domain in ['instagram', 'facebook', 'google']:
        return False  # Ignore legit domains like Instagram
    for keyword in suspicious_keywords:
        if keyword in url.lower():
            return True
    return False

def is_newly_registered(url):
    """Check if the domain is newly registered."""
    domain = tldextract.extract(url).domain
    try:
        domain_info = whois.whois(domain)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date and (2025 - creation_date.year) < 1:
            return True
    except Exception as e:
        return False
    return False

def url_length_check(url):
    """Check if the URL length is suspiciously long."""
    # Increase the length threshold to 200 characters (adjustable based on your needs)
    return len(url) > 200

def detect_phishing(url):
    """Analyze the URL for phishing risks."""
    print(f"Analyzing URL: {url}")
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        return "Invalid URL or network error."

    if not is_https(url):
        return "Suspicious: URL does not use HTTPS."

    if has_suspicious_keywords(url):
        return "Suspicious: URL contains potentially malicious keywords."

    if url_length_check(url):
        return "Suspicious: URL length is too long."

    if is_newly_registered(url):
        return "Suspicious: Domain was recently registered."

    return "The URL seems safe."

# Example usage
if __name__ == "__main__":
    url = input("Enter URL to check: ")
    result = detect_phishing(url)
    print(result)
