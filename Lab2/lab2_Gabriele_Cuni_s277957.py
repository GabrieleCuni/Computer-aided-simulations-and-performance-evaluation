from scipy import stats
from scipy.stats import truncnorm
from scipy.stats import t
import argparse
import numpy as np
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


def run(noStudents, noEvaluators, noHomeworks, stdQuality, stdEvaluation):
    X = np.empty(shape=noStudents)
    for s in range(noStudents):
        X[s] = np.random.uniform(0,1)

    Q = np.empty(shape=(noStudents,noHomeworks))
    for s in range(noStudents):
        mean = X[s]
        a, b = (0 - mean) / stdQuality, (1 - mean) / stdQuality
        rv = truncnorm(a=a, b=b, loc=mean, scale=stdQuality)
        # m = rv.mean()
        # std = rv.std()
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
    Q_hat = E.mean(axis=2, dtype=np.float64) 

    # rel_err = np.abs(Q_hat - Q)/Q

    # if noHomeworks==13 or noHomeworks==12:
    #     # print(f"Q_hat ({Q_hat.shape}):\n{Q_hat}")
    #     # print(f"Q ({Q.shape}):\n{Q}")
    #     # print(f"Q_hat-Q ({(Q_hat-Q).shape}):\n{Q_hat-Q}")
    #     print(f"Q_hat-Q/Q ({((Q_hat-Q)/Q).shape}):\n{(Q_hat-Q)/Q}")
    #     # print(f"rel_err:\n{rel_err}")
    #     print("***********************************************")

    # avg_rel_grading_err = np.mean(rel_err, dtype=np.float64)
    # avg_rel_grading_err = rel_err.mean(axis=1).mean()
    hbh = np.mean(np.mean(np.abs(Q_hat-Q)/Q,axis=1),axis=0)
    # final_grade = np.mean(np.abs(np.mean(Q_hat,axis=1)-np.mean(Q,axis=1))*(1/np.mean(Q,axis=1)), axis=0)
    final_grade = np.mean(np.abs((Q_hat-Q).sum(axis=1))/Q.sum(axis=1) ,axis=0)
    return hbh, final_grade

def main():
    parser = argparse.ArgumentParser(description='Lab 2 - Simulator')
    parser.add_argument("-s", "--seed", type=int, default=42, help="Initilizing seed - Default is 42")
    parser.add_argument("-S", "--noStudents", type=int, default=20, help="Number of samples - Default is 150")
    parser.add_argument("-K", "--noEvaluators", type=int, default=3, help='Number of evaluations receive for each delivery- Default is 2')
    parser.add_argument("-H", "--noHomeworks", type=int, default=15, help='Number of homeworks done during one accademic year- Default is 4')
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
    # print(f"noEvaluators: {noEvaluators}")
    print(f"noHomeworks: {noHomeworks}")
    print(f"stdQuality: {stdQuality}")
    print(f"stdEvaluation: {stdEvaluation}")

     

    # ho bisogno di più run per ogni insieme di parametri
    experiment_results = {"LB1":[],"hbh":[],"UB1":[],"LB2":[],"finalGrade":[],"UB2":[],"re1":[],"acc1":[],"re2":[],"acc2":[]}
    experiment_list = range(2,19)
    print("Starting Experiments***********************************************")
    # An experiment is made by 5 runs with the same input parameter set
    for noEvaluators in experiment_list: # Experimets
        np.random.seed(seed)
        print(f"noEvaluators: {noEvaluators}")
        results1 = np.empty(shape=5)
        results2 = np.empty(shape=5)
        for i in range(5): # 5 runs for each experiment
            results1[i], results2[i] = run(noStudents, noEvaluators, noHomeworks, stdQuality, stdEvaluation)

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

    # prova a plottare acc vs noEvaluators magari migliora
    plt.figure(1)
    plt.plot(experiment_list, experiment_results["hbh"], marker="o", label="hbh")
    plt.plot(experiment_list, experiment_results["LB1"], marker="o", linestyle="dotted", label="LB1", alpha=0.6)
    plt.plot(experiment_list, experiment_results["UB1"], marker="o", linestyle="dotted", label="UB1", alpha=0.6)    
    plt.fill_between(experiment_list, experiment_results["LB1"], experiment_results["UB1"], color='b', alpha=0.1)
    plt.ylabel("Rel err")
    plt.xlabel("Number of evaluators")
    plt.legend()
    plt.grid()
    plt.title(f"hbh - S:{noStudents} H:{noHomeworks} stdQ:{stdQuality} stdE:{stdEvaluation}")
    plt.savefig(f"hbh - S:{noStudents} H:{noHomeworks} stdQ:{stdQuality} stdE:{stdEvaluation}.png")
    plt.show()

    plt.figure(2)
    plt.plot(experiment_list, experiment_results["finalGrade"], marker="o", label="finalGrade")
    plt.plot(experiment_list, experiment_results["LB2"], marker="o", linestyle="dotted", label="LB2", alpha=0.6)
    plt.plot(experiment_list, experiment_results["UB2"], marker="o", linestyle="dotted", label="UB2", alpha=0.6)
    plt.fill_between(experiment_list, experiment_results["LB2"], experiment_results["UB2"], color='b', alpha=0.1)
    plt.ylabel("Rel err")
    plt.xlabel("Number of evaluators")
    plt.legend()
    plt.grid()
    plt.title(f"Final grade - S:{noStudents} H:{noHomeworks} stdQ:{stdQuality} stdE:{stdEvaluation}")
    plt.savefig(f"Final grade - S:{noStudents} H:{noHomeworks} stdQ:{stdQuality} stdE:{stdEvaluation}.png")
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