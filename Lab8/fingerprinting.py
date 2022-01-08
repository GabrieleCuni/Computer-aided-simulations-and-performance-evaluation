import argparse
import json
import math
import hashlib
import random

def simulation(words):
    digitsExp = 1
    digitsExpMin = None    
    noWords = len(words)

    while(True):
        collision = False
        fingerprintSet = set()
        for word in words:
            word_hash = hashlib.md5(word.encode('utf-8')) # md5 hash
            word_hash_int = int(word_hash.hexdigest(), 16) # md5 hash in integer format
            fingerprint = word_hash_int % (10**digitsExp) # Take only the last Bexp digits. n = 10**Bexp and map into [0,n-1] 
            if fingerprint in fingerprintSet:
                print(f"Collision occured, digitsExp:{digitsExp} is not enough")
                digitsExp += 1       
                collision = True     
                break
            else:
                fingerprintSet.add(fingerprint)

        if digitsExp > 39: # more than 39 means you want more than 39 last digits, but md5 has only 39 digits in integer format
            print("digitsExp min is impossible to be found")
            break

        if collision is False and digitsExp <= 39:
            digitsExpMin = digitsExp
            print(f"digitsExp min is found: BexpMin:{digitsExpMin}")
            break        
       
    digitsTeo = math.log((noWords/0.5),10)
    Bteo = math.log((noWords/0.5),2)
    # print(f"digitsTeo:{digitsTeo} vs digitsExpMin:{digitsExpMin}")

    n = 10**digitsExpMin 
    pFalsePositive = 1 - ( 1 - 1/n )**noWords
    # print(f"P('False positive')={pFalsePositive}")
    return digitsExpMin, digitsTeo, pFalsePositive, Bteo

def genInputList():
    input_list = []
    for i in (2, 3, 4, 5):
        a = [x*10**i for x in (1, 2)]
        input_list.extend(a)

    return input_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=int, default=42, help='Initial Seed')
    # parser.add_argument('-r', '--noRuns', type=int, default=5, help='Number of runs')
    # parser.add_argument('-cl', '--confidenceLevel', type=int, default=0.95, help='Confidence Level')
    args = parser.parse_args()

    seed = args.seed
    random.seed(seed)

    # Load words
    data = json.load(open("words_dictionary.json")) # Words are stored as keys with value equal to 1 

    
    words = list(data.keys()) # Attention: I'm sure words are unique because python dictionary keys are unique!
    noWords = len(words)
    print(f"Total number of words: {noWords}")
    
    experiments_result = {"noWords":[],"digitsExpMin":[],"digitsTeo":[],"pFalsePositive":[],"Bteo":[]}
    for numberOfWords in genInputList():
        print("*********************************")
        print(f"Number of words: {numberOfWords}")
        digitsExpMin, digitsTeo, pFalsePositive, Bteo = simulation(words[:numberOfWords])
        experiments_result["noWords"].append(numberOfWords)
        experiments_result["digitsExpMin"].append(digitsExpMin)
        experiments_result["digitsTeo"].append(digitsTeo)
        experiments_result["pFalsePositive"].append(pFalsePositive)
        experiments_result["Bteo"].append(Bteo)

    
    json.dump(experiments_result, open("experiments_result.txt","w"))

if __name__ == "__main__":
    main()