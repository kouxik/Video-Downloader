
from flask import Flask, request, send_file, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return open('index.html').read()

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    output_file = 'downloaded_video.mp4'

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'outtmpl': output_file,
        'format': 'best[ext=mp4]/best',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(output_file, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
