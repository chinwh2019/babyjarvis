# Streamlit UI for OpenAI's Whisper, GPT, chatGPT, babyagi and more

This is a simple [Streamlit UI](https://streamlit.io/) for [OpenAI's Whisper speech-to-text model](https://openai.com/blog/whisper/).
It let's you download and transcribe media from YouTube videos, playlists, or local files.
You can then browse, filter, and search through your saved audio files.

## Setup

This was built & tested on Python 3.11 but should also work on Python 3.9+ as with the original [Whisper repo](https://github.com/openai/whisper)).
You'll need to install `ffmpeg` on your system. Then, install the requirements with `pip`.

```
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg

pip install -r requirements.txt
```

## Usage

If want to use OpenAI chatGPT api:
1. Create a folder ```env```
2. Create a file ```local.toml``` 
2. Add api key to ```local.toml``` in```env``` folder

Once you're set up, you can run the app with:

```
streamlit run app/main.py
```

This will open a new tab in your browser with the app. You can then select a YouTube URL or local file & click "Run Whisper" to run the model on the selected media.

