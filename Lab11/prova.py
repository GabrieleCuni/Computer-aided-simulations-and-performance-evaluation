import math
import sys
import numpy as np
from matplotlib import pyplot as plt

def optionalOne(m, experimetList):
    # exp = np.empty(shape=(len(experimetList),len(list(range(1,33)))), dtype=np.float64)
    # print(exp.shape)
    # sys.exit(1)
    exp = []
    kOptList = []
    pFPList = []
    for b in experimetList:
        n = 2**b
        kOpt = math.ceil( (n/m) * math.log(2))
        kOptList.append(  kOpt )
        pFPList.append( ( 1 - math.exp((-kOpt*m)/n) )**kOpt )
        tmp = []
        for k in range(1,33): # [1,33)
            pFP = ( 1 - math.exp((-k*m)/n) )**k
            tmp.append(pFP)
        exp.append(tmp)
    return exp, kOptList, pFPList

experimetList = [19, 20, 21, 22, 23]
exp, kOptList, pFPList = optionalOne(300000, experimetList)

plt.figure()
plt.plot(list(range(1,33)), exp[0], label="b = 19")
plt.plot(list(range(1,33)), exp[1], label="b = 20")
plt.plot(list(range(1,33)), exp[2], label="b = 21")
plt.plot(kOptList[0], pFPList[0], "ro", label="ciao")
plt.plot(kOptList[1], pFPList[1], "ro", label="ciao")
plt.plot(kOptList[2], pFPList[2], "ro", label="ciao")
plt.xlabel("k")
plt.ylabel("P(FP)")
plt.legend()
plt.show()

plt.figure()
plt.plot(list(range(1,33)), exp[3], label="b = 22")
plt.plot(list(range(1,33)), exp[4], label="b = 23")
plt.plot(kOptList[3], pFPList[3], "ro", label="ciao")
plt.plot(kOptList[4], pFPList[4], "ro", label="ciao")
plt.xlabel("k")
plt.ylabel("P(FP)")
plt.legend()
plt.show()