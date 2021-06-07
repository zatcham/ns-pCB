## ns-pCB (number station - project Cherry Blossom)
## OTP Generation module
## Developed by Zach Matcham (zatcham)
## Version 0.4 | 7/6/21

import time
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
def generateNum(withOutput):
    for key, value in numbers.items():
        seed(newSeed())
        if value == "0":
            numbers.update({key: ranGen()})
        if withOutput:
            print(key, '->', numbers[key])

def generateLA(withOutput):
    for key, value in lower_alphabet.items():
        seed(newSeed())
        if value == "0":
            lower_alphabet.update({key: ranGen()})
        if withOutput:
            print(key, '->', lower_alphabet[key])

def generateUA(withOutput):
    for key, value in upper_alphabet.items():
        seed(newSeed())
        if value == "0":
            upper_alphabet.update({key: ranGen()})
        if withOutput:
            print(key, '->', upper_alphabet[key])

def checkForDuplicate():
    # i = 1
    # while i < 26:
    #     if lower_alphabet[i] == upper_alphabet[i]:
    #         print ("Duplicate between lowercase and uppercase!")
    #         print ("Exiting!")
    #         exit()
    #     elif lower_alphabet[i] == numbers[i]:
    #         print ("Duplicate between lowercase and numbers!")
    #         print ("Exiting!")
    #         exit()
    #     elif upper_alphabet[i] == numbers[i]:
    #         print ("Duplicate between uppercase and numbers!")
    #         print ("Exiting!")
    #         exit()
    #     else:
    #         i += 1
    # if lower_alphabet.values() in upper_alphabet.values():
    #     print ("Duplicate between lowercase and uppercase!")
    #     print ("Exiting!")
    #     exit()
    # elif lower_alphabet.values() in numbers.values():
    #     print ("Duplicate between lowercase and numbers!")
    #     print ("Exiting!")
    #     exit()
    # elif upper_alphabet.values() in numbers.values():
    #     print ("Duplicate between uppercase and numbers!")
    #     print ("Exiting!")
    #     exit()
    for key, value in lower_alphabet.items():
        if value in upper_alphabet.values():
            print("Duplicate between lowercase and uppercase!")
            print (key, value)
            print("Exiting!")
            exit()
    for key_1 in lower_alphabet:
        for key_2 in lower_alphabet:
            if key_1 == key_2:
                break
            for item in lower_alphabet[key_1]:
                if item in lower_alphabet[key_2]:
                    print("Duplicate between lowercase!")
                    print(key, value)
                    print("Exiting!")
                    exit()
    for key, value in lower_alphabet.items():
        if value in numbers.values():
            print("Duplicate between lowercase and numbers!")
            print (key, value)
            print("Exiting!")
            exit()
    for key, value in upper_alphabet.items():
        if value in numbers.values():
            print("Duplicate between uppercase and numbers!")
            print (key, value)
            print("Exiting!")
            exit()
        if value in upper_alphabet.values():
            print ("Duplicate within uppercase!")
            print (key, value)
            print("Exiting!")
            exit()
    for key, value in numbers.items():
        if value in numbers.items():
            print ("Duplicate within numbers!")
            print (key, value)
            print("Exiting!")
            exit()

# thx tom
def checkSectionForDupe(origKey, origValue, killProgram, debugPrint, returnVal):
    # toReturn = None
    for iKey, iValue in lower_alphabet.items():
        if (iKey != origKey) and (iValue == origValue):
            if debugPrint:
                print("Duplicate Found: \"" + str(iKey) + "\" and \"" + str(origKey) + "\" have a matching value: \n\"" + str(iValue) + "\", \"" + str(origValue) + "\"")
            if killProgram:
                print("A duplicate has been found, exiting")
                exit()
            if returnVal:
                return True
            # toReturn = iKey
            break
    for iKey, iValue in upper_alphabet.items():
        if (iKey != origKey) and (iValue == origValue):
            if debugPrint:
                print("Duplicate Found: \"" + str(iKey) + "\" and \"" + str(origKey) + "\" have a matching value: \n\"" + str(iValue) + "\", \"" + str(origValue) + "\"")
            if killProgram:
                print("A duplicate has been found, exiting")
                exit()
            if returnVal:
                return True
            # toReturn = iKey
            break
    for iKey, iValue in numbers.items():
        if (iKey != origKey) and (iValue == origValue):
            if debugPrint:
                print("Duplicate Found: \"" + str(iKey) + "\" and \"" + str(origKey) + "\" have a matching value: \n\"" + str(iValue) + "\", \"" + str(origValue) + "\"")
            if killProgram:
                print("A duplicate has been found, exiting")
                exit()
            if returnVal:
                return True
            # toReturn = iKey
            break
    return False

def checkAllForDupes(killProgram, debugPrint, returnVal):
    for origKey, origValue in lower_alphabet.items():
        if checkSectionForDupe(origKey, origValue, killProgram, debugPrint, returnVal):
            return True
    for origKey, origValue in lower_alphabet.items():
        if checkSectionForDupe(origKey, origValue, killProgram, debugPrint, returnVal):
            return True
    for origKey, origValue in lower_alphabet.items():
        if checkSectionForDupe(origKey, origValue, killProgram, debugPrint, returnVal):
            return True
    return False

def generateAll(withOutput):
    i = 0
    if i == 0:
        print ("Generating Numbers")
        generateNum(withOutput)
        print ("Generating lowercase alphabet")
        generateLA(withOutput)
        print ("Generating uppercase alphabet")
        generateUA(withOutput)
        if checkAllForDupes(False, True, True):
            while checkAllForDupes(False, True, True):
                time.sleep(2)
                resetDicts(withOutput)
                print("----")
                print("Regenerating due to duplicates")
                print("Regenerating Numbers")
                generateNum(withOutput)
                print("Regenerating lowercase alphabet")
                generateLA(withOutput)
                print("Regenerating uppercase alphabet")
                generateUA(withOutput)
                i += 1
            print("----")
            print ("Amount of duplicates found: " + str(i))
            print("----")
            return True
        else:
            return True

def resetDicts(withOutput):
    for key, value in lower_alphabet.items():
        lower_alphabet.update({key: "0"})
        if withOutput:
            print("changed key "+key+" to 0")
    for key, value in upper_alphabet.items():
        upper_alphabet.update({key: "0"})
        if withOutput:
            print("changed key " + key + " to 0")
    for key, value in numbers.items():
        numbers.update({key: "0"})
        if withOutput:
            print("changed key " + key + " to 0")
    if withOutput:
        print ("Reset all keys to 0")


def touch(path):
    open(path, 'a').close()

def otp_main():
    if generateAll(False):
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

if __name__ == "__main__":
    otp_main()