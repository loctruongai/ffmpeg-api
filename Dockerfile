FROM python:3.10-slim

# Cài ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "main.py"]
