import os
import time
import datetime
import pickle
import random
import requests

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, ImageClip

from openai import OpenAI

# =====================
# CONFIG
# =====================

# Folders
VIDEOS_DIR = "VIDEOS"
MUSIC_DIR = "MUSIC"

### API CONFIG

OPENAI_API_KEY = "api_key___I_obv_cant_push_mine"

# Google OAuth file:
CLIENT_SECRET_FILE = "client_secret.json"


### AI & YOUTUBE CONFIG

# The prompt that is sent to GPT Image generation.
PROMPT = "Skibidi toilet"

# Description for the videos:
DESCRIPTION = "Auto generated video"

# Titles for the videos:
TITLE_PREFIX = "AI Video"

# What times the videos should be uploaded on:
UPLOAD_TIME = "12:00"


### Scopes & Init, (You can look past this.)
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


# =====================
# GENERATE IMAGE (GPT)
# =====================
"""
Generates an image using OpenAI and saves it locally.
Returns the path to the generated image.
"""
def generate_image(prompt):
    img = client.images.generate(
        model="gpt-image-1-mini", # <- change if you have more money...
        prompt=prompt,
        size="1024x1024"
    )

    # Get image URL
    url = img.data[0].url

    # Download image
    img_data = requests.get(url).content

    # Save to VIDEOS folder
    path = os.path.join(VIDEOS_DIR, "temp.png")

    with open(path, "wb") as f:
        f.write(img_data)

    return path


# =====================
# CREATE VIDEO FROM IMAGE
# =====================
"""
Creates a simple video from an image (no TTS).
Adds background music.
"""
def create_video_from_image(image_path):
    # Create image clip (10 seconds)
    image = ImageClip(image_path).set_duration(10)

    # Get music files
    music_files = [f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")]

    if not music_files:
        print("No music found.")
        return None

    # Pick random music
    music_path = os.path.join(MUSIC_DIR, random.choice(music_files))
    music = AudioFileClip(music_path).volumex(0.2)

    # Match duration
    music = music.set_duration(10)

    # Attach audio
    final_video = image.set_audio(music)

    # Save video
    filename = f"video_{int(time.time())}.mp4"
    output_path = os.path.join(VIDEOS_DIR, filename)

    final_video.write_videofile(output_path, fps=24)

    return output_path


# =====================
# AUTH
# =====================
"""
Handles login/authentication with YouTube API.
Saves login session to token.pickle so you don't need to log in every time.
"""
def get_authenticated_service():
    creds = None

    # If we already got saved credentials, load them
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials, start login flow...
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE, SCOPES
        )

        # Opens browser / console login
        creds = flow.run_console()

        # Save credentials for next time
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    # Build YouTube API client
    return build("youtube", "v3", credentials=creds)


# =====================
# UPLOAD FUNCTION
# =====================
"""
Uploads a video file to YouTube with given title and description.
"""
def upload_video(youtube, file_path, title):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": DESCRIPTION,
            },
            "status": {
                "privacyStatus": "public"
            },
        },
        media_body=MediaFileUpload(file_path)
    )

    request.execute()
    print(f"Uploaded: {title}")


# =====================
# MAIN LOOP
# =====================
"""
Main loop:
- Generates image
- Converts to video
- Uploads at scheduled time
"""
def main():
    youtube = get_authenticated_service()

    while True:
        now = datetime.datetime.now().strftime("%H:%M")

        if now == UPLOAD_TIME:

            print("Generating AI image...")

            image = generate_image(PROMPT)

            print("Creating video...")
            video = create_video_from_image(image)

            if video:
                # Generate title & upload
                title = f"{TITLE_PREFIX} - {os.path.basename(video)}"
                upload_video(youtube, video, title)

                # Cleanup
                os.remove(image)
                os.remove(video)

            time.sleep(60)

        time.sleep(10)


if __name__ == "__main__":
    main()