


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
    def __init__(self,Narr,Ndep,NAveraegUser,OldTimeEvent,AverageDelay):
        self.arr = Narr
        self.dep = Ndep
        self.ut = NAveraegUser
        self.oldT = OldTimeEvent
        self.delay = AverageDelay
        
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
def arrival(time, FES, queue, arrivalTime, b):
    global users
            
    # cumulate statistics
    data.arr += 1
    data.ut += users*(time-data.oldT)
    data.oldT = time
    

    # sample the time until the next arrival
    inter_arrival = random.expovariate(lambd=1.0/arrivalTime) # return float number
    
    # schedule the next arrival
    FES.put((time + inter_arrival, "arrival"))

    if users < b:
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

def simulation(arrivalTime, b):
    global time
    # Simulate until the simulated time reaches a constant
    while time < SIM_TIME:
        # Extract next event from the FES
        (time, event_type) = FES.get()
        # Call the event functions based on the event type 
        if event_type == "arrival":
            arrival(time, FES, queue, arrivalTime, b)

        elif event_type == "departure":
            departure(time, FES, queue)

seed = 42
threshold = 25
random.seed(seed)

plt.figure()
for b in [1,5,10]:
    res = {
        "load":[],
        "simAvgDelay":[]
    } 
    print("*******************************************************")
    print(f"b: {b}")
    for i in range(0,20):
        users=0 
        time = 0
        queue=[]
        data = Measure(0,0,0,0,0)
        FES = PriorityQueue()
        FES.put((0, "arrival"))
        load = 0.5 + i * ((0.95-0.5)/20)
        res["load"].append(load)
        arrivalTime = SERVICE / load

        simulation(arrivalTime, b)

        simAvgDelay = data.delay / data.dep

        res["simAvgDelay"].append(simAvgDelay) 
        
        print(f"\tLoad: {round(load,2)}, simAvgDelay: {round(simAvgDelay,2)}")

    plt.plot(res["load"], res["simAvgDelay"], marker="o", label=f"B={b}")
plt.xlabel("Load")
plt.ylabel("Average Delay")
plt.title(f"seed: {seed}, Max simulation time: {SIM_TIME}")
plt.legend()
plt.grid()
plt.savefig("DelayVsLoad_finiteCapacity.png")
plt.show()


    