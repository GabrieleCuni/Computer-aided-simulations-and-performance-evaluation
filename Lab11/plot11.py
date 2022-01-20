import matplotlib.pyplot as plt
import json
import sys
import numpy as np
import argparse

# DATA
# "b":[],
# "pFPSim":[],
# "pFPTheo":[],
# "bfSimByte": [],
# "bfTheoByte":[],
# "bsTheoByte":[],
# "ftTheoByte":[],
# "kOpt":[]
       

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", action="store_true", help="Optional one")
    args = parser.parse_args()

    data = json.load(open("lab11Results.txt"))
    dL10 = json.load(open("lab10Results.txt"))

    if args.a is True:
        opt1 = json.load(open("lab11ResultsOptional1.txt"))
        exp = opt1["exp"]
        kOptList = opt1["kOptList"]
        pFPList = opt1["pFPList"]
        plt.figure()
        plt.plot(list(range(1,33)), exp[0], label="b = 19")
        plt.plot(list(range(1,33)), exp[1], label="b = 20")
        plt.plot(list(range(1,33)), exp[2], label="b = 21")
        plt.plot(kOptList[0], pFPList[0], "ro", label="kOpt for b=19")
        plt.plot(kOptList[1], pFPList[1], "ob", label="kOpt for b=20")
        plt.plot(kOptList[2], pFPList[2], "og", label="kOpt for b=21")
        plt.xlabel("k: Number of hash function")
        plt.ylabel("Probability of false positive")
        plt.legend()
        plt.savefig("pFPvsK1.png")
        plt.show()

        plt.figure()
        plt.plot(list(range(1,33)), exp[3], label="b = 22")
        plt.plot(list(range(1,33)), exp[4], label="b = 23")
        plt.plot(kOptList[3], pFPList[3], "ro", label="kOpt for b=22")
        plt.plot(kOptList[4], pFPList[4], "ob", label="kOpt for b=23")
        plt.xlabel("k: Number of hash function")
        plt.ylabel("Probability of false positive")
        plt.legend()
        plt.savefig("pFPvsK2.png")
        plt.show()
        sys.exit(0)

    
    plt.figure()
    plt.plot(data["b"], data["pFPSim"], linewidth=2, alpha=0.5, marker='o', label="Simulation results")
    plt.plot(data["b"], data["pFPTheo"], linewidth=3, linestyle="dotted", label="Theoretical results")
    plt.xticks(data["b"])
    plt.xlabel("Number of bits b")
    plt.ylabel("Probability of false positive")
    plt.title("Bloom Filter")
    plt.legend()
    plt.grid()
    plt.savefig("pFPlab11.png")
    plt.show()

    plt.figure()
    plt.plot(data["b"], data["pFPSim"], alpha=0.5, marker='o', label="Bloom Filter")
    plt.plot(np.array(dL10["b"])[:5], np.array(dL10["pFPSim"])[:5], alpha=0.5, marker='o', label="Bit String Array")
    plt.xticks(data["b"])
    plt.xlabel("Number of bits b")
    plt.ylabel("Probability of false positive")
    plt.title("Bloom Filter vs Bit String Array")
    plt.legend()
    plt.grid()
    plt.savefig("BFvsBSlab11.png")
    plt.show()

    plt.figure()
    plt.plot(data["b"], np.array(data["bfTheoByte"])/(2**10), linewidth=3, linestyle="dotted", label="Bloom Filter Theoretical")
    plt.plot(data["b"], np.array(data["bsTheoByte"])/(2**10), linewidth=3, linestyle="dotted", label="Bit String Array")
    plt.plot(data["b"], np.array(data["ftTheoByte"])/(2**10), linewidth=3, linestyle="dotted", label="Fingerprint in Table")
    plt.plot(data["b"], np.array(data["bfSimByte"])/(2**10), linewidth=2, alpha=0.5, marker='o', label="Bloom Filter Simulation")
    plt.xticks(data["b"])
    plt.yscale("log")
    plt.grid()
    plt.legend()
    plt.xlabel("Number of bits b")
    plt.ylabel("Memory occupancy [KB]")
    plt.savefig("memLab11.png")
    plt.show()

    

    # plt.figure()
    
    # plt.plot(data["b"], np.array(data["bsSimByte"])/(2**20), linewidth=2, alpha=0.5, marker='o', label="Bit Array simulation")
    # plt.plot(data["b"], np.array(data["bsTheoByte"])/(2**20),linewidth=3, linestyle="dotted", label="Bit Array theoretical")
    # plt.plot(data["b"], np.array(data["fpSimByte"])/(2**20), marker='o', alpha=0.5, label="Fingerprint Set simulation")
    # plt.plot(data["b"], np.array(data["fpTheoByte"])/(2**20), linestyle="dotted",color="black", label="Fingerprint theoretical")
    # plt.plot(data["b"], np.array(data["fpTheoExpectedByte"])/(2**20), linestyle="dotted", label="Fingerprint as integer theoretical")
    # plt.yscale("log")
    # plt.grid()
    # plt.legend()
    # plt.xlabel("Number of bits b")
    # plt.ylabel("Memory occupancy [MB]")
    # plt.savefig("mem.png")
    # plt.show()
    
if __name__ == "__main__":
    main()