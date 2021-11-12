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
    accuracy = 1 - rel_err
    lowerBound = x_hat - delta
    upperBound = x_hat + delta
    return x_hat, s, lowerBound, upperBound, rel_err, accuracy


# def run_simulator(n, initial_seed, confidence_level, runs, d):  # run the bins-and-ball model for n bins and for multiple runs
#     random.seed(a=initial_seed)  # reset initial seed
#     maxvec = np.full(runs, 0)  # init vector for the maximum for each run
#     for r in range(runs):  # for each run
#         bins = np.full(n, 0)  # bins[i] is the occupancy of bin i; start from empty bins
#         for i in range(n):  # for each ball
#             if d == 1:
#                 bins[random.randint(0, n - 1)] += 1  # drop ball randomly and update bins
#             else:
#                 occupancy = np.full(d, 0)
#                 bin_indexes = np.full(d, 0)
#                 for i in range(d):
#                     bin_indexes[i] = random.randint(0, n - 1) # Uniformly extract d candidated indexes
#                     occupancy[i] = bins[bin_indexes[i]] # Save the corresponding actual occupancy
#                 bin_index = bin_indexes[ occupancy.argmin() ] # Select the bin within the lower occupancy
#                 bins[bin_index] += 1
#         maxvec[r] = bins.max()  # compute the max occupancy
#     x_hat, _, CI_LB, CI_UB, rel_err, accuracy = confidenceInterval(maxvec, confidence_level)  # evaluate the confidence intervals
#     if d==1:
#         theo = np.log(n) / np.log(np.log(n))  # theoretical formula
#         return theo, 3 * theo, CI_LB, x_hat, CI_UB, rel_err, accuracy
#     else:
#         theo = np.log(np.log(n)) / np.log(d)
#         theo_UB = 3 * np.log(n) / np.log(np.log(n))
#         return theo, theo_UB, CI_LB, x_hat, CI_UB, rel_err, accuracy

def runSimulatorGeneralization(noBins, noBalls, seed, cl, runs, d, alpha):  # run the bins-and-ball model for n bins and for multiple runs
    random.seed(a=seed)  # reset initial seed
    maxvec = np.full(runs, 0)  # init vector for the maximum for each run
    for r in range(runs):  # for each run
        bins = np.full(noBins, 0)  # bins[i] is the occupancy of bin i; start from empty bins
        for i in range(noBalls):  # for each ball
            if d == 1:
                bins[random.randint(0, noBins - 1)] += 1  # drop ball randomly and update bins
            else:
                occupancy = np.full(d, 0)
                bin_indexes = np.full(d, 0)
                for i in range(d):
                    bin_indexes[i] = random.randint(0, noBins - 1) # Uniformly extract d candidated indexes
                    occupancy[i] = bins[bin_indexes[i]] # Save the corresponding actual occupancy
                bin_index = bin_indexes[ occupancy.argmin() ] # Select the bin within the lower occupancy
                bins[bin_index] += 1
        maxvec[r] = bins.max()  # compute the max occupancy
    x_hat, _, CI_LB, CI_UB, rel_err, accuracy = confidenceInterval(maxvec, cl)  # evaluate the confidence intervals
    if d==1:
        theo = np.log(noBins) / np.log(np.log(noBins))  # theoretical formula
        return alpha * theo, 3 * alpha * theo, CI_LB, x_hat, CI_UB, rel_err, accuracy
    else:
        # TODO
        theo = np.log(np.log(noBins)) / np.log(d)
        theo_UB = 3 * (np.log(noBins) / np.log(np.log(noBins)))
        return alpha * theo, alpha * theo_UB, CI_LB, x_hat, CI_UB, rel_err, accuracy

def genInputList():
    input_list = []
    for i in (2, 3, 4, 5):
        a = [x*10**i for x in (1, 2, 4, 8)]
        input_list.extend(a)
    input_list.append(1000000)

    return input_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=int, default=42, help='Initial Seed')
    parser.add_argument('-cl', '--confidenceLevel', type=int, default=0.95, help='Confidence Level')
    parser.add_argument('-r', '--noRuns', type=int, default=5, help='Number of runs')
    parser.add_argument("-d", type=int, default=1, help="Number of balancing bins")
    parser.add_argument("-a", "--alpha", type=float, default=1)
    args = parser.parse_args()

    # initial settings
    seed = args.seed
    confidence_level = args.confidenceLevel
    noRuns = args.noRuns
    d = args.d
    alpha = args.alpha
    output_file_name = f"binsballs_seed={seed}_runs={noRuns}_d={d}_cl={confidence_level}_alpha={alpha}.txt"

    # create list of inputs
    input_list = genInputList()

    # print input parameters
    print("*** INITIAL SETTINGS ***")
    print("Bins/Balls number for the simulation:")
    print("n:", input_list)
    print("Seed:", seed)
    print("Confidence level:", confidence_level)
    print("Number of runs:", noRuns)
    print("d:", d)
    print("Alpha:", alpha)
    print("*** END INITIAL SETTINGS ***")

    experiment_results = {
        "n": input_list,
        "noRuns": noRuns,
        "cl": confidence_level,
        "seed": seed,
        "d": d,
        "alpha": alpha,
        "theo":[],
        "tub":[], 
        "CI_LB":[], 
        "x_hat":[], 
        "CI_UB":[], 
        "re":[],
        "acc":[]        
    }
    for n in input_list:  # for each number of bins and balls
        noBalls = int(alpha*n) # By default alpha = 1, therefore noBalls = noBins
        print("Running for n=", n, "noBalls=", noBalls)  # log starting a run
        # get the output results of a run               
        theo, theo_UB, CI_LB, x_hat, CI_UB, rel_err, accuracy = runSimulatorGeneralization(n, noBalls, seed, confidence_level, noRuns, d, alpha)  
        experiment_results["theo"].append(theo)
        experiment_results["tub"].append(theo_UB)
        experiment_results["CI_LB"].append(CI_LB)
        experiment_results["CI_UB"].append(CI_UB)
        experiment_results["x_hat"].append(x_hat)
        experiment_results["re"].append(rel_err)
        experiment_results["acc"].append(accuracy)

    print("Dumping to file")
    json.dump(experiment_results, open(output_file_name,"w"))
    print("Dumping executed")

if __name__ == "__main__":
    main()
