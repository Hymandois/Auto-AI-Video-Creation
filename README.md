# Auto-AI-Video-Creation
Generates AI images, converts them into videos with music, and uploads them to YouTube automatically on a daily schedule.

## Features

- Generates images using OpenAI  
- Converts images into videos  
- Adds background music automatically  
- Uploads videos daily at a scheduled time  
- Uses YouTube Data API for uploading  
- Fully automated pipeline  

---

## 📁 Project Structure
Auto-AI-Video-Creaiton/
- ├── VIDEOS/ # Generated videos
- ├── MUSIC/ # Background music (.mp3 files)
- ├── client_secret.json # Google OAuth credentials
- ├── token.pickle # Saved login session (auto-generated)
- ├── main.py # Main script


---

## ⚙️ Configuration

The following must be set up before running:

### 1. OpenAI API Key

Used for generating images.

- Add it directly in the code
(There is no control for environment variables...)

### 2. YouTube API (OAuth)

You must provide:

- `client_secret.json`

Steps:
1. Go to Google Cloud Console  
2. Enable **YouTube Data API v3**  
3. Create OAuth credentials  
4. Download `client_secret.json` 
5. Copy and paste it to the project folder

### 3. MUSIC Folder

Add `.mp3` files to: 
	MUSIC/

---

## Instruction

```bash
python main.py
```

In the code, provide details on following variables:
```bash
PROMPT

DESCRIPTION

TITLE_PREFIX

UPLOAD_TIME
```
to your liking.