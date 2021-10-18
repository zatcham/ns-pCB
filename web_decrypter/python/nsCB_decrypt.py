# [154, 254, 68, 150]
# 154, 254, 68, 150 
# key = 1

from tscipherlib import cdecode
import csv

def tsDecrypt(txt, key):
    key = int(key)
    c = txt.replace(" ", "")
    key_list = c.split(",")
    for i in range(len(key_list)):
        key_list[i-1]=int(key_list[i-1])

    out = cdecode(key_list, key)
    return out

if __name__ == "__main__":
    txt = input("Text: ")
    key = int(input("Key: "))
    o = tsDecrypt(txt, key)
    print (o)