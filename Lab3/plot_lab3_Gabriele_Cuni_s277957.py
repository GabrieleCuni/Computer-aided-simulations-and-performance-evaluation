import argparse
import os
import json
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(description='Lab 2 - Simulator')
parser.add_argument("-o", "--inputFileName", type=str, default="data", help="Input File Name that stores all the simulation parameters and results")
parser.add_argument("-U", "--uniform", action="store_true", help="Use this parameter if you want to use the uniform distribution for the quality of the homework and evaluation")
args = parser.parse_args()

fileName = args.inputFileName

if args.uniform is False:
    experiment_results = json.load(open("truncatedNormal" + fileName + ".txt"))
else:
    experiment_results = json.load(open("uniform" + fileName + ".txt"))


experiment_list = experiment_results["n"]
noHomeworks = experiment_results["H"]
noStudents = experiment_results["S"]
minK = experiment_results["minK"]
maxK = experiment_results["maxK"]
stdQuality = experiment_results["stdQ"]
stdEvaluation = experiment_results["stdE"]
uniform = experiment_results["uni"]

if uniform is False:
    title = f"Homework-by-Homework - S:{noStudents} H:{noHomeworks} K:[{minK},{maxK-1}] stdQ:{stdQuality} stdE:{stdEvaluation}"
else:
    title = f"Homework-by-Homework - S:{noStudents} H:{noHomeworks} K:[{minK},{maxK-1}] - Uniform"

plt.figure(1)
plt.plot(experiment_list, experiment_results["hbh"], marker="o", label="Average Relative Grading Error")
plt.plot(experiment_list, experiment_results["LB1"], marker="o", linestyle="dotted", label="CI - LB", alpha=0.6)
plt.plot(experiment_list, experiment_results["UB1"], marker="o", linestyle="dotted", label="CI - UB", alpha=0.6)    
plt.fill_between(experiment_list, experiment_results["LB1"], experiment_results["UB1"], color='b', alpha=0.1)
plt.ylabel("Average Relative Grading Error")
plt.xlabel("K: Number of evaluation for each homework")
plt.legend()
plt.grid()
plt.title(title)
plt.savefig(title + ".png")
plt.show()

if uniform is False:
    title = f"Final Grade - S:{noStudents} H:{noHomeworks} K:[{minK},{maxK-1}] stdQ:{stdQuality} stdE:{stdEvaluation}"
else:
    title = f"Final Grade - S:{noStudents} H:{noHomeworks} K:[{minK},{maxK-1}] - Uniform"

plt.figure(2)
plt.plot(experiment_list, experiment_results["finalGrade"], marker="o", label="Average Relative Grading Error")
plt.plot(experiment_list, experiment_results["LB2"], marker="o", linestyle="dotted", label="CI - LB", alpha=0.6)
plt.plot(experiment_list, experiment_results["UB2"], marker="o", linestyle="dotted", label="CI - UB", alpha=0.6)
plt.fill_between(experiment_list, experiment_results["LB2"], experiment_results["UB2"], color='b', alpha=0.1)
plt.ylabel("Average Relative Grading Error")
plt.xlabel("K: Number of evaluation for each homework")
plt.legend()
plt.grid()
plt.title(title)
plt.savefig(title + ".png")
plt.show()

# if uniform is False:
#     title = f"Homework-by-Homework - CI RE - S:{noStudents} H:{noHomeworks} K:[{minK},{maxK-1}] stdQ:{stdQuality} stdE:{stdEvaluation}"
# else:
#     title = f"Homework-by-Homework - CI RE - S:{noStudents} H:{noHomeworks} K:[{minK},{maxK-1}] - Uniform"

# plt.figure(3)
# plt.plot(experiment_list, experiment_results["re1"], marker="o", linestyle="dotted")
# plt.ylabel("CI - Relative error")
# plt.xlabel("K: Number of evaluation for each homework")
# plt.grid()
# plt.title(title)
# plt.savefig(title + ".png")
# plt.show()

# if uniform is False:
#     title = f"Final Grade - CI RE - S:{noStudents} H:{noHomeworks} K:[{minK},{maxK-1}] stdQ:{stdQuality} stdE:{stdEvaluation}"
# else:
#     title = f"Final Grade - CI RE - S:{noStudents} H:{noHomeworks} K:[{minK},{maxK-1}] - Uniform"

