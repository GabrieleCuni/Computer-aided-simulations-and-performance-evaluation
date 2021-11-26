import matplotlib.pyplot as plt
import argparse
import json

"""
experiment_results = {
        "noPeople": noPeopleList,
        "noDays": noDays,
        "noRuns": noRuns,
        "noProbs": noProbs,
        "ciCl": ciCl,
        "seed": seed,
        "d": d,
        "pTheo":[],
        "ciLb":[], 
        "x_hat":[], 
        "ciUb":[], 
        "ciRe":[]      
    }
"""

def plot_graph(data):     
    parameters = f'seed={data["seed"]} noDays={data["noDays"]} noRuns={data["noRuns"]} noProb={data["noProbs"]}'
    x=10
    y=(x / 16)*10 
    plt.figure(figsize=(x,y))    
    plt.fill_between(data["noPeople"], data["ciLb"], data["ciUb"], color='b', alpha=.1, label=f"cl = {data['ciCl']}")
    plt.plot(data["noPeople"], data["x_hat"], label='Simulation Result', marker='o', color="orange", alpha=.5)
    plt.plot(data["noPeople"], data["pTheo"], linestyle="dotted", label="Theoretical formula", color="black") 
    plt.xlabel('n: Number of People' + "\n" + "Figure 1")
    plt.ylabel('Prob(Birthday Collision)')
    plt.legend()
    plt.grid()
    plt.title("Uniform Birthday Popularity " + "\n" + parameters)
    plt.savefig("UBP-" + parameters + ".png")
    plt.show()
    plt.clf()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=int, default=42, help='Initial Seed')
    parser.add_argument('-r', '--noRuns', type=int, default=1000, help='Number of runs')
    parser.add_argument("-p", "--noProb", type=int, default=5, help="Number of probabilities P(Collision) must be computed for any number of people")
    parser.add_argument("-n", "--noDays", type=int, default=365)
    parser.add_argument("-m", "--noPeople", type=int, default=81)
    parser.add_argument('-cl', '--confidenceLevel', type=int, default=0.95, help='Confidence Level')
    parser.add_argument("-d", type=int, default=1, choices=[1,2,3], help="The birthday popularity distribution")
    args = parser.parse_args()

    # initial settings
    seed = args.seed
    noRuns = args.noRuns
    noProbs = args.noProb
    noDays = args.noDays
    maxNoPeople = args.noPeople
    ciCl = args.confidenceLevel    
    d = args.d

    # This nameFile will be given to the file which stores the simulation results
    inputFileName = f"birthday_seed={seed}_cl={ciCl}_maxNoPeople={maxNoPeople}_noDays={noDays}_noRuns={noRuns}_noProb={noProbs}_d={d}.txt"

    data = json.load(open(inputFileName))

    plot_graph(data)


if __name__ == "__main__":
    main()
