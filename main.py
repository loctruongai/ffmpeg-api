from flask import Flask, request, send_file
import os
import uuid
import subprocess

app = Flask(__name__)

# Route để test server còn sống
@app.route("/", methods=["GET"])
def home():
    return "✅ API is live!"

# Route xử lý Ken Burns effect
@app.route("/kenburns", methods=["POST"])
def create_kenburns_video():
    try:
        print("🔥 Nhận request mới...")

        if 'image' not in request.files:
            print("❌ Không tìm thấy file 'image' trong request.")
            return {'error': 'No image uploaded'}, 400

        # Lưu ảnh vào thư mục tạm
        image_file = request.files['image']
        image_filename = f"{uuid.uuid4()}.jpg"
        image_path = os.path.join('/tmp', image_filename)
        image_file.save(image_path)
        print(f"✅ File ảnh đã lưu: {image_path}")

        # Tạo đường dẫn video đầu ra
        video_filename = image_filename.replace('.jpg', '.mp4')
        video_path = os.path.join('/tmp', video_filename)

        # Lệnh ffmpeg để tạo Ken Burns effect
        ffmpeg_cmd = [
            'ffmpeg',
            '-y',
            '-loop', '1',
            '-i', image_path,
            '-filter_complex', 'zoompan=z=\'min(zoom+0.0005,1.5)\':d=180:s=1080x1920',
            '-c:v', 'libx264',
            '-t', '6',
            '-pix_fmt', 'yuv420p',
            video_path
        ]

        print("🚀 Đang chạy ffmpeg...")
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"🎉 Tạo xong video: {video_path}")

        return send_file(video_path, mimetype='video/mp4')

    except subprocess.CalledProcessError as e:
        print("❌ Lỗi khi chạy ffmpeg:", e)
        return {'error': 'ffmpeg failed', 'details': str(e)}, 500
    except Exception as e:
        print("❌ Lỗi không xác định:", e)
        return {'error': 'Internal Server Error', 'details': str(e)}, 500

# Khởi chạy Flask khi chạy trực tiếp
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
