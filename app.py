
from flask import Flask, request, send_file, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return open('index.html').read()

@app.route('/download', methods=['POST'])
def download_video():
    import tempfile
    import os

    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
        output_file = tmp_file.name

    ydl_opts = {
        'outtmpl': output_file,
        'format': 'best[ext=mp4]/best',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        response = send_file(output_file, as_attachment=True)
        # Cleanup after sending
        @response.call_on_close
        def cleanup():
            try:
                os.remove(output_file)
            except Exception:
                pass
        return response
    except Exception as e:
        if os.path.exists(output_file):
            os.remove(output_file)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
