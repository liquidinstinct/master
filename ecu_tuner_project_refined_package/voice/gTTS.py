from gtts import gTTS
import os

tts = gTTS("Hello,dan would u like me to start kitt e,c,u tuner!", lang='en')
tts.save("hello.mp3")
os.system("start hello.mp3")