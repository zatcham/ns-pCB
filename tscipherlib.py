import math
import random


def cencode(text, key):
    output = []
    random.seed(key)
    for h in range(len(text)):
        i = h + 1
        output.append(
            (ord(text[h]) + cscramble(i, key))
            % 255)
    return output


def cencodeh(text, key):
    output = ""
    random.seed(key)
    for h in range(len(text)):
        i = h + 1
        chara = hex((ord(text[h]) + cscramble(i, key)) % 255)
        chara = chara[2:]
        while len(chara) < 2:
            chara = "0" + chara
        output = output + chara
    return output


def cscramble(iterate, key):
    interim = (iterate
               + (key % 10) * iterate + math.floor(iterate / 3)
               + iterate * 2
               + math.floor(9 * math.sin(math.radians(iterate * 2)))
               + random.randint(0, 200)
               ) % 255
    return interim + 255


def cdecode(array, key):
    output = ""
    random.seed(key)
    for h in range(len(array)):
        i = h + 1
        maths = (array[h] - cscramble(i, key))
        output = output + (chr(maths % 255))
    return output


def cdecodeh(stringin, key):
    stredit = stringin.lower()
    if len(stringin) % 2 == 1:
        stredit = "0" + stringin
    hexdigits = {"0": 0,
                 "1": 1,
                 "2": 2,
                 "3": 3,
                 "4": 4,
                 "5": 5,
                 "6": 6,
                 "7": 7,
                 "8": 8,
                 "9": 9,
                 "a": 10,
                 "b": 11,
                 "c": 12,
                 "d": 13,
                 "e": 14,
                 "f": 15}

    array = []
    for c in range(math.floor(len(stredit) / 2)):
        ptr = c * 2
        array.append((hexdigits[stredit[ptr]] * 16) + hexdigits[stredit[ptr + 1]])

    output = ""
    random.seed(key)
    for h in range(len(array)):
        i = h + 1
        maths = (array[h] - cscramble(i, key))
        output = output + (chr(maths % 255))
    return output


# random.seed(5)
# for i in range(5):
#    print(random.randint(0,10000))


if __name__ == "__main__":
    # execute only if run as a script
    print(cdecode(cencode("hello", 1), 1))
    a = cencode(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        1)
    for j in range(len(a)):
        print(" " * math.floor(a[j] / 2) + "#")
    print(cdecode([95, 175, 180, 10, 112, 3, 180, 11, 177, 196, 223, 119], 100))


