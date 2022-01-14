import argparse
import json
import math
import hashlib
import random
import sys
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
        return -1
    for i in range(num_hashes): # for each hash to generate
        if debug:
            print("{0:b}".format(md5)) # print the md5 value in binary
        value=md5 % (2 ** b) # take the last b bits for the hash value
        bits_to_update.append(value) # add the hash value in the list
        if debug:
            print("Hash value:",value,"\t{0:b}".format(value)) # debug
        md5 = md5 // (2 ** 3) # right-shift the md5 by 3 bits
    return bits_to_update


# # compute the hash
# word_hash = hashlib.md5('ciao'.encode('utf-8')) # example for 'ciao'
# word_hash_int = int(word_hash.hexdigest(), 16) # compute the hash
# all_bits_to_update=compute_all_hashes(word_hash_int, 32, 24) # compute 32 hash values on 24 bits
# print(all_bits_to_update) # show the obtained hash values

def bloomFilterInsertion(bitArray, all_bits_to_update, k):
    for j in range(k):
        bitArray[all_bits_to_update[j]] = 1

    return bitArray

def simulation(words, b):    
    noWords = len(words)
    # To confront fingerprintSet size vs words size both must be the same data structure type, because a set with the same elements of a list
    # is bigger than a list in term of memory occupation. 
    # So I made words, that is a list, a set and below I use wordsSet to compare with fingerprintSet
    wordsSet = set(words) 
    
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

    wordsSetBytesSize = p.asizeof(wordsSet) # Bytes
    filterStorageRealInBytes = p.asizeof(bitArray) # Bytes
    pFPTheo = ( 1 - math.exp((-kOpt*noWords)/n) )**kOpt
    pFPSim = (bitArray.count(1) / n)**kOpt
    filterStorageTheoBits = noWords * ( 1.44*math.log(1/pFPTheo, 2) )
    
    return pFPSim, pFPTheo, filterStorageRealInBytes, wordsSetBytesSize, filterStorageTheoBits, kOpt


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
    experimetList = [19, 20, 21, 22, 23]
    print("INPUT PARAMETERS:")
    print(f"\tSeed: {seed}")
    print(f"\tTotal number of words: {noWords}")    
    print(f"\texperimentList: {experimetList}")
    
    experiments_result = {
        "b":[],
        "pFPSim":[],
        "pFPTheo":[],
        "filterStorageRealInBytes": [],
        "wordsSetBytesSize":[],
        "filterStorageTheo":[]
    }    

    for b in experimetList:
        print("*********************************")
        pFPSim, pFPTheo, filterStorageRealInBytes, wordsSetBytesSize, filterStorageTheoBits, kOpt = simulation(words, b) 
        experiments_result["b"].append(b)
        experiments_result["pFPSim"].append(pFPSim)
        experiments_result["pFPTheo"].append(pFPTheo)
        experiments_result["filterStorageRealInBytes"].append(filterStorageRealInBytes)
        experiments_result["wordsSetBytesSize"].append(wordsSetBytesSize)
        experiments_result["filterStorageTheo"].append(filterStorageTheoBits)

        print("RESULTS:")
        print(f"\tb: {b}")
        print(f"\tpFPSim: {pFPSim}")
        print(f"\tpFPTheo: {pFPTheo}")
        print(f"\tfilterStorageRealInBytes: {int(round(filterStorageRealInBytes/(2**10),0))} Kbytes")
        print(f"\tfilterStorageTheoBits: {int(round((filterStorageTheoBits/8)/(2**10),0))} kbytes")
        print(f"\twordsSetBytesSize: {int(round(wordsSetBytesSize/(2**10),0))} Kbytes")        
        print(f"\tkOpt: {kOpt}")

    
    json.dump(experiments_result, open("lab11Results.txt","w"))

if __name__ == "__main__":
    main()