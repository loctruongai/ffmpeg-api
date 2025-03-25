FROM python:3.10-slim

# Cài đặt ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Tạo thư mục làm việc
WORKDIR /app

# Copy mã nguồn
COPY . .

# Cài đặt thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Cổng để expose nếu dùng render
EXPOSE 8000

# Chạy API Flask
CMD ["python", "main.py"]
