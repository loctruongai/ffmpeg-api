FROM python:3.10-slim

WORKDIR /app

# Cài ffmpeg và dependencies
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Cài Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ project
COPY . .

# Chạy app bằng Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
