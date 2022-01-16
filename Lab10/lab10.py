import argparse
import json
import math
import hashlib
import random
from pympler import asizeof as p
from bitarray import bitarray

# Compute the actual size of the fingerprint in bytes which is stored as integer
def getActualFPsize(fingerprintSet):
    dimensions = set()
    for fingerprint in fingerprintSet:
        dimensions.add(p.asizeof(fingerprint))
    actualFPsize = max(dimensions)
    print(f"fingerprint dimensions: {dimensions}, actualFPsize: {actualFPsize}")
    return actualFPsize

def simulation(words, b):    
    noWords = len(words)
    fingerprintSet = set()
    n = 2**b 
    bitArray = bitarray(n)
    # Initialize all bits to zero
    for i in range(n):
        bitArray[i] = 0

    for word in words:
        word_hash = hashlib.md5(word.encode('utf-8')) # md5 hash
        word_hash_int = int(word_hash.hexdigest(), 16) # md5 hash in integer format
        fingerprint = word_hash_int % (2**b) # Take only the last digits. n = 2**b and map into [0,n-1] 
        bitArray[fingerprint] = 1 # Set bit to one  
        fingerprintSet.add(fingerprint)
    
    # Compute all the output parameters
    pFPTheo = 1 - ( 1 - 1/n )**noWords
    pFPSim = bitArray.count(1) / n
    bsTheoByte = n / 8
    bsSimByte = p.asizeof(bitArray) # Bytes
    fpSimByte = p.asizeof(fingerprintSet)
    fpTheoByte  = math.ceil( (b * len(fingerprintSet)) / 8 )
    actualFPsize = getActualFPsize(fingerprintSet)
    fpTheoExpectedByte = actualFPsize * len(fingerprintSet)
    
    return pFPTheo, pFPSim, bsTheoByte, bsSimByte, fpSimByte, fpTheoByte, actualFPsize, fpTheoExpectedByte

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
        "pFPTheo":[],
        "pFPSim":[],
        "bsTheoByte":[],
        "bsSimByte":[],
        "fpSimByte":[],
        "fpTheoByte":[],
        "fpTheoExpectedByte":[]
    }    

    for b in experimetList:
        print("*********************************")
        pFPTheo, pFPSim, bsTheoByte, bsSimByte, fpSimByte, fpTheoByte, actualFPsize, fpTheoExpectedByte = simulation(words, b) 
        experiments_result["b"].append(b)
        experiments_result["pFPTheo"].append(pFPTheo)
        experiments_result["pFPSim"].append(pFPSim)
        experiments_result["bsTheoByte"].append(bsTheoByte)
        experiments_result["bsSimByte"].append(bsSimByte)
        experiments_result["fpSimByte"].append(fpSimByte)
        experiments_result["fpTheoByte"].append(fpTheoByte)
        experiments_result["fpTheoExpectedByte"].append(fpTheoExpectedByte)

        print("RESULTS:")
        print(f"\tb: {b}")
        print(f"\tpFPTheo: {pFPTheo}")
        print(f"\tpFPSim: {pFPSim}")
        print(f"\tbsTheoByte: {int(round(bsTheoByte/(2**10),2))} KB")
        print(f"\tbsSimByte: {int(round(bsSimByte/(2**10),2))} KB")
        print(f"\tfpTheoByte: {int(round(fpTheoByte/(2**10),2))} KB")
        print(f"\tfpTheoExpectedByte: {int(round(fpTheoExpectedByte/(2**10),2))} KB")
        print(f"\tfpSimByte: {int(round(fpSimByte/(2**10),2))} KB")
        print(f"\tactualFPsize: {actualFPsize} Byte")     

    json.dump(experiments_result, open("lab10Results.txt","w"))

if __name__ == "__main__":
    main()