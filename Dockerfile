FROM python:3.9-slim

WORKDIR /app

COPY . /app

# Install the required version of libstdc++
# RUN apt-get update && apt-get install -y libstdc++6

RUN pip install -r requirements.txt

CMD ["uvicorn", "klingon_transcribe.server:app", "--host", "0.0.0.0", "--port", "8000"]
