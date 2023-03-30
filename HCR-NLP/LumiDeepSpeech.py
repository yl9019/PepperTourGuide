import deepspeech
import numpy as np
import pyaudio
import time
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def correct_recognized_text(text, words, similarity_threshold=0.7):
    corrected_text = []
    for word in text.split():
        best_match = max(words, key=lambda x: similarity(word.lower(), x.lower()))
        if similarity(word.lower(), best_match.lower()) >= similarity_threshold:
            corrected_text.append(best_match)
        else:
            corrected_text.append(word)
    return ' '.join(corrected_text)

def listen_for_triggers(triggers, words_to_correct):
    model_file_path = 'deepspeech-0.9.3-models.pbmm'
    model = deepspeech.Model(model_file_path)

    ds_stream = model.createStream()

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK_SIZE = 1024

    audio = pyaudio.PyAudio()
    pa_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)

    print("Listening...")
    while True:
        buffer = pa_stream.read(CHUNK_SIZE)
        data16 = np.frombuffer(buffer, dtype=np.int16)
        model.feedAudio(ds_stream, data16)

        text = model.intermediateDecode(ds_stream).strip()
        corrected_text = correct_recognized_text(text, words_to_correct)
        print(f"Recognized: {corrected_text}")

        for trigger_word in triggers:
            if trigger_word.lower() in corrected_text.lower():
                command_start_idx = corrected_text.lower().find(trigger_word.lower()) + len(trigger_word)
                command = corrected_text[command_start_idx:].strip()
                print(f"Command: {command}")
                break

        time.sleep(0.1)

    pa_stream.stop_stream()
    pa_stream.close()
    audio.terminate()

if __name__ == "__main__":
    trigger_words = ["Lumi", "Hey Lumi", "Lumi Assistant"]
    words_to_correct = ["Yiannis", "Demiris", "Lumi"]
    listen_for_triggers(trigger_words, words_to_correct)
