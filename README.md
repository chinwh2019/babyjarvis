# Streamlit UI with openAI and OSS models for Transcription and Database, Personallized Chatbot, Document Query and Summarization, BabyAGI and more

This is a simple [Streamlit UI](https://streamlit.io/) for:

* [OpenAI's Whisper speech-to-text model](https://openai.com/blog/whisper/). It let's you download and transcribe media from videos, playlists, or local files. You can then browse, filter, and search through your saved audio files.

* [OpenAI's GPT-3.5](https://openai.com/blog/openai-api/). It let's you generate text from a prompt using the GPT-3.5 API.

* [babyagi](https://github.com/yoheinakajima/babyagi). It let's you create, prioritize, and execute tasks using the babyagi task management system.

* Prompt Engineering. It contains essential prompt tactics from Andrew Ng's OpenAI course for communicating with GPT-3.5.

* Document Query and Summarization. It let's you query and summarize documents using the GPT-3.5 or 4 or OSS models.

## Setup

This was built & tested on Python 3.9 but should also work on Python 3.9+ as with the original [Whisper repo](https://github.com/openai/whisper)).
You'll need to install `ffmpeg` on your system. Then, install the requirements with `pip`.

```bash
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
3. Add api key to ```local.toml``` in```env``` folder
4. Or key in api key in streamlit UI

Once you're set up, you can run the app with:

```bash
streamlit run app/main.py
```

This will open a new tab in your browser with the app. You can then select a YouTube URL or local file & click "Run Whisper" to run the model on the selected media.
