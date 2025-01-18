from jiwer import wer
import time
import psutil
import os
from difflib import SequenceMatcher

def calculate_metrics(reference_text, hypothesis_text, start_time):
    # Calculate time taken
    time_taken = time.time() - start_time
    
    # Calculate WER
    error_rate = wer(reference_text, hypothesis_text)
    
    # Calculate accuracy using SequenceMatcher
    accuracy = SequenceMatcher(None, reference_text.lower(), hypothesis_text.lower()).ratio() * 100
    
    # Get memory usage
    process = psutil.Process(os.getpid())
    memory_used = process.memory_info().rss / 1024 / 1024  # in MB
    
    return {
        "wer": round(error_rate * 100, 2),  # as percentage
        "accuracy": round(accuracy, 2),      # as percentage
        "time_taken": round(time_taken, 2),  # in seconds
        "memory_mb": round(memory_used, 2)
    }
