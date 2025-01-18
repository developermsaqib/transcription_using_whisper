import sys
import whisper
import warnings
import json
from metrics import calculate_metrics
import time

# Suppress warnings
warnings.filterwarnings("ignore")

def main():
    try:
        start_time = time.time()
        
        # Get the audio file path and reference text from arguments
        audio_path = sys.argv[1]
        reference_text = ""
        if len(sys.argv) > 2:
            reference_text = sys.argv[2]
            
        print(f"Processing audio file: {audio_path}", file=sys.stderr)
        
        # Load model and transcribe
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        transcribed_text = result["text"]
        
        # Calculate metrics
        metrics = calculate_metrics(
            reference_text,
            transcribed_text,
            start_time
        )
        
        # Output results as JSON
        output = {
            "transcription": transcribed_text,
            "metrics": metrics
        }
        
        print(json.dumps(output))
        
    except Exception as e:
        print(f"Error in Python script: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
