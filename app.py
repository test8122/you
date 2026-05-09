from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__)

# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():
    return render_template("index.html")

# =====================================================
# API
# =====================================================

@app.route("/info")
def info():

    try:

        video_url = request.args.get("url")

        if not video_url:
            return jsonify({
                "error": "No URL provided"
            })

        # =================================================
        # YT-DLP OPTIONS
        # =================================================

        ydl_opts = {

            "quiet": True,
            "noplaylist": True,

            # Better bypass for cloud hosting
            "extractor_args": {
                "youtube": {
                    "player_client": [
                        "android",
                        "web"
                    ]
                }
            },

            # Fake browser headers
            "http_headers": {
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            }
        }

        # =================================================
        # EXTRACT INFO
        # =================================================

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                video_url,
                download=False
            )

        # =================================================
        # BEST FORMATS
        # =================================================

        best_combined = None
        best_height = 0

        best_audio = None
        best_audio_bitrate = 0

        for f in info.get("formats", []):

            if not f.get("url"):
                continue

            # =============================================
            # BEST VIDEO + AUDIO
            # =============================================

            if (
                f.get("vcodec") != "none"
                and f.get("acodec") != "none"
            ):

                height = f.get("height") or 0

                if height > best_height:

                    best_height = height
                    best_combined = f

            # =============================================
            # BEST M4A AUDIO
            # =============================================

            if (
                f.get("vcodec") == "none"
                and f.get("acodec") != "none"
                and f.get("ext") == "m4a"
            ):

                abr = f.get("abr") or 0

                if abr > best_audio_bitrate:

                    best_audio_bitrate = abr
                    best_audio = f

        # =================================================
        # RESPONSE
        # =================================================

        return jsonify({

            "title":
                info.get("title", "Unknown Title"),

            "thumbnail":
                info.get("thumbnail", ""),

            "video": {

                "quality":
                    best_combined.get("height")
                    if best_combined else "Not Found",

                "ext":
                    best_combined.get("ext")
                    if best_combined else "",

                "url":
                    best_combined.get("url")
                    if best_combined else ""
            },

            "audio": {

                "bitrate":
                    best_audio.get("abr")
                    if best_audio else "Not Found",

                "ext":
                    best_audio.get("ext")
                    if best_audio else "",

                "url":
                    best_audio.get("url")
                    if best_audio else ""
            }

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# =====================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)