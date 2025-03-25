# Base image
FROM python:3.10-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Expose port
EXPOSE 8000

# Run app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
