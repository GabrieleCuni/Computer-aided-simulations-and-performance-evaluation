from scipy.stats import truncnorm
from scipy.stats import t
import argparse
import numpy as np
import json
from matplotlib import pyplot as plt

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


def run(noStudents, noEvaluators, noHomeworks, stdQuality, stdEvaluation, uni):
    X = np.empty(shape=noStudents, dtype=np.float64)
    for s in range(noStudents):
        X[s] = np.random.uniform(0,1)

    Q = np.empty(shape=(noStudents,noHomeworks), dtype=np.float64)
    for s in range(noStudents):
        mean = X[s]
        std = min((1-mean)/3,stdQuality,mean/3)
        a, b = (0 - mean) / std, (1 - mean) / std
        rv = truncnorm(a=a, b=b, loc=mean, scale=std)
        for h in range(noHomeworks):
            if uni is False:
                Q[s][h] = rv.rvs(size=1)
            else:
                delta = min(mean,0.1,1-mean)
                a = mean - delta
                b = mean + delta
                Q[s][h] = np.random.uniform(a,b)

    E = np.empty(shape=(noStudents,noHomeworks, noEvaluators), dtype=np.float64)
    for s in range(noStudents):
        for h in range(noHomeworks):
            mean = Q[s][h]
            std = min((1-mean)/3,stdEvaluation,mean/3)
            a, b = (0 - mean) / std, (1 - mean) / std
            rv = truncnorm(a=a, b=b, loc=mean, scale=std)
            for k in range(noEvaluators):
                if uni is False:
                    E[s][h][k] = rv.rvs(size=1)
                else:
                    delta = min(mean,0.1,1-mean)
                    a = mean - delta
                    b = mean + delta
                    E[s][h][k] = np.random.uniform(a,b)
                
    Q_hat = E.mean(axis=2, dtype=np.float64) 
    hbh = np.mean(np.mean(np.abs(Q_hat-Q)/Q,axis=1),axis=0)
    final_grade = np.mean(np.abs((Q_hat-Q).sum(axis=1))/Q.sum(axis=1) ,axis=0)
    return hbh, final_grade

def main():
    parser = argparse.ArgumentParser(description='Lab 2 - Simulator')
    parser.add_argument("-s", "--seed", type=int, default=421, help="Initilizing seed - Default is 42")
    parser.add_argument("-S", "--noStudents", type=int, default=25, help="Number of samples - Default is 150")
    parser.add_argument("-H", "--noHomeworks", type=int, default=5, help='Number of homeworks done during one accademic year- Default is 4')
    parser.add_argument("-stdq", "--stdQuality", type=float, default=0.1, help="Standard deviation of the student homework quality")
    parser.add_argument("-stde", "--stdEvaluation", type=float, default=0.1, help="Standard deviation of the student evaluation skill")
    parser.add_argument("-U", "--uniform", action="store_true", help="Use this parameter if you want to use the uniform distribution for the quality of the homework and evaluation")
    parser.add_argument("-o", "--outputFileName", type=str, default="data", help="Output File Name that stores all the simulation parameters and results")
    args = parser.parse_args()

    seed = args.seed
    noStudents = args.noStudents
    noHomeworks = args.noHomeworks
    stdQuality = args.stdQuality
    stdEvaluation = args.stdEvaluation
    fileName = args.outputFileName    

    print(f"seed: {seed}")
    print(f"noStudents: {noStudents}")
    print(f"noHomeworks: {noHomeworks}")
    print(f"stdQuality: {stdQuality}")
    print(f"stdEvaluation: {stdEvaluation}")

    minK = 2 # Inclusive
    maxK = 25 # Exclusive
    experiment_list = range(minK,maxK)
    experiment_results = {"n":list(experiment_list),"uni":args.uniform,"S":noStudents,"H":noHomeworks,"minK":minK,"maxK":maxK,"stdQ":stdQuality,"stdE":stdEvaluation,"LB1":[],"hbh":[],"UB1":[],"LB2":[],"finalGrade":[],"UB2":[],"re1":[],"acc1":[],"re2":[],"acc2":[]}    
    print("***********************************************")
    print("Simulation:")
    # An experiment is made by 5 runs with the same input parameter set
    for noEvaluators in experiment_list: # Experimets
        np.random.seed(seed)
        print(f"noEvaluators: {noEvaluators}")
        results1 = np.empty(shape=5, dtype=np.float64)
        results2 = np.empty(shape=5, dtype=np.float64)
        for i in range(5): # 5 runs for each experiment
            results1[i], results2[i] = run(noStudents, noEvaluators, noHomeworks, stdQuality, stdEvaluation, args.uniform)

        x_hat, s, lowerBound, upperBound, rel_err, accuracy = confidenceInterval(results1)
        experiment_results["hbh"].append(x_hat)
        experiment_results["LB1"].append(lowerBound)
        experiment_results["UB1"].append(upperBound)
        experiment_results["re1"].append(rel_err)
        experiment_results["acc1"].append(accuracy)

        x_hat, s, lowerBound, upperBound, rel_err, accuracy = confidenceInterval(results2)
        experiment_results["finalGrade"].append(x_hat)
        experiment_results["LB2"].append(lowerBound)
        experiment_results["UB2"].append(upperBound)
        experiment_results["re2"].append(rel_err)
        experiment_results["acc2"].append(accuracy)

    if args.uniform is False:
        json.dump(experiment_results, open("truncatedNormal" + fileName + ".txt","w"))
    else:
        json.dump(experiment_results, open("uniform" + fileName + ".txt","w"))

if __name__ == "__main__":
    main()