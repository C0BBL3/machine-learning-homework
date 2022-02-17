import random
import math

table = {"state": [1, 2, 3], "stop": [1, 2, 3], "continue": [2, 3, -3]}

expected_value = lambda state, action: -3 if state > max(table["state"]) else table[action][table["state"].index(state)]

alpha = 0.01

#random_numbers = [3, 2, 3, 1, 2, 1, 1, 2]

#random_index = 0

s_next = 0

#table[action][state - 1] += alpha * (max(expected_value(s_next, "stop"), expected_value(s_next, "continue")) - expected_value(s_curr, action) # update table value

for game in range(1,10000): # game

    if (game % 1000 == 0):

        alpha /= 2

    print("\nGame:", game)

    s_curr = random.randint(1, 3)
    #s_curr = random_numbers[random_index]

    #random_index += 1

    print("\nWe got a random # of", s_curr, "so our inital state is", s_curr)

    if (s_curr < 3):

        action = "continue"

    else:

        action = "stop"

    while (action == "continue"): # round

        change= random.randint(1, 3)
        #change = random_numbers[random_index]

        #random_index += 1

        s_next = s_curr + change

        print("\tcontinue -> random # =", change, "so state =", s_next)

        max_table = max(table["state"])

        if (s_next > max_table):

            a_max = -3
        
        else:

            a_max = max(expected_value(s_next, "stop"), expected_value(s_next, "continue"))

        print("\tresult =", a_max)

        update = alpha * (a_max - expected_value(s_curr, "continue"))

        table["continue"][table["state"].index(s_curr)] += update
        
        print("\tupdate = ", update)

        s_curr = s_next

        s_next = 0

        print("\n", table)

        if (s_curr >= max_table):
            
            break

    if (action == "stop"):

        print("\tstop -> state =", s_curr)

        if (s_curr > max(table["continue"])):

            a_max = -3
        
        else:

            a_max = expected_value(s_curr, "stop")

        print("\tresult =", a_max)

        continue