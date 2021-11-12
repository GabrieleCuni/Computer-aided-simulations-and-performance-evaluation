import argparse
import numpy as np
from matplotlib import pyplot as plt
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

def run(noAtt, noDef):
    while(1):
        # print("New noDef", noDef)
        # print("New noAtt", noAtt)
        if noAtt >= 4:    
            x_a = np.random.randint(1,7,size=3)
        elif noAtt==3:
            x_a = np.random.randint(1,7,size=2)
        elif noAtt==2:
            x_a = np.random.randint(1,7,size=1)
        else:
            return 0 # Defender win
            

        if noDef >= 3:
            x_d = np.random.randint(1,7,size=3)
        elif noDef == 2:
            x_d = np.random.randint(1,7,size=2)
        elif noDef == 1:
            x_d = np.random.randint(1,7,size=1)
        else:
            return 1 # Attacher win

        x_a = -np.sort(-x_a)
        x_d = -np.sort(-x_d)

        if len(x_a) < len(x_d):
            x_d = x_d[0:len(x_a)]
        if len(x_d) < len(x_a):
            x_a = x_a[0:len(x_d)]

        a = x_a > x_d
        b = list(filter(lambda x: x==True,a))

        # print("Defender lose",len(b))
        # print("Attecher lose:",len(x_a)-len(b))

        noDef = noDef - len(b)
        noAtt = noAtt - (len(x_a)-len(b))

        # print("New noDef", noDef)
        # print("New noAtt", noAtt)
        # print("------------------------------------------")

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--noDef', type=int, default=2502, help='Initial Seed')
args = parser.parse_args()
noRuns = 1000
noDef = args.noDef
maxNoAtt = 30


simulation_result = []
for noAtt in range(1,maxNoAtt+1):
    np.random.seed(421)
    experiments_result = np.empty(shape=noRuns, dtype=np.int)
    for i in range(noRuns):
        experiments_result[i] = run(noAtt+1, noDef)
    # print("experiments_result",experiments_result)
    # print("no Att win",len(list(filter(lambda x: x==1,experiments_result))))
    # print("noExperimets",len(experiments_result))
    prob_attacher_win = len(list(filter(lambda x: x==1,experiments_result))) / len(experiments_result)
    simulation_result.append(prob_attacher_win)
    # print("prob_attacher_win",prob_attacher_win)

plt.figure(1,(10,5))
plt.plot(list(range(1,maxNoAtt+1)),simulation_result, marker="o")
plt.hlines(0.95,2,30, color="green", label="95%")
plt.hlines(0.9,2,30, color="yellow", label="90%")
plt.hlines(0.8,2,30, color="red", label="80%")
plt.hlines(0.5,2,30, color="black", label="50%")
plt.grid()
plt.legend()
plt.xticks(list(range(1,maxNoAtt+1)))
plt.yticks(list(np.arange(0,1,0.1)))
plt.ylabel("Probability Attacher wins")
plt.xlabel("Number of Attacher Tanks")
plt.title(f"Number of defender tanks = {noDef}")
plt.savefig(f"Number of defender tanks = {noDef}.png")
plt.show()


