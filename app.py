from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__)

# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")

# ==========================================
# API
# ==========================================

@app.route("/info")
def info():

    try:

        video_url = request.args.get("url")

        if not video_url:
            return jsonify({
                "error": "No URL provided"
            })

        ydl_opts = {
            "quiet": True,
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                video_url,
                download=False
            )

        best_combined = None
        best_height = 0

        best_audio = None
        best_audio_bitrate = 0

        for f in info["formats"]:

            if not f.get("url"):
                continue

            # ==========================================
            # BEST COMBINED VIDEO + AUDIO
            # ==========================================

            if (
                f.get("vcodec") != "none"
                and f.get("acodec") != "none"
            ):

                height = f.get("height") or 0

                if height > best_height:
                    best_height = height
                    best_combined = f

            # ==========================================
            # BEST M4A AUDIO
            # ==========================================

            if (
                f.get("vcodec") == "none"
                and f.get("acodec") != "none"
                and f.get("ext") == "m4a"
            ):

                abr = f.get("abr") or 0

                if abr > best_audio_bitrate:
                    best_audio_bitrate = abr
                    best_audio = f

        return jsonify({

            "title": info.get("title"),

            "video": {
                "quality":
                    best_combined.get("height")
                    if best_combined else "Not Found",

                "url":
                    best_combined.get("url")
                    if best_combined else ""
            },

            "audio": {
                "bitrate":
                    best_audio.get("abr")
                    if best_audio else "Not Found",

                "url":
                    best_audio.get("url")
                    if best_audio else ""
            }

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# ==========================================

if __name__ == "__main__":
    app.run()