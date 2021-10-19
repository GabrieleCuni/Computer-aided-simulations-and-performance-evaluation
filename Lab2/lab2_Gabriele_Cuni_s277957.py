from scipy.stats import t
import argparse
import numpy as np
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(description='Lab 2 - Simulator')
parser.add_argument("-s", "--seed", type=int, default=42, help="Initilizing seed - Default is 42")
parser.add_argument("-lb", "--intervalEvaluationLB", type=int, default=0, help="")
parser.add_argument("-lb", "--intervalEvaluationUB", type=int, default=1, help="")
parser.add_argument("-ns", "--noStudents", type=int, default=150, help="Number of samples - Default is 150")
parser.add_argument("-ne", "--noEvaluations", type=int, default=2, help='Number of evaluations receive for each delivery- Default is 2')
parser.add_argument("-nh", "--noHomeworks", type=int, default=4, help='Number of homeworks done during one accademic year- Default is 4')
parser.add_argument("-stds", "--stdStudent", type=float, default=3, help="Standard deviation of the student homework quality")
parser.add_argument("-stdv", "--stdEvaluation", type=float, default=3, help="Standard deviation of the student evaluation skill")
# parser.add_argument("-sc", "--stoppingCondition", type=int, default=1, choices=[1,2,3,4,5], help="Stop the simulation when the desired relative error is reached - Default is 1%")
args = parser.parse_args()

seed = args.seed
intervalEvaluationLB = args.intervalEvaluationLB
intervalEvaluationUB = args.intervalEvaluationUB
noStudents = args.noStudents
noEvaluations = args.noEvaluations
noHomeworks = args.noHomeworks
stdStudent = args.stdStudent
stdEvaluation = args.stdEvaluation

randomGenerator = np.random.default_rng(seed) 
x_prof = randomGenerator.uniform(0,1)
x_s = randomGenerator.uniform(0,1)
