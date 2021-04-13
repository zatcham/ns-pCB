import sys
import time
import csv
import os
from random import seed
from random import randint
from datetime import datetime 
import pandas as pd

# RNG
def newSeed():
    unixtime = time.time()
    ran_time = randint(randint(2,90000), randint(90001,330920))
    if unixtime > ran_time:
        ran_seed = unixtime - ran_time
    elif unixtime < ran_time:
        ran_seed = ran_time - unixtime
    else:
        print ("error")
    return ran_seed

def ranGen():
    ran_val = randint(100, 999)
    return ran_val

def generateDate():
    date_now = datetime.now()
    date_1 = date_now.strftime("%d%m%y-%H%M%S")
    return date_1

# Dicts
lower_alphabet = {
    "a": "0",
    "b": "0",
    "c": "0",
    "d": "0",
    "e": "0",
    "f": "0",
    "g": "0",
    "h": "0",
    "i": "0",
    "j": "0",
    "k": "0",
    "l": "0",
    "m": "0",
    "n": "0",
    "o": "0",
    "p": "0",
    "q": "0",
    "r": "0",
    "s": "0",
    "t": "0",
    "u": "0",
    "v": "0",
    "w": "0",
    "x": "0",
    "y": "0",
    "z": "0"
}

upper_alphabet = {
    "A": "0",
    "B": "0",
    "C": "0",
    "D": "0",
    "E": "0",
    "F": "0",
    "G": "0",
    "H": "0",
    "I": "0",
    "J": "0",
    "K": "0",
    "L": "0",
    "M": "0",
    "N": "0",
    "O": "0",
    "P": "0",
    "Q": "0",
    "R": "0",
    "S": "0",
    "T": "0",
    "U": "0",
    "V": "0",
    "W": "0",
    "X": "0",
    "Y": "0",
    "Z": "0"
}

numbers = {
    "0": "0",
    "1": "0",
    "2": "0",
    "3": "0",
    "4": "0",
    "5": "0",
    "6": "0",
    "7": "0",
    "8": "0",
    "9": "0"
}

# Iterate for numbers
def generateNum():
    for key, value in numbers.items():
        seed(newSeed())
        if value == "0":
            numbers.update({key: ranGen()})
        print(key, '->', numbers[key])

def generateLA():
    for key, value in lower_alphabet.items():
        seed(newSeed())
        if value == "0":
            lower_alphabet.update({key: ranGen()})
        print(key, '->', lower_alphabet[key])

def generateUA():
    for key, value in upper_alphabet.items():
        seed(newSeed())
        if value == "0":
            upper_alphabet.update({key: ranGen()})
        print(key, '->', upper_alphabet[key])

def touch(path):
    open(path, 'a').close()

def otp_main():
    print ("Generating Numbers")
    generateNum()
    print ("Generating lowercase alphabet")
    generateLA()
    print ("Generating uppercase alphabet")
    generateUA()

    # CSV out

    date_fn = str(generateDate())
    print ("Exporting OTPs to CSV")
    print ("File names will be: \n Numbers: OTPNum-" + date_fn + ".csv" 
    "\n Lowercase: OTPLC-" + date_fn + ".csv" + 
    "\n Uppercase: OTPUC-" + date_fn + ".csv")

    touch("otp/OTPNum-" + date_fn + ".csv")
    touch("otp/OTPLC-" + date_fn + ".csv")
    touch("otp/OTPUC-" + date_fn + ".csv")

    nf = pd.DataFrame.from_dict(numbers, orient="index")
    nf.to_csv("otp/OTPNum-" + date_fn + ".csv")

    lcf = pd.DataFrame.from_dict(lower_alphabet, orient="index")
    lcf.to_csv("otp/OTPLC-" + date_fn + ".csv")

    ucf = pd.DataFrame.from_dict(upper_alphabet, orient="index")
    ucf.to_csv("otp/OTPUC-" + date_fn + ".csv")

    """
    "\n Lowercase: OTPLC-" + date_fn + ".csv" + 
    "\n Uppercase: OTPUC-" + date_fn + ".csv")
    with open("otp/OTPNum-" + date_fn + ".csv", 'w') as f:
        w = csv.DictWriter(f, numbers.keys())
        w.writeheader()
        w.writerow(numbers)

    with open("otp/OTPLC-" + date_fn + ".csv", 'w') as f:
        w = csv.DictWriter(f, lower_alphabet.keys())
        w.writeheader()
        w.writerow(lower_alphabet)

    with open("otp/OTPUC-" + date_fn + ".csv", 'w') as f:
        w = csv.DictWriter(f, upper_alphabet.keys())
        w.writeheader()
        w.writerow(upper_alphabet)
 """

if __name__ == "__main__":
    otp_main()
