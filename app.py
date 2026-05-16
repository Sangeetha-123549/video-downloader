from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    data = request.json
    url = data.get("url")

    def run_progress():

        # 🔥 REAL progress loop
        for i in range(1, 101):

            time.sleep(0.05)  # simulate speed

            socketio.emit("progress_update", {
                "progress": i
            })

        # 🔥 FINAL COMPLETE EVENT
        socketio.emit("download_complete", {
            "status": "success"
        })

    thread = threading.Thread(target=run_progress)
    thread.start()

    return jsonify({"status": "started"})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)