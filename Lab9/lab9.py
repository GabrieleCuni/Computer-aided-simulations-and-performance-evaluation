import argparse
import json
import math
import hashlib
import random
import sys
from pympler import asizeof as p
import pandas as pd

def simulation(words):
    bExp = 1
    bExpMin = None    
    noWords = len(words)
    # To confront fingerprintSet size vs words size both must be the same data structure type, because a set with the same elements of a list
    # is bigger than a list in term of memory occupation. 
    # So I made words, that is a list, a set and below I use wordsSet to compare with fingerprintSet
    wordsSet = set(words) 

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
            print("ERR: IMPOSSIBLE TO FIND")
            break

        if collision is False:
            bExpMin = bExp
            print(f"bExp min is found: BexpMin:{bExpMin}")
            break        
       
    if bExpMin is None:
        print("bExp min is impossible to be found")
        sys.exit(1)

    fingerprintSetBytesSize = p.asizeof(fingerprintSet)
    wordsSetBytesSize = p.asizeof(wordsSet)
    bTeo = math.log((noWords/0.5),2)
    n = 2**bExpMin 
    pFalsePositive = 1 - ( 1 - 1/n )**noWords
    
    return bExpMin, bTeo, pFalsePositive, fingerprintSetBytesSize, wordsSetBytesSize

def genInputList():
    input_list = []
    for i in (2, 3, 4,5):
        a = [x*10**i for x in (1,2)]
        input_list.extend(a)
    input_list.pop()
    return input_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=int, default=42, help='Initial Seed')
    args = parser.parse_args()

    seed = args.seed
    random.seed(seed)

    # Load titles
    data_df = pd.read_csv('data.tsv',sep='\t') 
    mask = (data_df['region']=="IT")
    df = data_df.loc[mask, 'title'] # Take the title column where the region field is IT
    titleSet = set(df) # Delete all the duplicates
    titleList = list(titleSet) # Make it a list because list supports more operations

    random.shuffle(titleList)
    random.shuffle(titleList)
    noWords = len(titleList)
    print("INPUT PARAMETERS:")
    print(f"\tSeed: {seed}")
    print(f"\tTotal number of words: {noWords}")
    
    experiments_result = {
        "noWords":[],
        "bExpMin":[],
        "bTeo":[],
        "pFalsePositive":[],
        "fingerprintSetBytesSize":[],
        "wordsSetBytesSize":[]
    }

    for numberOfWords in genInputList():
        print("*********************************")
        bExpMin, bTeo, pFalsePositive, fingerprintSetBytesSize, wordsSetBytesSize = simulation(titleList[:numberOfWords]) 
        experiments_result["noWords"].append(numberOfWords)
        experiments_result["bExpMin"].append(bExpMin)
        experiments_result["bTeo"].append(bTeo)
        experiments_result["pFalsePositive"].append(pFalsePositive)
        experiments_result["fingerprintSetBytesSize"].append(fingerprintSetBytesSize)
        experiments_result["wordsSetBytesSize"].append(wordsSetBytesSize)

        print("RESULTS:")
        print(f"\tnoWords: {numberOfWords}")
        print(f"\tbExpMin: {bExpMin}")
        print(f"\tbTeo: {round(bTeo, 2)}")
        print(f"\tpFalsePositive: {pFalsePositive}")
        print(f"\tfingerprintSetBytesSize: {round(fingerprintSetBytesSize/(2**10),2)} Kbytes")
        print(f"\twordsSetBytesSize: {round(wordsSetBytesSize/(2**10),2)} Kbytes")

    
    json.dump(experiments_result, open("resultLab9.txt","w"))

if __name__ == "__main__":
    main()