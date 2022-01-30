


# ******************************************************************************
#
# This is a discrete-event simulator (event scheduling approach) of a queue
# - single-server 
# - infinite capacity of the waiting line
# - exponential inter arrival times
# - exponential service times
#
# 
# ******************************************************************************
 


import random
import numpy as np
from queue import PriorityQueue
from matplotlib import pyplot as plt

# ******************************************************************************
# Constants
# ******************************************************************************

# LOAD=0.85  # load of the queue
SERVICE = 10.0 # av service time
# ARRIVAL   = SERVICE/LOAD # av. inter-arrival time
TYPE1 = 1 # At the beginning all clients are of the same type, TYPE1 

# If I reduce it, the simulated curve became more noisy
SIM_TIME = 500000 # condition to stop the simulation. 


# ******************************************************************************
# To take the measurements
#
# Collect
# - total number of arrivals, Narr
# - total number of departures, Ndep
# - integral of the number of client in time
# - store the time of the last event (for computing the integral)
# - total delay in the queue 
# ******************************************************************************
class Measure:
    def __init__(self,Narr,Ndep,NAveraegUser,OldTimeEvent,AverageDelay, idleTime):
        self.arr = Narr
        self.dep = Ndep
        self.ut = NAveraegUser
        self.oldT = OldTimeEvent
        self.delay = AverageDelay
        self.idleTime = idleTime
        self.delayBelowCount = 0
        self.delayCount = 0
        self.userFrequencySet = dict()
        
# ******************************************************************************
# Client
# 
# Identify the client with
# - type: for future use
# - time of arrival (for computing the delay, i.e., time in the queue)
# ******************************************************************************
class Client:
    def __init__(self,type,arrival_time):
        self.type = type
        self.arrival_time = arrival_time


# ******************************************************************************
# ARRIVAL: event function
# 
# Receive in input 
# - the FES (Feature Event Set), for possibly schedule new events
# - the queue of the clients
# ******************************************************************************
def arrival(time, FES, queue, arrivalTime):
    global users
            
    # cumulate statistics
    if users == 0:
            data.idleTime += time - data.oldT
    data.arr += 1
    data.ut += users*(time-data.oldT)
    data.oldT = time
    

    # sample the time until the next arrival
    inter_arrival = random.expovariate(lambd=1.0/arrivalTime) # return float number
    
    # schedule the next arrival
    FES.put((time + inter_arrival, "arrival"))

    # update the state variable, by increasing the no. of clients by 1
    users += 1
    
    # create a record for the client
    client = Client(TYPE1,time)

    # insert the record in the queue
    queue.append(client)

    # if the server is idle start the service
    if users==1:
        # sample the service time
        service_time = random.expovariate(1.0/SERVICE)
        # schedule the departure of the client
        FES.put((time + service_time, "departure"))

    if users not in data.userFrequencySet.keys():
        data.userFrequencySet[users] = 1
    else:
        data.userFrequencySet[users] += 1


# ******************************************************************************
def departure(time, FES, queue):
    global users

    # get the first element from the queue
    client = queue.pop(0)
        
    # cumulate statistics
    data.dep += 1
    data.ut += users*(time-data.oldT)
    data.oldT = time
    data.delay += (time-client.arrival_time)
    if (time-client.arrival_time) < threshold:
        data.delayBelowCount += 1
    data.delayCount += 1


    # update the state variable, by decreasing the no. of clients by 1
    users -= 1
    
    # check whether there are more clients to in the queue
    if users >0:
        # sample the service time
        service_time = random.expovariate(1.0/SERVICE)
        # schedule the departure of the client
        FES.put((time + service_time, "departure"))


        
# ******************************************************************************
# Event-loop 
# ******************************************************************************
#

def simulation(arrivalTime):
    global time
    # Simulate until the simulated time reaches a constant
    while time < SIM_TIME:
        # Extract next event from the FES
        (time, event_type) = FES.get()
        # Call the event functions based on the event type 
        if event_type == "arrival":
            arrival(time, FES, queue, arrivalTime)

        elif event_type == "departure":
            departure(time, FES, queue)

def plotUserDistribution(userDistribution, load):
    plt.figure()
    plt.bar(userDistribution.keys(), userDistribution.values())
    plt.xlabel("Number of users")
    plt.ylabel("Probability")
    plt.title(f"Distribution of the number of users with load: {round(load,2)}")
    plt.savefig(f"userDist_load={round(load,2)}.png")
    plt.close()
    

seed = 42
threshold = 25
random.seed(seed)

