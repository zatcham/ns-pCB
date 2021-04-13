## ns-pCB (number station - project Cherry Blossom)
## Developed by Zach Matcham (zatcham) and Tom Sangster (tomrow)
## Version 0.2a | 13/4/21

# Imports
import sys
import os
import csv
import re
from gtts import gTTS # pip - tts engine
from datetime import datetime
from pathlib import Path
import pandas as pd
from fpdf import FPDF
from pydub import AudioSegment
from tscipherlib import cencodeh
import nsCB_otpgen

# Variables
main_dir = "/Users/zachmatcham/Documents/ns1z"
date_file = ""
num_csv = {}
lc_csv = {}
uc_csv = {}
strotp_list = []

# imported here to remove msg
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer # install from pip

# Functions 
# 1 - Ancillary

# Checks main_dir exists, if not return false
def checkFilePaths():
    if os.path.exists(main_dir):
        if os.path.exists(main_dir + "/audio"):
            return True
        else:
            return False
    else:
        return False

# Generates date file path for tts export
def generateDate():
    date_now = datetime.now()
    date_1 = date_now.strftime("%d%m%y-%H%M%S")
    date_file = (main_dir + "/audio/" + date_1 + ".mp3")
    return date_file

# Generates TTS MP3s from string 
def generateTTS(phrase):
    tts_lang = "en"
    tts_tld = "com.au"
    tts_obj = gTTS(text=phrase, lang=tts_lang, tld=tts_tld, slow=False)
    fname = generateDate()
    tts_obj.save(fname)
    print ("Time code is " + fname)

# Audio playback - Not yet implamented
# Preamble playback - Most likely not needed due to combine
def playPreamble():
    mixer.init()
    mixer.music.load(main_dir + "/audio/preamble.mp3")
    mixer.music.play()

# Plays audio file
def playAudio(file):
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()

# Playback of TTS File, not working
def runSpeak():
    ttstoplay = input("Enter date/time code of file you want to play : ")
    playAudio(ttstoplay)
    print ("Finished")

# import csv otp as a dict
def importCSVs():
    # Find latest OTPs
    p = Path (main_dir + "/otp/")
    num_latest = max([fn for fn in p.glob('*OTPNum*.csv')], key=lambda f: f.stat().st_mtime)
    lc_latest = max([fn for fn in p.glob('*OTPLC*.csv')], key=lambda f: f.stat().st_mtime)
    uc_latest = max([fn for fn in p.glob('*OTPUC*.csv')], key=lambda f: f.stat().st_mtime)

    # num_reader = csv.DictReader(open(num_latest, 'r'))
    global num_csv
    num_csv = pd.read_csv(num_latest, dtype={"a": int, "b": int}, header=None, index_col=0, squeeze=True).to_dict()
    print (num_csv)

    global lc_csv
    lc_csv = pd.read_csv(lc_latest, header=None, index_col=0, squeeze=True,).to_dict()
    print (lc_csv)

    global uc_csv
    uc_csv = pd.read_csv(uc_latest, header=None, index_col=0, squeeze=True,).to_dict()
    print (uc_csv)

# covert string to otp via dict
def stringToOTP(s):
    # s = cencodeh(s, 1234)
    print (s)
    for element in range(0, len(s)):
        e = s[element]
        if hasNumbers(e): 
            e = float(e)
            for key in num_csv.keys():
                if str(e) == str(key):
                    k = str(num_csv[key])
                    print (str(e) + " -> " + k)
                    strotp_list.append(k)
        else:
            if e.islower():
                for key in lc_csv.keys():
                    if str(e) == str(key):
                        k = str(lc_csv[key])
                        print (str(e) + " -> " + k)
                        strotp_list.append(k)
            elif e.isupper():
                for key in uc_csv.keys():
                    if str(e) == str(key):
                        k = str(uc_csv[key])
                        print (str(e) + " -> " + k)
                        strotp_list.append(k) 
            elif e.isspace():
                strotp_list.append("--")
            else:
                print("Error. Make sure there is no special chars")

