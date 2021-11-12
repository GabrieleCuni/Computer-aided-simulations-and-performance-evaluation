import matplotlib.pyplot as plt
import argparse
import json

def plot_graph(experiment_results):  
    title = f"seed={experiment_results['seed']} - noRuns={experiment_results['noRuns']} - CL={experiment_results['cl']} - d={experiment_results['d']} - alpha={experiment_results['alpha']}"
    plt.plot(experiment_results["n"], experiment_results["theo"], linestyle="dotted", label="Theoretical formula")  
    plt.plot(experiment_results["n"], experiment_results["tub"], linestyle="dotted", label="Theoretical UB")
    plt.plot(experiment_results["n"], experiment_results["x_hat"], label='Average max bin occupancy',marker='o')
    plt.xscale("log")
    plt.fill_between(experiment_results["n"], experiment_results["CI_LB"], experiment_results["CI_UB"], color='b', alpha=.1, label="Confidence Interval")
    plt.xlabel('n: Number of bins and balls')
    plt.ylabel('Average max bin occupancy')
    # plt.ylim(bottom=0)
    plt.legend()
    plt.title("Average max bin occupancy" + "\n" + title)
    plt.savefig("AvgMaxBinOcc -" + title + ".png")
    # plt.show()
    plt.clf()

def plotTheoreticalResult(seed, noRuns, cl):    
    inputFileName = f"binsballs_seed={seed}_runs={noRuns}_d={1}_cl={cl}_alpha=1.txt"
    experiment_results1 = json.load(open(inputFileName))
    inputFileName = f"binsballs_seed={seed}_runs={noRuns}_d={2}_cl={cl}_alpha=1.txt"
    experiment_results2 = json.load(open(inputFileName))
    inputFileName = f"binsballs_seed={seed}_runs={noRuns}_d={4}_cl={cl}_alpha=1.txt"
    experiment_results4 = json.load(open(inputFileName))

    title = f"seed={experiment_results1['seed']} - noRuns={experiment_results1['noRuns']} - CL={experiment_results1['cl']} - alpha=1"
    plt.plot(experiment_results1["n"], experiment_results1["theo"], label="Random Dropping")
    plt.plot(experiment_results2["n"], experiment_results2["theo"], linestyle="dotted", label="Random Load Balancing d=2")
    plt.plot(experiment_results4["n"], experiment_results4["theo"], linestyle="dotted", label="Random Load Balancing d=4")
    plt.ylabel("Maximum occupancy")
    plt.xlabel("n: Number of bins and balls")
    plt.xscale("log")
    plt.grid()
    plt.legend()
    plt.title("Theoretical results for randomized dropping policies")
    plt.savefig("Theo" + title + ".png")
    plt.clf()
    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', '-s', type=int, default=42, help='Initial Seed')
    parser.add_argument('--confidenceLevel', '-cl', type=int, default=0.95, help='Confidence Level')
    parser.add_argument('--noRuns', '-r', type=int, default=5, help='Number of runs')
    parser.add_argument("-d", type=int, default=1, help="Number of balancing bins")
    parser.add_argument("-t", "--thoretical", action="store_true", help="Ploting theoretical formulas")
    parser.add_argument("-a", "--alpha", type=float, default=1)
    args = parser.parse_args()

    seed = args.seed
    confidence_level = args.confidenceLevel
    noRuns = args.noRuns
    d = args.d
    theo = args.thoretical
    alpha = args.alpha
    inputFileName = f"binsballs_seed={seed}_runs={noRuns}_d={d}_cl={confidence_level}_alpha={alpha}.txt"

    experiment_results = json.load(open(inputFileName))

    plot_graph(experiment_results)
    if theo is True:
        plotTheoreticalResult(seed, noRuns, confidence_level)


if __name__ == "__main__":
    main()
