from flask import Flask, request, render_template
import yt_dlp
import os

app = Flask(__name__)

# Create download folder
os.makedirs("storage/downloads", exist_ok=True)

# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")

# ==========================================
# DOWNLOAD
# ==========================================

@app.route("/download", methods=["POST"])
def download():

    video_url = request.form.get("url")
    download_type = request.form.get("type")

    # ======================================
    # VIDEO 360P WITH AUDIO
    # ======================================

    if download_type == "video":

        ydl_opts = {

            'format':'best',

            'outtmpl':
            'storage/downloads/%(title)s.%(ext)s',

            'noplaylist': True
        }

    # ======================================
    # BEST M4A AUDIO
    # ======================================

    elif download_type == "audio":

        ydl_opts = {

            'format':
            'bestaudio[ext=m4a]',

            'outtmpl':
            'storage/downloads/%(title)s.%(ext)s',

            'noplaylist': True
        }

    else:
        return "Invalid option"

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return """
        <h2>Download Completed</h2>
        <a href="/">Back</a>
        """

    except Exception as e:

        return f"""
        <h2>Error</h2>
        <p>{e}</p>
        <a href="/">Back</a>
        """

# ==========================================

if __name__ == "__main__":
    app.run()