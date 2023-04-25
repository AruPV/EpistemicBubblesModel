import random
from typing import List
from agent import Agent
from information import Information
from position import Position
from grid import Grid

def tests():
    

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
   
    '''
    print("###TESTING OUT GET MOVE CELL AND MOVEAGENT")

    print("Starting Cell:")
    print(test_cell)

    print("Agent to be moved:")
    moving_agent = test_cell.contents[0]
    print(moving_agent)

    print("Information Origin Position:")
    origin = Position(row = 4, col = 1)
    print(origin)

    print("Getting Target Position")
    target_cell = g._getMoveCell(moving_agent = moving_agent, origin = origin)
    print(target_cell)
py
    print("Attempting Move")
    g._moveAgent(moving_agent, origin)

    print("Starting Cell:")
    print(test_cell)

    print("Target Cell:")
    print(target_cell)
    

    print("###TESTING OUT _oneTurn")
    test_agent = g._agents[0]
    test_information = Information(test_position)
    g._oneTurn(test_agent, debugging = False)

    '''

    print("###Testing out _oneRound")
    print(g)
    print("###")
    g.runRounds(num_rounds = 3, debugging = False)
    print(g)
    return

def main():
    random.seed(42)
    g = Grid(rows= 100, cols = 100)
    '''
    g.toCSV(filename = "0_round.csv")
    g.run()
    g.toCSV(filename = "1_round.csv")
    g.run()
    g.toCSV(filename = "2_round.csv")
    g.run()
    g.toCSV(filename = "3_round.csv")
    g.run()
    g.toCSV(filename = "4_round.csv")
    g.run()
    g.toCSV(filename = "5_round.csv")
    g.run()
    g.toCSV(filename = "6_round.csv")
    g.run()
    g.toCSV(filename = "7_round.csv")
    g.run()
    g.toCSV(filename = "8_round.csv")
    g.run()
    g.toCSV(filename = "9_round.csv")
    g.run()
    g.toCSV(filename = "10_round.csv")
    '''
    g.run(num_rounds = 100)
    g.toCSV(filename = "100_round.csv")
    g.run(num_rounds = 900)
    g.toCSV(filename = "1000_round.csv")



main()
