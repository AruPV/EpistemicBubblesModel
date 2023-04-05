import random
from typing import List
from agent import Agent
from information import Information
from position import Position
from grid import Grid

def main():
    random.seed(42)
    g = Grid()
    print(g)

    print("### TESTING ADD AGENT ###")
    ################# testing addAgent
    p = Position(1,1)
    g._addAgent(p)
    print(len(g._agents))
    print(g)

    #agent30 = g._findAgent(30)
    #print(g._agentsInRange(agent30)[0])
    ############## testing agentInRange when spread radius is 1
    print("### TESTING AGENT IN RANGE RANGE 1 ###")
    agent9 = g._findAgent(9)
    p2 = Position(1,3)
    g._addAgent(p2)
    #test = g._agentsInRange(agent9)
    #for a in test:
        #print(a)

    ############ testing agentInRange when spread radius is 2
    print("### TESTING AGENT IN RANGE RANGE 2 ###")
    test = g._agentsInRange(agent9)
    for a in test:
        print(a)



main()
