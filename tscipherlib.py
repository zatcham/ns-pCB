import math
import random
def cencode(text,key):
    output = []
    random.seed(key)
    for h in range(len(text)):
        i = h + 1
        output.append(
            (ord(text[h])+cscramble(i,key))
            %255)
    return output

def cencodeh(text,key):
    output = ""
    random.seed(key)
    for h in range(len(text)):
        i = h + 1
        chara = hex((ord(text[h])+cscramble(i,key))%255)
        chara = chara[2:]
        while len(chara)<2:
            chara = "0" + chara
        output = output + chara
    return output

def cscramble(iterate,key):
    interim = (iterate
            +(key%10)*iterate+math.floor(iterate/3)
            +iterate*2
            +math.floor(9*math.sin(math.radians(iterate*2)))
            +random.randint(0,200)
           )%255
    return interim+255
                       
def cdecode(array,key):
    output = ""
    random.seed(key)
    for h in range(len(array)):
        i = h + 1
        maths =(array[h]-cscramble(i,key))
        output = output + (chr(maths%255))
    return output

#random.seed(5)
#for i in range(5):
#    print(random.randint(0,10000))




if __name__ == "__main__":
    # execute only if run as a script

    print(cdecode(cencode("hello", 1),1))
    a=cencode("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 1)
    for j in range(len(a)):
        print(" "*math.floor(a[j]/2)+"#")