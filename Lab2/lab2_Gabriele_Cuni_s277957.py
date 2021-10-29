from scipy import stats
from scipy.stats import truncnorm
import argparse
import numpy as np
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(description='Lab 2 - Simulator')
parser.add_argument("-s", "--seed", type=int, default=42, help="Initilizing seed - Default is 42")
parser.add_argument("-S", "--noStudents", type=int, default=150, help="Number of samples - Default is 150")
parser.add_argument("-K", "--noEvaluators", type=int, default=3, help='Number of evaluations receive for each delivery- Default is 2')
parser.add_argument("-H", "--noHomeworks", type=int, default=4, help='Number of homeworks done during one accademic year- Default is 4')
parser.add_argument("-stdq", "--stdQuality", type=float, default=0.1, help="Standard deviation of the student homework quality")
parser.add_argument("-stde", "--stdEvaluation", type=float, default=0.1, help="Standard deviation of the student evaluation skill")
# parser.add_argument("-sc", "--stoppingCondition", type=int, default=1, choices=[1,2,3,4,5], help="Stop the simulation when the desired relative error is reached - Default is 1%")
args = parser.parse_args()

seed = args.seed
intervalEvaluationLB = 0
intervalEvaluationUB = 1
noStudents = args.noStudents
noEvaluators = args.noEvaluators
noHomeworks = args.noHomeworks
stdQuality = args.stdQuality
stdEvaluation = args.stdEvaluation

np.random.seed(seed) 
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

X = []
for s in range(noStudents):
    X.append( np.random.uniform(0,1) )

Q = []
for s in range(noStudents):
    mean = X[s]
    a, b = (0 - mean) / stdQuality, (1 - mean) / stdQuality
    Q.append( truncnorm.rvs(a=a, b=b, loc=mean, scale=stdQuality, size=noHomeworks) )

E = []
for s in range(noStudents):
    E.append([])
    for h in range(noHomeworks):
        mean = Q[s][h]
        a, b = (0 - mean) / stdEvaluation, (1 - mean) / stdEvaluation
        E[s].append( truncnorm.rvs(a=a, b=b, loc=mean, scale=stdEvaluation, size=noEvaluators) )

Q_hat = np.empty(shape=(noStudents,noHomeworks), dtype=np.float64)
for s in range(noStudents):
    for h in range(noHomeworks):
        Q_hat[s][h] = E[s][h].mean() 

count = 0
for s in range(noStudents):
    for h in range(noHomeworks):
        count += abs(Q_hat[s][h] - Q[s][h]) / Q[s][h]
averageRelativeGradingError = count / (noHomeworks*noStudents)
print(averageRelativeGradingError)
