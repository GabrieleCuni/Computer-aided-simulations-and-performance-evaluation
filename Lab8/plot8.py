import matplotlib.pyplot as plt
import argparse
import json

# def plot_graph(data, figureNumber):     
#     # Select your favourite window length x and y will computed to be a 16/10 window
#     # x=10
#     # y=(x / 16)*10 
#     # plt.figure(figsize=(x,y))    
#     plt.figure()
#     plt.fill_between(data["noPeople"], data["ciLb"], data["ciUb"], color='b', alpha=.1, label=f"cl = {data['ciCl']}")
#     plt.plot(data["noPeople"], data["x_hat"], label='Simulation Result', marker='o', color="orange", alpha=.5)
#     plt.plot(data["noPeople"], data["pTheo"], linestyle="dotted", label="Theoretical formula", color="black") 
#     plt.xlabel('n: Number of People' + "\n" + f"Figure {figureNumber}")
#     plt.ylabel('Prob(Birthday Collision)')
#     plt.legend()
#     plt.grid()
#     plt.title("Uniform Birthday Popularity " + "\n" + parameters)
#     plt.savefig("UBP-" + parameters + ".png")
#     plt.show()
#     plt.clf()

def main():
    inputFileName = "experiments_result.txt"

    data = json.load(open(inputFileName))
    
    plt.figure()
    plt.plot(data["noWords"], data["bExpMin"], marker='o', label="bExpMin")
    plt.plot(data["noWords"], data["bTeo"], marker='o', label="bTeo")
    plt.xlabel("Number of words")
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
    plt.xlabel("Number of words")
    plt.ylabel("Probability of false positive")
    plt.savefig("pFalsePositive.png")
    plt.show()
    
if __name__ == "__main__":
    main()