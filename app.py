from flask import Flask, request, jsonify, render_template, send_file
import yt_dlp
import os
import glob

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    try:

        data = request.get_json()

        url = data["url"]

        ydl_opts = {
            "format": "best",
            "outtmpl": f"{DOWNLOAD_DIR}/video.%(ext)s",
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return jsonify({
            "status": "success"
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        })


@app.route("/file")
def file():

    files = glob.glob(f"{DOWNLOAD_DIR}/video.*")

    if not files:
        return "Video not found"

    return send_file(
        files[0],
        as_attachment=True,
        download_name="video.mp4",
        mimetype="video/mp4"
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
