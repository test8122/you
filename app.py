from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__)

# =====================================
# FRONTEND PAGE
# =====================================

@app.route("/")
def home():
    return render_template("index.html")

# =====================================
# API
# =====================================

@app.route("/info")
def info():

    try:

        video_url = request.args.get("url")

        ydl_opts = {
            "quiet": True,
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                video_url,
                download=False
            )

        return jsonify({
            "title": info["title"]
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# =====================================

if __name__ == "__main__":
    app.run()
