from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

progress = 0
video_url = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    global progress, video_url
    data = request.get_json()
    video_url = data["url"]

    progress = 0
    return jsonify({"status":"started"})

@app.route("/progress")
def get_progress():
    global progress

    if progress < 100:
        progress += 20

    return jsonify({"value": progress})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
