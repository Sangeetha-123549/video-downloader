from flask import Flask, request, jsonify, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

latest_file = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    global latest_file

    try:

        data = request.get_json()

        url = data["url"]

        ydl_opts = {
            "format": "best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            latest_file = ydl.prepare_filename(info)

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

    global latest_file

    try:

        return send_file(
            latest_file,
            as_attachment=True,
            download_name="video.mp4",
            mimetype="video/mp4"
        )

    except Exception as e:

        return str(e)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
