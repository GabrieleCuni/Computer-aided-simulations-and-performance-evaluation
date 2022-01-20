import argparse
import json
import math
import hashlib
import random
import sys
import numpy as np
from pympler import asizeof as p
from bitarray import bitarray

def compute_all_hashes(md5, num_hashes, b):
    # returns the list of num_hashes indexes corresponding to all the bits to update in a bloom filter
    # md5 is the hash integer value obtained by md5, on 128 bits
    # num_hashes is the number of hash values to generate
    # b is the number of bits such that the bit array is of size 2**b
    debug=False # flag to obtain debug info, useful to understand how the function work
    bits_to_update=[] # the list of bits to update is initially empty
    if (b+3*num_hashes>128): # check the condition about the max number of supported hashes
        print("Error - at most 32 hashes")
        sys.exit(1)
    for i in range(num_hashes): # for each hash to generate
        if debug:
            print("{0:b}".format(md5)) # print the md5 value in binary
        value=md5 % (2 ** b) # take the last b bits for the hash value
        bits_to_update.append(value) # add the hash value in the list
        if debug:
            print("Hash value:",value,"\t{0:b}".format(value)) # debug
        md5 = md5 // (2 ** 3) # right-shift the md5 by 3 bits
    return bits_to_update

def bloomFilterInsertion(bitArray, all_bits_to_update, k):
    for j in range(k):
        bitArray[all_bits_to_update[j]] = 1

    return bitArray

def simulation(words, b):    
    noWords = len(words)    
    n = 2**b 
    kOpt = math.ceil( (n/noWords) * math.log(2) )
    bitArray = bitarray(n)
    for i in range(n):
        bitArray[i] = 0

    for word in words:
        word_hash = hashlib.md5(word.encode('utf-8')) # md5 hash
        word_hash_int = int(word_hash.hexdigest(), 16) # md5 hash in integer format
        all_bits_to_update = compute_all_hashes(word_hash_int, kOpt, b) # compute kOpt hash values on b bits

        bitArray = bloomFilterInsertion(bitArray, all_bits_to_update, kOpt)

    pFPTheo = ( 1 - math.exp((-kOpt*noWords)/n) )**kOpt
    pFPSim = (bitArray.count(1) / n)**kOpt
    bfSimByte =  p.asizeof(bitArray)
    bfTheoByte = (noWords * ( 1.44*math.log(1/pFPTheo, 2) )) / 8 # Bloom filter
    bsTheoByte = (noWords/(1 - ( 1 - 1/n )**noWords)) / 8 # Bit String Array
    ftTheoByte = (noWords * math.log(noWords/(1 - ( 1 - 1/n )**noWords), 2)) / 8 # Fingerprint in a table
    
    return pFPSim, pFPTheo, bfSimByte, bfTheoByte, bsTheoByte, ftTheoByte, kOpt

def optionalOne(m, experimetList):
    exp = []
    kOptList = []
    pFPList = []
    for b in experimetList:
        n = 2**b
        kOpt = math.ceil( (n/m) * math.log(2))
        print(f"b = {b} -> kOpt = {kOpt}")
        kOptList.append(  kOpt )
        pFPList.append( ( 1 - math.exp((-kOpt*m)/n) )**kOpt )
        tmp = []
        for k in range(1,33): # [1,33)
            pFP = ( 1 - math.exp((-k*m)/n) )**k
            tmp.append(pFP)
        exp.append(tmp)
    return exp, kOptList, pFPList

