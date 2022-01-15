import matplotlib.pyplot as plt
import argparse
import json
import numpy as np

# DATA
#         "b":[],
#         "pFPTheo":[],
#         "pFPSim":[],
#         "bsTheoByte":[],
#         "bsSimByte":[],
#         "fpSimByte":[],
#         "fpTheoByte":[],
#         "fpTheoExpectedByte":[]
#        

def main():
    inputFileName = "lab10Results.txt"

    data = json.load(open(inputFileName))
    
    plt.figure()
    plt.plot(data["b"], data["pFPSim"], linewidth=2, alpha=0.5, marker='o', label="Simulation results")
    plt.plot(data["b"], data["pFPTheo"], linewidth=3, linestyle="dotted", label="Theoretical results")
    plt.xlabel("Number of bits b")
    plt.ylabel("Probability of false positive")
    # plt.xscale("log")
    plt.legend()
    plt.grid()
    # plt.title("epsilon1e-5")
    plt.savefig("pFP.png")
    plt.show()

    plt.figure()
    
    plt.plot(data["b"], np.array(data["bsSimByte"])/(2**20), linewidth=2, alpha=0.5, marker='o', label="bsSimByte")
    plt.plot(data["b"], np.array(data["bsTheoByte"])/(2**20),linewidth=3, linestyle="dotted", label="bsTheoByte")
    plt.plot(data["b"], np.array(data["fpSimByte"])/(2**20), marker='o', alpha=0.5, label="fpSimByte")
    plt.plot(data["b"], np.array(data["fpTheoByte"])/(2**20), linestyle="dotted", label="fpTheoByte")
    plt.plot(data["b"], np.array(data["fpTheoExpectedByte"])/(2**20), linestyle="dotted", label="fpTheoExpectedByte")
    plt.yscale("log")
    plt.grid()
    plt.legend()
    plt.xlabel("Number of bits b")
    plt.ylabel("Memory occupancy [MB]")
    plt.savefig("mem.png")
    plt.show()

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