import json
import openai
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import tempfile
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

load_dotenv()

# Replace with your ElevenLabs API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


# Set API keys
GPTclient = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

# Load Whisper model once
whisper_model = whisper.load_model("base")

# === Persistent Memory Store ===
# In-memory dictionary to store memory for each user
MEMORY_FILE = "memory_store.json"
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory_store = json.load(f)
else:
    memory_store = {}

# Function to get memory of a user (this can be conversation history)
def get_memory(user_id):
    return memory_store.get(str(user_id), [])

# Function to update memory store with new conversation history
def update_memory(user_id, entry):
    uid = str(user_id)
    if uid not in memory_store:
        memory_store[uid] = []
    memory_store[uid].append(entry)
    memory_store[uid] = memory_store[uid][-10:]  # Keep last 10 entries
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_store, f)

# ====================
# 🎙️ Record audio from mic
# ====================
def record_audio(duration=5, samplerate=16000):
    print(f"[🎤] Recording {duration} seconds...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    print("[✔️] Recording complete.")
    return samplerate, audio

# ====================
# 📝 Save audio to temp WAV file
# ====================
def save_wav(samplerate, audio):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        scipy.io.wavfile.write(f.name, samplerate, (audio * 32767).astype(np.int16))
        return f.name

# ====================
# 🗣️ Transcribe with Whisper
# ====================
def transcribe_audio(audio_path):
    print(f"[🧠] Transcribing with Whisper...")
    result = whisper_model.transcribe(audio_path)
    print(f"[📝] User said: {result['text']}")
    return result["text"]

# ====================
# 🤖 Get GPT response
# ====================
def get_gpt_response(prompt, chat_history=[]):
    chat_history.append({"role": "user", "content": prompt})
    response = GPTclient.chat.completions.create(
        model="gpt-4",
        messages=chat_history,
        temperature=0.7
    )
    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})
    return reply, chat_history

# ====================
# 🔊 Speak with ElevenLabs
# ====================
def speak(text):
    print(f"[🔊] Speaking: {text}")
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="kPzsL2i3teMYv0FxEYQ6",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128")
    play(audio)

# ====================
# 🚀 Main loop
# ====================
def run_assistant():
    print("🤖 Voice assistant running. Press Ctrl+C to stop.")
    chat_history = []

    while True:
        try:
            # 1. Record mic input
            samplerate, audio = record_audio(duration=5)

            # 2. Save and transcribe
            audio_path = save_wav(samplerate, audio)
            text = transcribe_audio(audio_path)
            os.remove(audio_path)

            # 3. Get GPT response
            response, chat_history = get_gpt_response(text, chat_history)

            # 4. Speak it aloud
            speak(response)

        except KeyboardInterrupt:
            print("\n👋 Exiting assistant.")
            break
        except Exception as e:
            print(f"[❌ Error] {e}")

# Run the assistant
if __name__ == "__main__":
    run_assistant()