def optionalTwo(words, b):
    noWords = len(words)    
    n = 2**b 
    kOpt = math.ceil( (n/noWords) * math.log(2) )
    bitArray = bitarray(n)
    for i in range(n):
        bitArray[i] = 0

    d = {
        "noWords":[],
        "distEl":[]
    }
    count = 0
    print("************************************")
    for word in words:
        count += 1
        word_hash = hashlib.md5(word.encode('utf-8')) # md5 hash
        word_hash_int = int(word_hash.hexdigest(), 16) # md5 hash in integer format
        all_bits_to_update = compute_all_hashes(word_hash_int, kOpt, b) # compute kOpt hash values on b bits

        bitArray = bloomFilterInsertion(bitArray, all_bits_to_update, kOpt)
        distEl = (-n/kOpt) * math.log(1-(bitArray.count(1)/n))
        d["noWords"].append(count)
        d["distEl"].append(distEl)
        print(f"\tInserted Words: {count}, distinct Elements Theo: {int(distEl)}", end="\r")
    
    return d


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=int, default=42, help='Initial Seed')
    parser.add_argument("-a", action="store_true", help="Optional one")
    parser.add_argument("-b", action="store_true", help="Optional two")
    args = parser.parse_args()

    seed = args.seed
    random.seed(seed)

    # Load words
    data = json.load(open("words_dictionary.json")) # Words are stored as keys with value equal to 1 
    
    words = list(data.keys()) # Attention: I'm sure words are unique because python dictionary keys are unique!
    random.shuffle(words)
    random.shuffle(words)
    noWords = len(words)
    experimetList = [19, 20, 21, 22, 23]

    if args.a is True:
        exp, kOptList, pFPList= optionalOne(noWords, experimetList)
        option1Dict={
            "exp":exp,
            "kOptList":kOptList,
            "pFPList":pFPList
        }
        json.dump(option1Dict, open("lab11ResultsOptional1.txt","w"))
        print("lab11ResultsOptional1.txt made")
        sys.exit(0)

    if args.b is True:
        print("INPUT PARAMETERS:")
        print(f"\tSeed: {seed}")
        print(f"\tTotal number of words: {len(words[:170000])}")    
        print(f"\tb: 23")
        d = optionalTwo(words[:170000], 23)
        json.dump(d, open("lab11ResultsOptional2.txt","w"))
        print("lab11ResultsOptional2.txt made")
        sys.exit(0)

    print("INPUT PARAMETERS:")
    print(f"\tSeed: {seed}")
    print(f"\tTotal number of words: {noWords}")    
    print(f"\texperimentList: {experimetList}")
    
    experiments_result = {
        "b":[],
        "pFPSim":[],
        "pFPTheo":[],
        "bfSimByte": [],
        "bfTheoByte":[],
        "bsTheoByte":[],
        "ftTheoByte":[],
        "kOpt":[]
    }    

    for b in experimetList:
        print("*********************************")
        pFPSim, pFPTheo, bfSimByte, bfTheoByte, bsTheoByte, ftTheoByte, kOpt = simulation(words, b) 
        experiments_result["b"].append(b)
        experiments_result["pFPSim"].append(pFPSim)
        experiments_result["pFPTheo"].append(pFPTheo)
        experiments_result["bfSimByte"].append(bfSimByte)
        experiments_result["bfTheoByte"].append(bfTheoByte)
        experiments_result["bsTheoByte"].append(bsTheoByte)
        experiments_result["ftTheoByte"].append(ftTheoByte)
        experiments_result["kOpt"].append(kOpt)
        

        print("RESULTS:")
        print(f"\tb: {b}")
        print(f"\tkOpt: {kOpt}")
        print(f"\tpFPSim: {pFPSim}")
        print(f"\tpFPTheo: {pFPTheo}")
        print(f"\tbfSimByte: {int(round(bfSimByte/(2**10),0))} Kbytes")
        print(f"\tbfTheoByte: {int(round(bfTheoByte/(2**10),0))} kbytes")
        print(f"\tbsTheoByte: {int(round(bsTheoByte/(2**10),0))} Kbytes")       
        print(f"\tftTheoByte: {int(round(ftTheoByte/(2**10),0))} Kbytes")  
        

    
    json.dump(experiments_result, open("lab11Results.txt","w"))

if __name__ == "__main__":
    main()