# checks if str has any nums in it
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# generates pdf for otps based off csv using fpdf
def generatePDF():
    print ("\n ns-pCB1 - OTP PDF Creation \n")
    print ("Generating PDFs from latest OTP CSVs \n")
    date_now = datetime.now()
    date_1 = date_now.strftime("%d/%m/%y %H:%M:%S")
    date_2 = date_now.strftime("%d%m%y-%H%M%S")
    print ("File name is " + 'OTP ' + date_2 + '.pdf' + "\n")
    p = Path (main_dir + "/otp/")
    p1 = max([fn for fn in p.glob('*OTPNum*.csv')], key=lambda f: f.stat().st_mtime)
    p2 = max([fn for fn in p.glob('*OTPLC*.csv')], key=lambda f: f.stat().st_mtime)
    p3 = max([fn for fn in p.glob('*OTPUC*.csv')], key=lambda f: f.stat().st_mtime)
    with open(p1, newline='') as f1, open(p2, newline='') as f2, open(p3, newline='') as f3:
        n_reader = csv.reader(f1)
        lc_reader = csv.reader(f2)
        uc_reader = csv.reader(f3)
        pdf = FPDF()
        pdf.add_page()
        page_width = pdf.w - 2 * pdf.l_margin
        pdf.set_font('Courier', '', 14.0) 
        pdf.cell(page_width, 0.0, 'OTP - Exported: ' + date_1, align='C')
        pdf.ln(10)
        pdf.set_font('Courier', '', 12)
        col_width = page_width/4
        pdf.ln(1)
        th = pdf.font_size
        pdf.ln(4)
        pdf.cell(page_width, 10.0, 'Double hyphen = space ', align='L')
        pdf.ln(10)
        pdf.ln(4)
        pdf.cell(page_width, 10.0, 'Numbers: ', align='L')
        pdf.ln(10)
        for row in n_reader:
            pdf.cell(col_width, th, str(row[0]), border=1)
            pdf.cell(col_width, th, row[1], border=1)
            pdf.ln(th)
        pdf.ln(4)
        pdf.cell(page_width, 10.0, 'Lowercase: ', align='L')
        pdf.ln(10)
        for row in lc_reader:
            pdf.cell(col_width, th, str(row[0]), border=1)
            pdf.cell(col_width, th, row[1], border=1)
            pdf.ln(th)
        pdf.ln(4)
        pdf.cell(page_width, 10.0, 'Uppercase: ', align='L')
        pdf.ln(10)
        for row in uc_reader:
            pdf.cell(col_width, th, str(row[0]), border=1)
            pdf.cell(col_width, th, row[1], border=1)
            pdf.ln(th)
        pdf.ln(10)
        pdf.set_font('Times','',10.0) 
        pdf.cell(page_width, 0.0, '- end of report -', align='C')
        pdf.output('OTP ' + date_2 + '.pdf', 'F')

# merges audio files , preamble and tts, using pydub
def mergeAudio():
    p = Path (main_dir + "/audio/")
    s1 = AudioSegment.from_mp3(max([fn for fn in p.glob('*.mp3')], key=lambda f: f.stat().st_mtime))
    s2 = AudioSegment.from_mp3("audio/preamble.mp3")
    silence = AudioSegment.silent(duration=2000)
    out = s2 + silence + s1
    date_now = datetime.now()
    date_1 = date_now.strftime("%d%m%y-%H%M%S")
    date_file = (main_dir + "/audio/" + date_1 +  "-merge.mp3")
    out.export(date_file, format="mp3")

# 2 - Mains

# main menu
def showMenu():
    menu = True
    print ("Welcome to ns-pCB1 \n")
    while menu:
        menu = input ("Select an option: \n 1. TTS Generation \n 2. TTS Output (not yet implamented) \n 3. OTP Generation \n 4. Convert OTP into PDF \n 5. Exit\n")
        if menu == "1":
            ttsGenMain()
        elif menu == "2":
            ttsOutMain()
        elif menu == "3":
            otpGenMain()
        elif menu == "5":
            print ("Goodbye")
            menu = None
        elif menu == "4":
            generatePDF()
        elif menu !="":
            print("Incorrect input, try again")
        else:
            showMenu()

def ttsGenMain():
    print ("\n ns-pCB1 - TTS Generation \n")
    importCSVs()
    st = input ("String to convert (no special chars): ")
    stringToOTP(st)
    print(strotp_list)
    generateTTS(str(strotp_list))
    mergeAudio()

def ttsOutMain():
    print ("Not done")

def otpGenMain():
    print ("\n ns-pCB1 - OTP Generation \n")
    print ("Warning: By running this, all future TTS Generations will require the new OTP.")
    q = input("To continue, enter Y, or to return to main menu, press any other key: ")
    if q == "Y":
        print ("\n")
        nsCB1_otpgen.otp_main()
        print ("\n")

def main():
    print ("ns-pCB1 Initialisation:")
    if checkFilePaths() == False:
        print ("Main directory does not exist, exiting")
        print ("Make sure " + main_dir + " exists and /audio")
    elif checkFilePaths() == True:
        print ("Init done \n")
        showMenu()
        
main()
