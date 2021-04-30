## ns-pCB (number station - project Cherry Blossom)
## TTS Module
## Developed by Zach Matcham (zatcham)
## Version 0.1 | 24/4/21

import os
from pydub import AudioSegment
from datetime import datetime

morse_dict = {'A':'.-', 'B':'-...', 'C':'-.-.', 
                'D':'-..', 'E':'.', 'F':'..-.', 
                'G':'--.', 'H':'....', 'I':'..', 
                'J':'.---', 'K':'-.-', 'L':'.-..', 
                'M':'--', 'N':'-.', 'O':'---', 
                'P':'.--.', 'Q':'--.-', 'R':'.-.', 
                'S':'...', 'T':'-', 'U':'..-', 
                'V':'...-', 'W':'.--',
                'X':'-..-', 'Y':'-.--', 'Z':'--..',
                '1':'.----', '2':'..---', '3':'...--',
                '4':'....-', '5':'.....', '6':'-....',
                '7':'--...', '8':'---..', '9':'----.',
                '0':'-----', ', ':'--..--', '.':'.-.-.-',
                '?':'..--..', '/':'-..-.', '-':'-....-',
                '(':'-.--.', ')':'-.--.-'}

morsefiie_list = ['dot.mp3','dash.mp3']
speechfiie_list = ['0.mp3','1.mp3','2.mp3','3.mp3','4.mp3','5.mp3','6.mp3','7.mp3','8.mp3','9.mp3']
test_list = ['tts_gen/audio/0.mp3', 'tts_gen/audio/1.mp3']

def generateTTS(ttsin):
    temp = AudioSegment.empty()
    for element in ttsin:
        if element == "1":
            a1 = AudioSegment.from_mp3("tts_gen/voice/1.mp3")
            temp += a1
        elif element == "2":
            a1 = AudioSegment.from_mp3("tts_gen/voice/2.mp3")
            temp += a1
        elif element == "3":
            a1 = AudioSegment.from_mp3("tts_gen/voice/3.mp3")
            temp += a1
        elif element == "4":
            a1 = AudioSegment.from_mp3("tts_gen/voice/4.mp3")
            temp += a1
        elif element == "5":
            a1 = AudioSegment.from_mp3("tts_gen/voice/5.mp3")
            temp += a1
        elif element == "6":
            a1 = AudioSegment.from_mp3("tts_gen/voice/6.mp3")
            temp += a1
        elif element == "7":
            a1 = AudioSegment.from_mp3("tts_gen/voice/7.mp3")
            temp += a1
        elif element == "8":
            a1 = AudioSegment.from_mp3("tts_gen/voice/8.mp3")
            temp += a1
        elif element == "9":
            a1 = AudioSegment.from_mp3("tts_gen/voice/9.mp3")
            temp += a1
        elif element == "0":
            a1 = AudioSegment.from_mp3("tts_gen/voice/0.mp3")
            temp += a1
    if __name__ == "__main__":
        date_now = datetime.now()
        date_1 = date_now.strftime("%d%m%y-%H%M%S")
        date_file = ("tts_gen/out/" + date_1 +  ".mp3")
        temp.export(date_file, format="mp3")

    return temp

def generateMorseTxt(morsein):
    morsein = morsein.upper()
    out = ""
    for element in morsein:
        if element != " ":
            out += morse_dict[element] + " "
        else:
            out += " "
    return out

def generateMorseAud(moresin):
    m = generateMorseTxt(moresin)
    temp = AudioSegment.empty()
    silence = AudioSegment.silent(duration=500)
    for element in m:
        if element == "-":
            a1 = AudioSegment.from_mp3("tts_gen/morse/dash.mp3")
            temp += a1
            temp += silence
        elif element == ".":
            a1 = AudioSegment.from_mp3("tts_gen/morse/dot.mp3")
            temp += a1
            temp += silence
        elif element == " ":
            s1 = AudioSegment.silent(duration=500)
            temp += s1
    if __name__ == "__main__":
        date_now = datetime.now()
        date_1 = date_now.strftime("%d%m%y-%H%M%S")
        date_file = ("tts_gen/out/" + date_1 +  "-morse.mp3")
        temp.export(date_file, format="mp3")

    return temp


def checkForFiles():
    if all([os.path.isfile("tts_gen/audio/" + f) for f in speechfiie_list]):
        print ("all exist")
    else:
        print ("none")
    if all([os.path.isfile("tts_gen/audio/" + f) for f in morsefiie_list]):
        print ("all exist")  
    else:
        print ("none")
    if all([os.path.isfile(f) for f in test_list]):
        print ("all exist")  
    else:
        print ("none")
    print ("x")

def generateMorse(x):
    a = generateMorseTxt(x)
    return generateMorseAud(a)

if __name__ == "__main__":
    a = input ("Enter string: ")
    # generateTTS(a)
    checkForFiles()
    print (generateMorseTxt(a))
    generateMorseAud(a)