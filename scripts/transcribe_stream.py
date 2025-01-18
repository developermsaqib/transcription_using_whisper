import sys
import whisper
import json
import base64
import numpy as np
import io
import wave

# Initialize Whisper model
model = whisper.load_model("base")
print(json.dumps({"status": "Model loaded"}), flush=True)

def process_audio_chunk(audio_base64):
    try:
        # Decode base64 audio
        audio_bytes = base64.b64decode(audio_base64)
        
        # Convert WAV bytes to numpy array
        with io.BytesIO(audio_bytes) as wav_io:
            with wave.open(wav_io, 'rb') as wav_file:
                audio_data = np.frombuffer(wav_file.readframes(-1), dtype=np.int16)
                audio_data = audio_data.astype(np.float32) / 32768.0  # Normalize to [-1, 1]
        
        # Transcribe
        result = model.transcribe(audio_data)
        
        print(json.dumps({
            "type": "transcription",
            "text": result["text"].strip()
        }), flush=True)
        
    except Exception as e:
        print(json.dumps({
            "type": "error",
            "error": str(e)
        }), flush=True)

# Read input lines
while True:
    try:
        line = sys.stdin.readline()
        if not line:
            break
        data = json.loads(line)
        if 'audio' in data:
            process_audio_chunk(data['audio'])
    except Exception as e:
        print(json.dumps({
            "type": "error",
            "error": f"Input processing error: {str(e)}"
        }), flush=True)
