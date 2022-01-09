import argparse
import json
import math
import hashlib
import random
import sys

def simulation(words):
    bExp = 1
    bExpMin = None    
    noWords = len(words)

    while(True):
        collision = False
        fingerprintSet = set()
        for word in words:
            word_hash = hashlib.md5(word.encode('utf-8')) # md5 hash
            word_hash_int = int(word_hash.hexdigest(), 16) # md5 hash in integer format
            fingerprint = word_hash_int % (2**bExp) # Take only the last Bexp digits. n = 10**Bexp and map into [0,n-1] 
            if fingerprint in fingerprintSet:
                # print(f"Collision occured, bExp:{bExp} is not enough")
                bExp += 1       
                collision = True     
                break
            else:
                fingerprintSet.add(fingerprint)

        if 2**bExp > 10**39: # more than 39 means you want more than 39 last digits, but md5 has only 39 digits in integer format
            break

        if collision is False:
            bExpMin = bExp
            print(f"bExp min is found: BexpMin:{bExpMin}")
            break        
       
    if bExpMin is None:
        print("bExp min is impossible to be found")
        sys.exit(1)

    bTeo = math.log((noWords/0.5),2)
    n = 2**bExpMin 
    pFalsePositive = 1 - ( 1 - 1/n )**noWords
    
    return bExpMin, bTeo, pFalsePositive

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
    random.shuffle(words)
    random.shuffle(words)
    noWords = len(words)
    print(f"Total number of words: {noWords}")
    
    experiments_result = {"noWords":[],"bExpMin":[],"bTeo":[],"pFalsePositive":[]}
    for numberOfWords in genInputList():
        print("*********************************")
        bExpMin, bTeo, pFalsePositive = simulation(words[:numberOfWords]) 
        experiments_result["noWords"].append(numberOfWords)
        experiments_result["bExpMin"].append(bExpMin)
        experiments_result["bTeo"].append(bTeo)
        experiments_result["pFalsePositive"].append(pFalsePositive)

        print("RESULTS:")
        print(f"\tnoWords: {numberOfWords}")
        print(f"\tbExpMin: {bExpMin}")
        print(f"\tbTeo: {round(bTeo, 2)}")
        print(f"\tpFalsePositive: {pFalsePositive}")

    
    json.dump(experiments_result, open("experiments_result.txt","w"))

if __name__ == "__main__":
    main()