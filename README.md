# 🎬 Subtitle Translator Bot (Free Version)

A Telegram bot that translates subtitles (.srt, .ass, .vtt, .sub) into any language using **googletrans** (no paid API required).

## ✨ Features

- Auto-remember user translation preference (`/translate en si`)  
- Multi-format subtitle support (`.srt`, `.ass`, `.vtt`, `.sub`)  
- Batch subtitle support  
- Free, no API key needed  
- Ready for VPS, Docker, Heroku, Railway  

## 🚀 Usage

### 1. Set translation - /translate en si
- Sets English → Sinhala translation.  

### 2. Send subtitle file
- Bot will automatically translate using your saved setting.  

### 3. Check status - /status
- Shows your current translation setting.

## 🛠 Deployment

## Local
```
# 1. Install full Python support if not already
sudo apt update
sudo apt install python3-venv python3-pip -y

# 2. Create a virtual environment inside your project
python3 -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate

# 4. Now install requirements
pip install -r requirements.txt

# 5. Start bot
python bot.py or python3 bot.py

```
## Docker
```
docker build -t subtitle-bot .
docker run -e BOT_TOKEN=your_token subtitle-bot
```
## Heroku
```
heroku create
heroku config:set BOT_TOKEN=your_token
git push heroku main
```
---

This bot is **fully functional**:  

- Users can set translation once via `/translate`  
- Any subtitle they send afterward is automatically translated  
- Multi-format support, free translation only using `googletrans`  

---
