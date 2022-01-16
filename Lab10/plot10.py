import matplotlib.pyplot as plt
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
    plt.legend()
    plt.grid()
    plt.savefig("pFP.png")
    plt.show()

    plt.figure()
    
    plt.plot(data["b"], np.array(data["bsSimByte"])/(2**20), linewidth=2, alpha=0.5, marker='o', label="Bit Array simulation")
    plt.plot(data["b"], np.array(data["bsTheoByte"])/(2**20),linewidth=3, linestyle="dotted", label="Bit Array theoretical")
    plt.plot(data["b"], np.array(data["fpSimByte"])/(2**20), marker='o', alpha=0.5, label="Fingerprint Set simulation")
    plt.plot(data["b"], np.array(data["fpTheoByte"])/(2**20), linestyle="dotted",color="black", label="Fingerprint theoretical")
    plt.plot(data["b"], np.array(data["fpTheoExpectedByte"])/(2**20), linestyle="dotted", label="Fingerprint as integer theoretical")
    plt.yscale("log")
    plt.grid()
    plt.legend()
    plt.xlabel("Number of bits b")
    plt.ylabel("Memory occupancy [MB]")
    plt.savefig("mem.png")
    plt.show()
    
if __name__ == "__main__":
    main()