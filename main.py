import random
from typing import List
from agent import Agent
from information import Information
from position import Position
from grid import Grid

def main():

    g = Grid()
    print(g)


    #agent30 = g._findAgent(30)
    #print(g._agentsInRange(agent30)[0])
    ############## testing agentInRange when spread radius is 1
    print("### TESTING AGENT IN RANGE RANGE 1 ###")
    agent9 = g._agents[2]
    print(agent9)
    test = g.agentsInRange(agent9)
    for a in test:
        print(a)

    ############ testing agentInRange when spread radius is 2
    print("### TESTING AGENT IN RANGE RANGE 2 ###")
    test = g.agentsInRange(agent9)
    for a in test:
        print(a)

    print("### TESTING GET CELL###")
    test_position = Position(row = 2, col = 3)
    test_cell = g.getCell(test_position)
    print(test_cell)


main()
