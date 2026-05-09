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

    video_url = request.args.get("url")

    ydl_opts = {
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)

    best_combined = None
    best_combined_height = 0

    best_m4a_audio = None
    best_m4a_bitrate = 0

    for f in info["formats"]:

        if not f.get("url"):
            continue

        # BEST COMBINED VIDEO + AUDIO
        if (
            f.get("vcodec") != "none"
            and f.get("acodec") != "none"
        ):

            height = f.get("height") or 0

            if height > best_combined_height:
                best_combined_height = height
                best_combined = f

        # BEST M4A AUDIO
        if (
            f.get("vcodec") == "none"
            and f.get("acodec") != "none"
            and f.get("ext") == "m4a"
        ):

            abr = f.get("abr") or 0

            if abr > best_m4a_bitrate:
                best_m4a_bitrate = abr
                best_m4a_audio = f

    return jsonify({
        "title": info["title"],

        "video": {
            "quality": best_combined.get("height"),
            "url": best_combined.get("url")
        },

        "audio": {
            "bitrate": best_m4a_audio.get("abr"),
            "url": best_m4a_audio.get("url")
        }
    })

# =====================================

if __name__ == "__main__":
    app.run()
