import requests

def read(url):
    """Read audio file from HTTP URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def write(url, data):
    """Write data to HTTP URL."""
    response = requests.put(url, data=data)
    response.raise_for_status()
