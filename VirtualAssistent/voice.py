import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

# Reading Microphone as source
# listening the speech and store in audio_text variable
with sr.Microphone() as source:
    print("Start Talking")
    audio_text = recognizer.listen(source)
    try:
        # using google speech recognition
        _youSaid = recognizer.recognize_google(audio_text)
        print("You Said: " + _youSaid)
    except:
        print("Sorry, I did not get that")