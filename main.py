from flask import Flask, request, send_file
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route('/kenburns', methods=['POST'])
def kenburns():
    try:
        if 'image' not in request.files:
            return {'error': 'No image uploaded'}, 400

        image_file = request.files['image']
        image_id = str(uuid.uuid4())
        image_path = f'/tmp/{image_id}.jpg'
        video_path = f'/tmp/{image_id}.mp4'

        image_file.save(image_path)

        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', image_path,
            '-filter_complex', 'zoompan=z=\'min(zoom+0.0005,1.5)\':d=180:s=1080x1920',
            '-c:v', 'libx264',
            '-t', '6',
            '-pix_fmt', 'yuv420p',
            video_path
        ]

        subprocess.run(ffmpeg_cmd, check=True)

        return send_file(video_path, mimetype='video/mp4')
    except Exception as e:
        return {'error': str(e)}, 500
