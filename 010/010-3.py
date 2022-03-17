from numpy import random
import math

table = {
    "state": [(1, False), (1, True), (2, False), (2, True), (3, False), (3, True)], 
    "stop": [1, 1, 2, 2, 3, 3], 
    "continue": [1, 1, 1, 1, -3, -3],
    "mulligan": [1, None, 1, None, 1, None]
} # initial table

state = {"initial": (0, None), "current": (0, None), "next": (0, None), "result": (0,  None)} # default boi

def expected_value(state, action):
    max_value = max(table["state"])[0]
    if state[0] > max_value:
        return -3
    return table[action][table["state"].index(state)]

alpha = 0.01

random_numbers = [1, 3, 1, 1, 3]

random_index = 0

mulligan_index = 0

action = None

mulligan = False

game = 1

while (game < 10000): # game

    if (game % 1000 == 0):

        alpha /= 2

    if (not mulligan):
        print("\nGame:", game)

        state = {"initial": (0, None), "current": (0, None), "next": (0, None), "result": (0,  None), "update": (0, None)} # default boi

        state["initial"] = (random.randint(1, 3), mulligan)

        print("\nWe got a random # of", state["initial"], "so our inital state is", state["initial"])

        if (state["initial"][0] < 3):

            action = random.choice(["continue", "mulligan"], [0.5, 0.5])
        
            if (action == "mulligan"):

                print("\n\tMulligan mood")

                state["update"] = state["initial"]

                mulligan = True

                continue

            state["current"] = state["initial"]

            #state["initial"] = (0, None)#?
        
        else:

            action = "stop"

    else:

        state["next"] = (random.randint(1, 3), mulligan)

        print("\nWe got a random # of", state["next"], "so our inital state is", state["next"])
        

        if (state["next"][0] < 3):

            action = "continue"

        else:
            
            action = "stop"
        

    while (action == "continue"): # round

        change = random.randint(1, 3)

        state["next"] = (state["current"][0] + change, mulligan)

        state["update"] = state["current"]

        print("\tcontinue -> random # =", change, "so state =", state["next"])

        
        max_table = max(table["state"])[0]

        if (state["next"][0] > max_table):

            a_max = -3
        
        else:

            a_max = max(expected_value(state["next"], "stop"), expected_value(state["next"], "continue"), expected_value(state["next"], "mulligan"))

        print("\tresult =", a_max)

        update = alpha * (a_max - expected_value(state["update"], "continue"))

        table["continue"][table["state"].index(state["update"])] += update
        
        print("\tupdate = ", update)

        state["current"] = state["next"]

        state["next"] = (0, None)

        if (not mulligan):

            action = ["mulligan", "continue", "mulligan"][mulligan_index] #random.choice(["continue", "mulligan"], [0.5, 0.5])

            mulligan_index += 1
        
            if (action == "mulligan"):

                print("\n\tMulligan mood")

                state["update"] = state["current"]

                state["current"] = state["initial"]

                state["initial"] = (0, None)#?

                mulligan = True

                continue

        if (state["current"][0] >= max_table):
            
            break

    if (action == "stop"):

        state["result"] = state["current"]
        
        if (mulligan):
            
            state["result"] = state["next"]

            print("\tstop -> state =", state["result"])

            max_table = max(table["state"])[0]

            if (state["next"][0] > max_table):

                a_max = -3
            
            else:

                a_max = max(expected_value(state["next"], "stop"), expected_value(state["next"], "continue"))

            #print("\tresult =", a_max)

            expected_value_temp = expected_value(state["update"], "mulligan") #initial

            update = alpha * (a_max - expected_value_temp)

            table["mulligan"][table["state"].index(state["update"])] += update
            
            print("\tupdate = ", update)

        mulligan = False
        
        if (state["result"][0] > max(table["state"])[0]):

            a_max = -3
        
        else:

            a_max = expected_value(state["result"], "stop")

        print("\tresult =", a_max)

        game += 1

        continue

print("\n", table)