res = {
    "load":[],
    "simAvgDelay":[],
    "theoAvgDelay":[],
    "pServerIdle":[],
    "pServerIdleTheo":[],
    "pDelayBelow":[]
} 

for i in range(0,20):
    users=0 
    time = 0
    queue=[]
    data = Measure(0,0,0,0,0,0)
    FES = PriorityQueue()
    FES.put((0, "arrival"))
    load = 0.5 + i * ((0.95-0.5)/20)
    res["load"].append(load)
    arrivalTime = SERVICE / load

    simulation(arrivalTime)

    simAvgDelay = data.delay / data.dep
    theoAvgDelay = (1/(1.0/SERVICE-1.0/arrivalTime))
    pServerIdle = data.idleTime / SIM_TIME
    pServerIdleTheo = 1.0 - load
    pDelayBelow = data.delayBelowCount / data.delayCount # Probability that the delay is below a given value

    total = 0
    userDistribution = dict()
    for key in data.userFrequencySet.keys():
        total += data.userFrequencySet[key]
    for key in data.userFrequencySet.keys():
        userDistribution[key] = data.userFrequencySet[key] / total

    plotUserDistribution(userDistribution, load)

    res["simAvgDelay"].append(simAvgDelay)
    res["theoAvgDelay"].append(theoAvgDelay)
    res["pServerIdle"].append(pServerIdle)
    res["pServerIdleTheo"].append(pServerIdleTheo)
    res["pDelayBelow"].append(pDelayBelow)

    

    print("*******************************************************")
    print(f"\tLoad: {round(load,2)}")
    print(f"\tsimAvgDelay: {round(simAvgDelay,2)}")
    print(f"\ttheoAvgDelay: {round(theoAvgDelay,2)}")
    print(f"\tpServerIdle: {round(pServerIdle,2)}")
    print(f"\tpServerIdleTheo: {round(pServerIdleTheo,2)}")
    print(f"\tpDelayBelow: {round(pDelayBelow,2)}")
    # print(f"\tusers distrib: {userDistribution}")

#*******************************************************
# PLOT
#********************************************************

plt.figure()
plt.plot(res["load"], res["simAvgDelay"], marker="o", label="Simulation")
plt.plot(res["load"], res["theoAvgDelay"], linestyle="--", label="Theory")
plt.xlabel("Load")
plt.ylabel("Average Delay")
plt.title(f"seed: {seed}, Max simulation time: {SIM_TIME}")
plt.legend()
plt.grid()
plt.savefig("DelayVsLoad.png")
plt.show()

plt.figure()
plt.plot(res["load"], res["pServerIdle"], marker="o", label="Simulation")
plt.plot(res["load"], res["pServerIdleTheo"], linestyle="--", label="Theory")
plt.xlabel("Load")
plt.ylabel("Probability that the server is idle")
plt.title(f"seed: {seed}, Max simulation time: {SIM_TIME}")
plt.legend()
plt.grid()
plt.savefig("idleVsLoad.png")
plt.show()



# ******************************************************************************
# Print outputs
# ******************************************************************************


# print("\n\n\n","*"*10,"  MEASUREMENTS  ","*"*10,"\n")
# print("No. of users in the queue at the end of the simulation:",users,\
#       "\nTot. no. of arrivals =",data.arr,"- Tot. no. of departures =",data.dep)
# print("Actual queue size: ",len(queue))
# if len(queue)>0:
#     print("Arrival time of the last element in the queue:",queue[len(queue)-1].arrival_time)

# print("\n\nLoad: ",LOAD)
# print("Nominal arrival rate: ",1.0/ARRIVAL)
# print("Measured arrival rate",data.arr/time,"\nMeasured departure rate: ",data.dep/time)
# theorical=(1.0/ARRIVAL)/(1.0/SERVICE-1.0/ARRIVAL)
# print("\n\nAverage number of users\nTheorical: ", theorical,\
#       "  -  Empirical: ",data.ut/time)

# theorical=1.0/(1.0/SERVICE-1.0/ARRIVAL)
# print("Average delay \nTheorical= ",theorical,"  -  Empirical: ",data.delay/data.dep)

# print("\n","*"*40)

# ******************************************************************************
# Initialization
# ******************************************************************************
#


# #arrivals=0
# # State variable: number of users
# users=0  
# # the simulation time 
# time = 0
# # Queue of the clients
# queue=[]  
# # Collect measurements
# data = Measure(0,0,0,0,0)
# # Future Event Set: the list of events in the form: (time, type)
# FES = PriorityQueue()
# # schedule the first arrival at t=0
# FES.put((0, "arrival"))
# # Initialize the random number generator    
# random.seed(42)
    