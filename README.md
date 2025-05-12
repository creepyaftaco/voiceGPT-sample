# 🎙️ Voice Assistant

A Python-based voice assistant that utilizes OpenAI's Whisper for speech recognition, GPT-4o for generating responses, and ElevenLabs for text-to-speech synthesis.

## 🚀 Features

- Real-time speech-to-text conversion using Whisper
- Context-aware responses powered by GPT-4o
- Natural-sounding voice output via ElevenLabs
- Multi-turn conversation support

## 🛠️ Setup Instructions

## Installation Steps

1. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set API Keys:**
   Replace the placeholders in `botScript.py` with your actual OpenAI and ElevenLabs API keys:
   ```python
   OPENAI_API_KEY = "your-openai-api-key"
   ELEVENLABS_API_KEY = "your-elevenlabs-api-key"
   ```

4. **Install FFmpeg:**
   * **Windows:** Download from https://ffmpeg.org/download.html and add the `bin` directory to your system's PATH.
   * **macOS:** Use Homebrew:
     ```bash
     brew install ffmpeg
     ```
   * **Linux:** Use your distribution's package manager:
     ```bash
     sudo apt-get install ffmpeg
     ```

5. **Run the Assistant:**
   ```bash
   python botScript.py
   ```

## Notes
* Ensure your microphone is properly connected and configured.
* The assistant records 5-second audio clips; adjust the duration in `botScript.py` if needed.
* For continuous conversation, the assistant maintains context across turns.
