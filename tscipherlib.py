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
        chara = hex((ord(text[h])+cscramble(i,key)) %255)
        chara = chara[2:]
        while len(chara)<2:
            chara = "0" + chara
        output = output + chara
    return output

def cscramblem(iterate,key):
    interim = (iterate
            +(key%10)*iterate+math.floor(iterate/3)
            +iterate*2
            +math.floor(9*math.sin(math.radians(iterate*2)))
            +random.randint(0,200)
           )%255
    return interim+255

def cscramble(iterate,key):
    interim = iterate
    interim += (key%10)*iterate
    interim += math.floor(iterate/3)
    interim += iterate*2
    interim += math.floor(9*math.sin(math.radians(iterate*2)))  #add 9sin(iterate*2) with the decimal point chopped off
    print (interim)
    #interim += random.randint(0,200) #REMOVE!
    for i in range(6):
        interimb = math.sin(math.radians(key*2)) * (2**32) #make a very big number using key*2
        interimb = math.floor(interimb) #make it int
        interimb = interimb*3 ^ (iterate*7) #xor (iterate*7)
        #print (interimb)
        interimc = interimb >> 5
        interimc = interimc << 5 #chop off a few bits
        #print (interimc)
        interimd = interimc << 3 #make another one
        interime = interimb ^ interimc
        interime += interimd
        # print (interime)
        interim -= interime
        #print (interim)
    #print (interim)
    interim = interim % 255
    print (interim)
    #print (interim+255)
    return interim+255
                       
def cdecode(array,key):
    output = ""
    random.seed(key)
    for h in range(len(array)):
        i = h + 1
        maths =(array[h]-cscramble(i,key))
        output = output + (chr(maths%255))
    return output

def cdecodeh(stringin,key):
    stredit = stringin.lower()
    if len(stringin)%2 == 1:
        stredit = "0" + stringin
    hexdigits = {"0" : 0 ,
                 "1" : 1 ,
                 "2" : 2 ,
                 "3" : 3 ,
                 "4" : 4 ,
                 "5" : 5 ,
                 "6" : 6 ,
                 "7" : 7 ,
                 "8" : 8 ,
                 "9" : 9 ,
                 "a" : 10 ,
                 "b" : 11 ,
                 "c" : 12 ,
                 "d" : 13 ,
                 "e" : 14 ,
                 "f" : 15}
    
    array = []                 
    for c in range(math.floor(len(stredit)/2)):
        ptr = c*2
        array.append((hexdigits[stredit[ptr]]*16)+hexdigits[stredit[ptr+1]])
        

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

    # print(cdecode(cencode("hello", 1),1))
    # a=cencode("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 1)
    # for j in range(len(a)):
    #     print(" "*math.floor(a[j]/2)+"#")
    #print(cencode("test", 1))
    print (cdecode([171, 214, 95, 155], 1))
    #print (chr(79))