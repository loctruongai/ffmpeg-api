from flask import Flask, request, send_file, jsonify
import os
import uuid
import subprocess

app = Flask(__name__)

@app.route('/kenburns', methods=['POST'])
def create_kenburns_video():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image_filename = f"{uuid.uuid4()}.jpg"
    image_path = os.path.join('/tmp', image_filename)
    image_file.save(image_path)

    video_filename = image_filename.replace('.jpg', '.mp4')
    video_path = os.path.join('/tmp', video_filename)

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

    try:
        print("👉 Running FFmpeg command:", " ".join(ffmpeg_cmd))
        subprocess.run(ffmpeg_cmd, check=True)
        print("✅ FFmpeg finished processing.")
    except subprocess.CalledProcessError as e:
        print("❌ FFmpeg error:", e)
        return jsonify({'error': f'FFmpeg failed: {str(e)}'}), 500

    return send_file(video_path, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
