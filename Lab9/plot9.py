import matplotlib.pyplot as plt
import argparse
import json
import numpy as np

def main():
    inputFileName = "resultLab9.txt"

    data = json.load(open(inputFileName))
    
    plt.figure()
    plt.plot(data["noWords"], data["bExpMin"], marker='o', label="bExpMin")
    plt.plot(data["noWords"], data["bTeo"], marker='o', label="bTeo")
    plt.xlabel("Number of titles")
    plt.ylabel("Number of bits")
    plt.xscale("log")
    plt.legend()
    plt.grid()
    # plt.title("epsilon1e-5")
    plt.savefig("plot.png")
    plt.show()

    plt.figure()
    plt.plot(data["noWords"], data["pFalsePositive"], marker='o')
    plt.xscale("log")
    plt.grid()
    plt.xlabel("Number of titles")
    plt.ylabel("Probability of false positive")
    plt.savefig("pFalsePositive.png")
    plt.show()

    plt.figure()
    plt.plot(data["noWords"], np.array(data["fingerprintSetBytesSize"])/2**20, marker='o', label="fingerprintSet size")
    plt.plot(data["noWords"], np.array(data["wordsSetBytesSize"])/2**20, marker="o", label="wordsSet size")
    plt.plot(data["noWords"], (np.array(data["bTeo"])*np.array(data["noWords"]))/2**20, marker="o", label="m times bTeo")
    plt.ylabel("Memory occupancy in MB")
    plt.xscale("log")
    plt.xlabel("Number of titles")
    plt.grid()
    plt.legend()
    plt.savefig("ratio.png")
    plt.show()
    
if __name__ == "__main__":
    main()