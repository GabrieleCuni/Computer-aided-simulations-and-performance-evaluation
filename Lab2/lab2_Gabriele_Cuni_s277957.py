from scipy import stats
from scipy.stats import truncnorm
import argparse
import numpy as np
from matplotlib import pyplot as plt

def run_experiment(noStudents, noEvaluators, noHomeworks, stdQuality, stdEvaluation):
    X = np.empty(shape=noStudents)
    for s in range(noStudents):
        X[s] = np.random.uniform(0,1)

    Q = np.empty(shape=(noStudents,noHomeworks))
    for s in range(noStudents):
        mean = X[s]
        a, b = (0 - mean) / stdQuality, (1 - mean) / stdQuality
        rv = truncnorm(a=a, b=b, loc=mean, scale=stdQuality)
        for h in range(noHomeworks):
            Q[s][h] = rv.rvs(size=1)
            # Q[s][h] = truncnorm.rvs(a=a, b=b, loc=mean, scale=stdQuality, size=1) 

    # E = np.empty(shape=(noEvaluators,noStudents,noHomeworks))
    E = np.empty(shape=(noStudents,noHomeworks, noEvaluators))
    for s in range(noStudents):
        for h in range(noHomeworks):
            mean = Q[s][h]
            a, b = (0 - mean) / stdEvaluation, (1 - mean) / stdEvaluation
            rv = truncnorm(a=a, b=b, loc=mean, scale=stdEvaluation)
            for k in range(noEvaluators):
                E[s][h][k] = rv.rvs(size=1)
                # E[k][s][h] = truncnorm.rvs(a=a, b=b, loc=mean, scale=stdEvaluation, size=1)

    # Q_hat = E.mean(axis=0) 
    Q_hat = E.mean(axis=2) 

    rel_err = np.abs( (Q_hat - Q)/Q )

    # if noHomeworks==13 or noHomeworks==12:
    #     # print(f"Q_hat ({Q_hat.shape}):\n{Q_hat}")
    #     # print(f"Q ({Q.shape}):\n{Q}")
    #     # print(f"Q_hat-Q ({(Q_hat-Q).shape}):\n{Q_hat-Q}")
    #     print(f"Q_hat-Q/Q ({((Q_hat-Q)/Q).shape}):\n{(Q_hat-Q)/Q}")
    #     # print(f"rel_err:\n{rel_err}")
    #     print("***********************************************")

    avg_rel_grading_err = np.mean(rel_err)
    return avg_rel_grading_err

def main():
    parser = argparse.ArgumentParser(description='Lab 2 - Simulator')
    parser.add_argument("-s", "--seed", type=int, default=42, help="Initilizing seed - Default is 42")
    parser.add_argument("-S", "--noStudents", type=int, default=25, help="Number of samples - Default is 150")
    parser.add_argument("-K", "--noEvaluators", type=int, default=3, help='Number of evaluations receive for each delivery- Default is 2')
    parser.add_argument("-H", "--noHomeworks", type=int, default=4, help='Number of homeworks done during one accademic year- Default is 4')
    parser.add_argument("-stdq", "--stdQuality", type=float, default=0.1, help="Standard deviation of the student homework quality")
    parser.add_argument("-stde", "--stdEvaluation", type=float, default=0.1, help="Standard deviation of the student evaluation skill")
    # parser.add_argument("-sc", "--stoppingCondition", type=int, default=1, choices=[1,2,3,4,5], help="Stop the simulation when the desired relative error is reached - Default is 1%")
    args = parser.parse_args()

    seed = args.seed
    noStudents = args.noStudents
    noEvaluators = args.noEvaluators
    noHomeworks = args.noHomeworks
    stdQuality = args.stdQuality
    stdEvaluation = args.stdEvaluation

    print(f"seed: {seed}")
    print(f"noStudents: {noStudents}")
    print(f"noEvaluators: {noEvaluators}")
    # print(f"noHomeworks: {noHomeworks}")
    print(f"stdQuality: {stdQuality}")
    print(f"stdEvaluation: {stdEvaluation}")

    np.random.seed(seed) 

    experiment_results = []
    experiment_list = range(2,20)
    print("Starting Experiments***********************************************")
    for noHomeworks in experiment_list:
        print(f"noHomeworks: {noHomeworks}")
        result = run_experiment(noStudents, noEvaluators, noHomeworks, stdQuality, stdEvaluation)
        experiment_results.append(result)
        # if result<1:
        #     experiment_results.append( result )
        # else:
        #     experiment_results.append(1)

    plt.figure(1)
    plt.plot(experiment_list, experiment_results, marker="o")
    plt.ylabel("Rel err")
    plt.xlabel("Number of homeworks")
    plt.grid()
    plt.title(f"S:{noStudents} K:{noEvaluators} stdQ:{stdQuality} stdE:{stdEvaluation}")
    plt.savefig(f"S:{noStudents} K:{noEvaluators} stdQ:{stdQuality} stdE:{stdEvaluation}.png")
    plt.show()

if __name__ == "__main__":
    main()





# loc is the mean; scale is the standard deviation

# Test the truncnorm
# n=100
# mean = 1
# stdQuality = 0.3
# a, b = (0 - mean) / stdQuality, (1 - mean) / stdQuality
# x = np.linspace(0,1, 100)
# r = truncnorm(a=a, b=b, loc=mean, scale=stdQuality)
# plt.plot(x, r.pdf(x))
# # plt.hist(r, density=True, histtype='stepfilled', alpha=0.2)
# plt.show()