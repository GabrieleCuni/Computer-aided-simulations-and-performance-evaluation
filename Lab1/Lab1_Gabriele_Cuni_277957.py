from scipy.stats import t
import argparse
import numpy as np
from matplotlib import pyplot as plt

# function to compute confidence intervals
def confidenceInterval(x):
    t_sh = t.ppf((cl + 1) / 2, df=len(x) - 1)  # threshold for t_student
    x_hat = x.mean()  
    s = x.std(ddof=1)  # Squared root of the estimated variance. If ddof=0 Biased estimator, if ddof=1 Unbiased estimator 
    delta = t_sh * s / np.sqrt(len(x))  # confidence interval half width
    rel_err = delta / x_hat 
    accuracy = 1 - rel_err
    lowerBound = x_hat - delta
    upperBound = x_hat + delta
    return x_hat, s, lowerBound, upperBound, rel_err, accuracy

def runExperiment(n, randomGenerator):
    x = np.full(shape=n, fill_value=0, dtype=float)
    for i in range(n):
        d = np.full(shape=noSamples, fill_value=0, dtype=float)
        for j in range(noSamples):
            d[j] = randomGenerator.uniform(0,10)
        x[i] =  d.mean() 
    return confidenceInterval(x)

# INPUT
parser = argparse.ArgumentParser(description='Simulator')
parser.add_argument("-s", "--seed", type=int, default=42, help="Initilizing seed - Default is 42")
parser.add_argument("-ns", "--noSamples", type=int, default=50, help="Number of samples - Default is 50")
parser.add_argument("-cl", "--confidenceLevel", type=float, default=0.95, help='Confidence level - Default is 0.95')
parser.add_argument("-sc", "--stoppingCondition", type=int, default=1, choices=[1,2,3,4,5], help="Stop the simulation when the desired relative error is reached - Default is 1%")
args = parser.parse_args()

seed = args.seed
noSamples = args.noSamples
cl = args.confidenceLevel
stop = args.stoppingCondition

# https://towardsdatascience.com/stop-using-numpy-random-seed-581a9972805f
# https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.uniform.html
randomGenerator = np.random.default_rng(seed) 

# PRINT INPUT PARAMETERS
print("*** INITIAL SETTINGS***")
print(f"Initial seed: {seed}")
print(f"Number of samples: {noSamples}") # potrebbe essere che questo viene gestito dal simulatore 0 100 1000 10000 ecc ecc
print(f"Confidence level: {cl}")
print(f"Stopping condition: Relative error < {stop}%")
print("*** END INITIAL SETTINGS ***")

stopFlag = False

simulationLog = {"noRuns":[],"x_hat":[], "s":[], "lowerBound":[], "upperBound":[],"rel_err":[],"accuracy":[]}
for noRuns in range(5,1000,5): # from 5 to 100 with step 5
    print(f"Running the experiment number: {noRuns}") 
    x_hat, s, lowerBound, upperBound, rel_err, accuracy = runExperiment(noRuns, randomGenerator)
    simulationLog["noRuns"].append(noRuns)
    simulationLog["x_hat"].append(x_hat)
    simulationLog["s"].append(s)
    simulationLog["lowerBound"].append(lowerBound)
    simulationLog["upperBound"].append(upperBound)
    simulationLog["rel_err"].append(rel_err*100)
    simulationLog["accuracy"].append(accuracy*100)
    if (rel_err*100) <= stop:
        print(f"Simulation is ended because the stopping condition is achieved. noRun:{noRuns}, RelErr:{int(round(rel_err,2)*100)}, Acc:{int(round(accuracy,2)*100)}%")
        stopFlag = True
        break

if not stopFlag:
    print("Simulation is ended, but the stopping condition is not achieved")

plt.subplot()
plt.plot(simulationLog["noRuns"], simulationLog["accuracy"], label="Accuracy", marker="o")
plt.xlabel("Number of runs")
plt.ylabel("Accuracy [%]")
plt.title(f"CL={int(cl*100)}% - Max Accuracy={int(round(accuracy,2)*100)}% - Min Relative error={int(round(rel_err,2)*100)}%")
plt.legend()
plt.grid()
plt.savefig(f"chart_Accuracy_CL={int(cl*100)}%_Acc={int(round(accuracy,2)*100)}%_RelErr={int(round(rel_err,2)*100)}%.png")
plt.show()

population_mean = np.full(shape=len(simulationLog["noRuns"]), fill_value=5, dtype=float)

plt.subplot()
plt.plot(simulationLog["noRuns"], simulationLog["lowerBound"], label="CI lower bound", linestyle="dotted", color="red")
plt.plot(simulationLog["noRuns"], simulationLog["x_hat"], label="Estimated average", marker="o")
plt.plot(simulationLog["noRuns"], simulationLog["upperBound"], label="CI upper bound", linestyle="dotted", color="green")
plt.plot(simulationLog["noRuns"], population_mean, label="Population mean", color="black")
plt.fill_between(simulationLog["noRuns"], simulationLog["lowerBound"], simulationLog["upperBound"], color='b', alpha=.1)
plt.xlabel("Number of runs")
plt.ylabel("Population mean and Estimated average")
plt.title(f"CL={int(cl*100)}% - Max Accuracy={int(round(accuracy,2)*100)}% - Min Relative error={int(round(rel_err,2)*100)}%")
plt.legend()
plt.grid()
plt.savefig(f"chart_ConfidenceInterval_CL={int(cl*100)}%_Acc={int(round(accuracy,2)*100)}%_RelErr={int(round(rel_err,2)*100)}%.png")
plt.show()






