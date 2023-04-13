import pyttsx3

def voice_transfer(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate+50)
    voices = engine.getProperty('voices')
    for voice in voices:
        if voice.name == 'Microsoft Irina Desktop - Russian':
            engine.setProperty('voice', voice.id)
            break

    engine.say(text)
    engine.runAndWait()