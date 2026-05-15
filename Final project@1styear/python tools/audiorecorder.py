import speech_recognition as sr


r = sr.Recognizer()
with sr.Microphone() as source:
    print("Listening")
    audio = r.listen(source)


with open("microphone-results.raw", "wb") as file:
    file.write(audio.get_raw_data())


with open("microphone-results.wav", "wb") as file:
    file.write(audio.get_wav_data())


with open("microphone-results.aiff", "wb") as file:
    file.write(audio.get_aiff_data())

with open("microphone-results.flac", "wb") as file:
    file.write(audio.get_flac_data())