## ns-pCB (number station - project Cherry Blossom)
## TTS Module
## Developed by Zach Matcham (zatcham)
## Version 0.1 | 24/4/21

import os
from pydub import AudioSegment
from datetime import datetime
import configparser

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

morsefiie_list = ['tts_gen/morse/dot.mp3','tts_gen/morse/dash.mp3']
speechfiie_list = ['tts_gen/voice/0.mp3','tts_gen/voice/1.mp3','tts_gen/voice/2.mp3','tts_gen/voice/3.mp3','tts_gen/voice/4.mp3','tts_gen/voice/5.mp3','tts_gen/voice/6.mp3','tts_gen/voice/7.mp3','tts_gen/voice/8.mp3','tts_gen/voice/9.mp3']
test_list = ['tts_gen/voice/0.mp3', 'tts_gen/voice/1.mp3']

def generateTTS(ttsin):
    checkConfig()
    checkForFiles()
    temp = AudioSegment.empty()
    for element in ttsin:
        if element == "1":
            a1 = AudioSegment.from_mp3("tts_gen/voice/1.mp3")
            temp += a1
            temp += AudioSegment.silent(duration=50)
        elif element == "2":
            a1 = AudioSegment.from_mp3("tts_gen/voice/2.mp3")
            temp += a1
            temp += AudioSegment.silent(duration=50)
        elif element == "3":
            a1 = AudioSegment.from_mp3("tts_gen/voice/3.mp3")
            temp += a1
            temp += AudioSegment.silent(duration=50)
        elif element == "4":
            a1 = AudioSegment.from_mp3("tts_gen/voice/4.mp3")
            temp += a1
            temp += AudioSegment.silent(duration=50)
        elif element == "5":
            a1 = AudioSegment.from_mp3("tts_gen/voice/5.mp3")
            temp += a1
            temp += AudioSegment.silent(duration=50)
        elif element == "6":
            a1 = AudioSegment.from_mp3("tts_gen/voice/6.mp3")
            temp += a1
            temp += AudioSegment.silent(duration=50)
        elif element == "7":
            a1 = AudioSegment.from_mp3("tts_gen/voice/7.mp3")
            temp += a1
            temp += AudioSegment.silent(duration=50)
        elif element == "8":
            a1 = AudioSegment.from_mp3("tts_gen/voice/8.mp3")
            temp += a1
            temp += AudioSegment.silent(duration=50)
        elif element == "9":
            a1 = AudioSegment.from_mp3("tts_gen/voice/9.mp3")
            temp += a1
            temp += AudioSegment.silent(duration=50)
        elif element == "0":
            a1 = AudioSegment.from_mp3("tts_gen/voice/0.mp3")
            temp += a1
            temp += AudioSegment.silent(duration=50)
        elif element == " ":
            a1 = AudioSegment.silent(duration=300)
            temp += a1
    if __name__ == "__main__":
        date_now = datetime.now()
        date_1 = date_now.strftime("%d%m%y-%H%M%S")
        date_file = ("tts_gen/out/" + date_1 +  "-speech.mp3")
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
    checkForFiles()
    checkConfig()
    m = generateMorseTxt(moresin)
    temp = AudioSegment.empty()
    silence = AudioSegment.silent(duration=float(fc_md1))
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
            s1 = AudioSegment.silent(duration=float(fc_md2))
            temp += s1
        elif element == "  ":
            s1 = AudioSegment.silent(duration=float(fc_md3))
            temp += s1
    if __name__ == "__main__":
        date_now = datetime.now()
        date_1 = date_now.strftime("%d%m%y-%H%M%S")
        date_file = ("tts_gen/out/" + date_1 +  "-morse.mp3")
        temp.export(date_file, format="mp3")

    return temp


def checkForFiles():
    if all([os.path.isfile(f) for f in speechfiie_list]):
        print ("All speech files exist")
    else:
        print ("Speech files missing")
        print ("Exiting...")
        exit()
    if all([os.path.isfile(f) for f in morsefiie_list]):
        print ("All morse files exist")  
    else:
        print ("Morse files missing")
        print ("Exiting...")
        exit()
    # if all([os.path.isfile(f) for f in test_list]):
    #     print ("All test files exist")  
    # else:
    #     print ("Test files missing")
    #     print ("Exiting...")
    #     exit()


def checkConfig():
    conf = configparser.ConfigParser()
    conf.read("config.cb")
    global fc_md1
    fc_md1 = conf.get("TTS", "morse_delay1")
    global fc_md2
    fc_md2 = conf.get("TTS", "morse_delay2")
    global fc_md3
    fc_md3 = conf.get("TTS", "morse_delay3")
    global fc_ml
    fc_ml = conf.get("TTS", "morse_loop")
    global fc_mld1
    fc_mld1 = conf.get("TTS", "morseloop_delay1")
    global fc_mld2
    fc_mld2 = conf.get("TTS", "morseloop_delay2")

def generateMorse(x): # dont use on nscb
    checkConfig()
    a = generateMorseTxt(x)
    b = generateMorseAud(x)
    return b

def generateMorseLoop(x): # dont use this in main
    checkForFiles()
    checkConfig()
    z = 0
    y = int(fc_ml)
    print (generateMorseTxt(x))
    silence = AudioSegment.silent(float(fc_mld1))
    b = generateMorseAud(x)
    c = AudioSegment.empty()
    while y > z:
        c += b
        c += AudioSegment.silent(float(fc_mld2))
        print(y)
        print(z)
        z += 1
        print(z)
    if y > 1:
        c += silence
    return c


if __name__ == "__main__":
    checkConfig()  
    a = input ("Enter string: ")
    generateTTS(a) 
    print (generateMorseTxt(a))
    generateMorseAud(a)