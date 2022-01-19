import matplotlib.pyplot as plt
import json
import numpy as np

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
    data = json.load(open("lab11Results.txt"))
    dL10 = json.load(open("lab10Results.txt"))

    
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