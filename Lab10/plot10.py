import matplotlib.pyplot as plt
import argparse
import json
import numpy as np

# data keys:
#         "b":[],
#         "bTeo":[],
#         "pSimFalsePositive": [],
#         "pFalsePositive":[],
#         "fingerprintSetBytesSize":[],
#         "wordsSetBytesSize":[],
#         "bitArrayByteSize":[]

def main():
    inputFileName = "simResults.txt"

    data = json.load(open(inputFileName))
    
    plt.figure()
    plt.plot(data["b"], data["pSimFalsePositive"], marker='o', label="pSimFalsePositive")
    plt.plot(data["b"], data["pFalsePositive"], marker='o', label="pFalsePositive")
    plt.xlabel("Number of bits b")
    plt.ylabel("Probability of false positive")
    # plt.xscale("log")
    plt.legend()
    plt.grid()
    # plt.title("epsilon1e-5")
    plt.savefig("plot.png")
    plt.show()

    # plt.figure()
    # plt.plot(data["noWords"], data["pFalsePositive"], marker='o')
    # plt.xscale("log")
    # plt.grid()
    # plt.xlabel("Number of words")
    # plt.ylabel("Probability of false positive")
    # plt.savefig("pFalsePositive.png")
    # plt.show()

    # plt.figure()
    # plt.plot(data["noWords"], np.array(data["fingerprintSetBytesSize"])/2**20, marker='o', label="fingerprintSet size")
    # plt.plot(data["noWords"], np.array(data["wordsSetBytesSize"])/2**20, marker="o", label="wordsSet size")
    # plt.plot(data["noWords"], (np.array(data["bTeo"])*np.array(data["noWords"]))/2**20, marker="o", label="m times bTeo")
    # plt.ylabel("Memory occupancy in MB")
    # plt.xscale("log")
    # plt.yscale("log")
    # plt.xlabel("Number of words")
    # plt.grid()
    # plt.legend()
    # plt.savefig("ratio.png")
    # plt.show()
    
if __name__ == "__main__":
    main()