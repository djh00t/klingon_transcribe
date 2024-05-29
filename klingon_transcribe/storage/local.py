def read(file_path):
    """Read audio file from local storage."""
    with open(file_path, 'rb') as f:
        audio_data = f.read()
    return audio_data

def write(file_path, data):
    """Write data to local storage."""
    with open(file_path, 'wb') as f:
        f.write(data)
