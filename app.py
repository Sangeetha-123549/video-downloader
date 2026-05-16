from flask import Flask, request, render_template, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

downloaded_file = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    global downloaded_file

    url = request.json["url"]

    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
        "format": "best"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        downloaded_file = filename

    return jsonify({"status": "done"})

@app.route("/file")
def file():
    return send_file(downloaded_file, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
