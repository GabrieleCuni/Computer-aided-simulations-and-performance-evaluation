import argparse
import numpy as np
import random
import json
from scipy.stats import t

def confidenceInterval(x, cl=0.99):
    t_sh = t.ppf((cl + 1) / 2, df=len(x) - 1)  # threshold for t_student
    x_hat = x.mean()  
    s = x.std(ddof=1)  # Squared root of the estimated variance. If ddof=0 Biased estimator, if ddof=1 Unbiased estimator 
    delta = t_sh * s / np.sqrt(len(x))  # confidence interval half width
    rel_err = delta / x_hat 
    lowerBound = x_hat - delta
    upperBound = x_hat + delta
    return x_hat, lowerBound, upperBound, rel_err

def runSimulatorGeneralization(noPeople, noDays, ciCl, noRuns, noProb):  
    pArray = np.full(noProb, 0, dtype=np.float64) # It must be a float array in order to store a probability
    for p in range(noProb): # Repeat the experiment noProb times to be able to compute a confidence interval
        runResult = np.full(noRuns, 0)  
        for r in range(noRuns):  # Do noRuns runs to be able to compute the P(collision).
            days = np.full(noDays, 0) 
            for _ in range(noPeople):                  
                days[random.randint(0, noDays - 1)] += 1 # Draw from the uniform distribution a birthday and add it in the right day      
            if days.max() > 1:
                runResult[r] = 1 # At least one collision is happen in this run
            else:
                runResult[r] = 0 # No collision in this run
        pArray[p] =  len(list(filter(lambda x: x==1, runResult ))) / len(runResult) # Compute the P(collision)
    x_hat, ciLb, ciUb, ciRe = confidenceInterval(pArray, ciCl)  # evaluate the confidence intervals    
    pTheo = 1 - np.exp( -( (noPeople**2)/(2*noDays) ) )  # theoretical formula
    # Clip UB and LB
    ciLb = max(0, ciLb)
    ciUb = min(1, ciUb)
    return pTheo, x_hat, ciLb, ciUb, ciRe


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=int, default=42, help='Initial Seed')
    parser.add_argument('-r', '--noRuns', type=int, default=500, help='Number of runs')
    parser.add_argument("-p", "--noProb", type=int, default=5, help="Number of probabilities P(Collision) must be computed for any number of people")
    parser.add_argument("-n", "--noDays", type=int, default=365)
    parser.add_argument("-m", "--noPeople", type=int, default=81)
    parser.add_argument('-cl', '--confidenceLevel', type=int, default=0.95, help='Confidence Level')
    args = parser.parse_args()

    # initial settings
    seed = args.seed
    noRuns = args.noRuns
    noProbs = args.noProb
    noDays = args.noDays
    maxNoPeople = args.noPeople
    ciCl = args.confidenceLevel    

    # This nameFile will be given to the file which stores the simulation results
    output_file_name = f"birthday_seed={seed}_cl={ciCl}_maxNoPeople={maxNoPeople}_noDays={noDays}_noRuns={noRuns}_noProb={noProbs}.txt"

    # create list of inputs which makes the x-axis of the charts
    noPeopleList = list(range(2,maxNoPeople,4))

    # print input parameters
    print("*** INITIAL SETTINGS ***")
    print("Seed:", seed)
    print("Number of runs:", noRuns)
    print("Number of probabilities p:", noProbs)
    print("Number of days n:", noDays)
    print("Max number of people:", maxNoPeople)    
    print("Confidence level:", ciCl)    
    print("*** END INITIAL SETTINGS ***")

    simulation_results = {
        "noPeople": noPeopleList,
        "noDays": noDays,
        "noRuns": noRuns,
        "noProbs": noProbs,
        "ciCl": ciCl,
        "seed": seed,
        "pTheo":[],
        "ciLb":[], 
        "x_hat":[], 
        "ciUb":[], 
        "ciRe":[]      
    }

    # For each number of People m I do an experiment which consists of multiples runs.
    for m in noPeopleList:  
        print("Running for noPeople=", m)  
        random.seed(a=seed)  # reset initial seed
        # Each time I call this function I do an experiment              
        pTheo, x_hat, ciLb, ciUb, ciRe = runSimulatorGeneralization(m, noDays, ciCl, noRuns, noProbs)  
        simulation_results["pTheo"].append(pTheo)
        simulation_results["ciUb"].append(ciUb)
        simulation_results["ciLb"].append(ciLb)
        simulation_results["x_hat"].append(x_hat)
        simulation_results["ciRe"].append(ciRe)

    print("Dumping to file")
    json.dump(simulation_results, open(output_file_name,"w"))
    print("Dumping executed")

if __name__ == "__main__":
    main()
