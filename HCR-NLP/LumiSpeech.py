import speech_recognition as sr
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
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")

        while True:
            audio = recognizer.listen(source, phrase_time_limit=5)

            try:
                text = recognizer.recognize_google(audio, language='en-GB')
                corrected_text = correct_recognized_text(text, words_to_correct)
                print(f"Recognized: {corrected_text}")

                for trigger_word in triggers:
                    if trigger_word.lower() in corrected_text.lower():
                        command_start_idx = corrected_text.lower().find(trigger_word.lower()) + len(trigger_word)
                        command = corrected_text[command_start_idx:].strip()
                        print(f"Command: {command}")
                        break

            except sr.UnknownValueError:
                pass

            except sr.RequestError as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    # trigger_words = ["Lumi", "Hey Lumi", "Lumi Assistant"]
    # words_to_correct = ["Yiannis", "Demiris", "Lumi"]
    trigger_words = ["Lumi", ["Hey","Lumi"], ["Lumi","Assistant"]]
    words_to_correct = ["Yiannis", "Demiris", "Lumi"]
    listen_for_triggers(trigger_words, words_to_correct)
