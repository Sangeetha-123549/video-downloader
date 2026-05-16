from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

progress = {"value": 0}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    progress["value"] = 0

    for i in range(1, 101):
        time.sleep(0.03)
        progress["value"] = i

    return jsonify({"status": "completed"})

@app.route("/progress")
def get_progress():
    return jsonify(progress)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)