# plt.figure(4)
# plt.plot(experiment_list, experiment_results["re2"], marker="o", linestyle="dotted")
# plt.ylabel("CI - Relative error")
# plt.xlabel("K: Number of evaluation for each homework")
# plt.grid()
# plt.title(title)
# plt.savefig(title + ".png")
# plt.show()

if uniform is False:
    title = f"Final Grade and HbH - S:{noStudents} H:{noHomeworks} K:[{minK},{maxK-1}] stdQ:{stdQuality} stdE:{stdEvaluation}"
else:
    title = f"Final Grade and HbH - S:{noStudents} H:{noHomeworks} K:[{minK},{maxK-1}] - Uniform"

plt.figure(5)
plt.plot(experiment_list, experiment_results["hbh"], marker="o", label="Homework-by-Homework")
plt.plot(experiment_list, experiment_results["LB1"], marker="o", linestyle="dotted", label="CI - LB", alpha=0.6)
plt.plot(experiment_list, experiment_results["UB1"], marker="o", linestyle="dotted", label="CI - UB", alpha=0.6)  
plt.plot(experiment_list, experiment_results["finalGrade"], marker="o", label="Final Grade")
plt.plot(experiment_list, experiment_results["LB2"], marker="o", linestyle="dotted", label="CI - LB", alpha=0.6)
plt.plot(experiment_list, experiment_results["UB2"], marker="o", linestyle="dotted", label="CI - UB", alpha=0.6)
plt.fill_between(experiment_list, experiment_results["LB2"], experiment_results["UB2"], color='b', alpha=0.1)  
plt.fill_between(experiment_list, experiment_results["LB1"], experiment_results["UB1"], color='r', alpha=0.1)
plt.ylabel("Average Relative Grading Error")
plt.xlabel("K: Number of evaluation for each homework")
plt.legend()
plt.grid()
plt.title(title)
plt.savefig(title + ".png")
plt.show()

file1 = "truncatedNormal" + fileName + ".txt"
file2 = "uniform" + fileName + ".txt"
file_list = os.listdir()
if file1 in file_list and file2 in file_list:
    title = f"TruncatedNormal and Uniform - HbH - S:{noStudents} H:{noHomeworks} K:[{minK},{maxK-1}]"

    experiment_results_TN = json.load(open("truncatedNormal" + fileName + ".txt"))


    experiment_list = experiment_results_TN["n"]
    noHomeworks = experiment_results_TN["H"]
    noStudents = experiment_results_TN["S"]
    minK = experiment_results_TN["minK"]
    maxK = experiment_results_TN["maxK"]
    stdQuality = experiment_results_TN["stdQ"]
    stdEvaluation = experiment_results_TN["stdE"]
    uniform = experiment_results_TN["uni"]

    # new
    plt.figure(6)
    plt.plot(experiment_list, experiment_results_TN["hbh"], marker="o", label="TruncatedNormal - hbh")
    plt.plot(experiment_list, experiment_results_TN["LB1"], marker="o", linestyle="dotted", label="CI - LB", alpha=0.6)
    plt.plot(experiment_list, experiment_results_TN["UB1"], marker="o", linestyle="dotted", label="CI - UB", alpha=0.6) 
    plt.fill_between(experiment_list, experiment_results_TN["LB1"], experiment_results_TN["UB1"], color='r', alpha=0.1)

    experiment_results_U = json.load(open("uniform" + fileName + ".txt"))
    experiment_list = experiment_results_U["n"]
    noHomeworks = experiment_results_U["H"]
    noStudents = experiment_results_U["S"]
    minK = experiment_results_U["minK"]
    maxK = experiment_results_U["maxK"]
    stdQuality = experiment_results_U["stdQ"]
    stdEvaluation = experiment_results_U["stdE"]
    uniform = experiment_results_U["uni"]

    plt.plot(experiment_list, experiment_results_U["hbh"], marker="o", label="Uniform - hbh")
    plt.plot(experiment_list, experiment_results_U["LB1"], marker="o", linestyle="dotted", label="CI - LB", alpha=0.6)
    plt.plot(experiment_list, experiment_results_U["UB1"], marker="o", linestyle="dotted", label="CI - UB", alpha=0.6) 
    plt.fill_between(experiment_list, experiment_results_U["LB1"], experiment_results_U["UB1"], color='r', alpha=0.1)

    plt.ylabel("Average Relative Grading Error")
    plt.xlabel("K: Number of evaluation for each homework")
    plt.legend()
    plt.grid()
    plt.title(title)
    plt.savefig(title + ".png")
    plt.show()