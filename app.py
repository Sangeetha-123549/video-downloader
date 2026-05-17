from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import time

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    filename = f"video_{int(time.time())}.mp4"

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/{filename}',
        'format': 'best'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return jsonify({"status": "success", "file": filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/file")
def file():
    files = sorted(os.listdir(DOWNLOAD_FOLDER), reverse=True)

    if len(files) == 0:
        return "Video not found", 404

    latest_file = files[0]
    return send_file(os.path.join(DOWNLOAD_FOLDER, latest_file), as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
