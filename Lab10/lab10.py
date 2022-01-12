import argparse
import json
import math
import hashlib
import random
import sys
from pympler import asizeof as p
from bitarray import bitarray

def simulation(words, b):    
    noWords = len(words)
    # To confront fingerprintSet size vs words size both must be the same data structure type, because a set with the same elements of a list
    # is bigger than a list in term of memory occupation. 
    # So I made words, that is a list, a set and below I use wordsSet to compare with fingerprintSet
    wordsSet = set(words) 
    
    collision = False
    count = 0
    fingerprintSet = set()
    n = 2**b 
    bitArray = bitarray(n)
    for i in range(n):
        bitArray[i] = 0

    for word in words:
        word_hash = hashlib.md5(word.encode('utf-8')) # md5 hash
        word_hash_int = int(word_hash.hexdigest(), 16) # md5 hash in integer format
        fingerprint = word_hash_int % (2**b) # Take only the last digits. n = 2**b and map into [0,n-1] 
        if fingerprint in fingerprintSet:    
            collision = True  
            count += 1
        fingerprintSet.add(fingerprint)
        bitArray[fingerprint] = 1

    if collision is False:
        print(f"b:{b} makes no collisions")   
    else:
        print(f"Collision occured {count} times, b:{b} is not enough")

    fingerprintSetBytesSize = p.asizeof(fingerprintSet) # Bytes
    wordsSetBytesSize = p.asizeof(wordsSet) # Bytes
    bitArrayByteSize = p.asizeof(bitArray) # Bytes
    # bTeo = math.log((noWords/0.5),2) # WRONG
    bTeo = math.log((noWords/1.17)**2,2) # RIGHT
    pFalsePositive = 1 - ( 1 - 1/n )**noWords
    pSimFalsePositive = bitArray.count(1) / n
    
    return pSimFalsePositive, bTeo, pFalsePositive, fingerprintSetBytesSize, wordsSetBytesSize, bitArrayByteSize

def genInputList(noWords):
    input_list = []
    for i in (2, 3, 4, 5):
        a = [x*10**i for x in (1, 2)]
        input_list.extend(a)
    input_list.append(noWords)

    return input_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=int, default=42, help='Initial Seed')
    args = parser.parse_args()

    seed = args.seed
    random.seed(seed)

    # Load words
    data = json.load(open("words_dictionary.json")) # Words are stored as keys with value equal to 1 
    
    words = list(data.keys()) # Attention: I'm sure words are unique because python dictionary keys are unique!
    random.shuffle(words)
    random.shuffle(words)
    noWords = len(words)
    experimetList = [19, 20, 21, 22, 23, 24, 25, 26]
    print("INPUT PARAMETERS:")
    print(f"\tSeed: {seed}")
    print(f"\tTotal number of words: {noWords}")    
    print(f"\texperimentList: {experimetList}")
    
    experiments_result = {
        "b":[],
        "bTeo":[],
        "pSimFalsePositive": [],
        "pFalsePositive":[],
        "fingerprintSetBytesSize":[],
        "wordsSetBytesSize":[],
        "bitArrayByteSize":[]
    }    

    for b in experimetList:
        print("*********************************")
        pSimFalsePositive, bTeo, pFalsePositive, fingerprintSetBytesSize, wordsSetBytesSize, bitArrayByteSize = simulation(words, b) 
        experiments_result["b"].append(b)
        experiments_result["bTeo"].append(bTeo)
        experiments_result["pSimFalsePositive"].append(pSimFalsePositive)
        experiments_result["pFalsePositive"].append(pFalsePositive)
        experiments_result["fingerprintSetBytesSize"].append(fingerprintSetBytesSize)
        experiments_result["wordsSetBytesSize"].append(wordsSetBytesSize)
        experiments_result["bitArrayByteSize"].append(bitArrayByteSize)

        print("RESULTS:")
        print(f"\tb: {b}")
        print(f"\tbTeo: {round(bTeo, 2)}")
        print(f"\tpSimFalsePositive: {pSimFalsePositive}")
        print(f"\tpFalsePositive: {pFalsePositive}")
        print(f"\tfingerprintSetBytesSize: {round(fingerprintSetBytesSize/(2**10),2)} Kbytes")
        print(f"\twordsSetBytesSize: {round(wordsSetBytesSize/(2**10),2)} Kbytes")
        print(f"\tbitArrayByteSize: {round(bitArrayByteSize/(2**10),2)} Kbytes")

    
    json.dump(experiments_result, open("simResults.txt","w"))

if __name__ == "__main__":
    main()