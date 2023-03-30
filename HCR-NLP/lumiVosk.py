import pyaudio
import json
from vosk import Model, KaldiRecognizer
from difflib import SequenceMatcher
import numpy as np
import webrtcvad  # Import the WebRTC VAD library
# import rospy
#https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip small
#https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip big
#https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip mid
# def talk3(str_msg,topic):
#     pub = rospy.Publisher(topic, String, queue_size=10)
#     rospy.loginfo(str_msg)
#     pub.publish(str_msg)

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
    model = Model("vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 16000)

    vad = webrtcvad.Vad(1)  # Create a VAD object with the aggressiveness level set to 3

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print("Listening...")

    frame_duration_ms = 30  # Frame duration in milliseconds
    frame_size = int(16000 * frame_duration_ms / 1000)  # Calculate the frame size based on the duration and sample rate

    while True:
        data = stream.read(frame_size, exception_on_overflow=False)
        if len(data) == 0:
            break

        # Check if the frame contains speech using VAD
        if vad.is_speech(data, 16000):
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                corrected_text = correct_recognized_text(text, words_to_correct)
                print(f"Recognized: {corrected_text}")

                for trigger_word in triggers:
                    if trigger_word.lower() in corrected_text.lower():
                        command_start_idx = corrected_text.lower().find(trigger_word.lower()) + len(trigger_word)
                        command = corrected_text[command_start_idx:].strip()
                        print(f"Command: {command}")
                        # talk3.talk(command, "nlp_input")
                        break

if __name__ == "__main__":
    # rospy.init_node('speech_to_text_node', anonymous=True)
    trigger_words = ["pepper", "Hey pepper", "Hi pepper", "peppa"]
    words_to_correct = ["Yiannis", "Demiris"]
    listen_for_triggers(trigger_words, words_to_correct)