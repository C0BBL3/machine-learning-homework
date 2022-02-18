import random
import math

table = {
    "state": [(1, False), (1, True), (2, False), (2, True), (3, False), (3, True)], 
    "stop": [1, 1, 2, 2, 3, 3], 
    "continue": [1, 1, 1, 1, -3, -3],
    "mulligan": [1, None, 1, None, 1, None]
} # initial table

def expected_value(state, action):
    max_value = max(table["state"])[0]
    if state[0] > max_value:
        return -3
    return table[action][table["state"].index(state)]

alpha = 0.01

random_numbers = [1, 3, 1, 1, 3]

random_index = 0

mulligan_index = 0

s_next = 0

action = None

mulligan = False

game = 0

s_curr = (0, None) # default boi

#table[action][state - 1] += alpha * (max(expected_value(s_next, "stop"), expected_value(s_next, "continue")) - expected_value(s_curr, action) # update table value

while (game < 10000): # game

    #if (game % 1000 == 0):

     #   alpha /= 2

    if (not mulligan):
        print("\nGame:", game)

        #s_curr = (random.randint(1, 3), mulligan)
        temp = (random_numbers[random_index], mulligan)
        
        random_index += 1

        print("\nWe got a random # of", temp, "so our inital state is", temp)

        if (temp[0] < 3):

            action = ["mulligan", "continue", "mulligan"][mulligan_index] #random.choices(["continue", "mulligan"], [0.5, 0.5])

            mulligan_index += 1
        
            if (action == "mulligan"):

                print("\n\tMulligan mood")

                mulligan = True

                continue

            s_curr = temp
        
        else:

            action = "stop"

    else:

        #s_next = (random.randint(1, 3), mulligan)
        s_next = (s_curr[0] + random_numbers[random_index], mulligan)
        
        random_index += 1

        print("\nWe got a random # of", s_next, "so our inital state is", s_next)
        

        if (s_next[0] < 3):

            action = "continue"

        else:
            
            action = "stop"
        

    while (action == "continue"): # round

        #change= random.randint(1, 3)
        change = random_numbers[random_index]

        random_index += 1

        temp = (s_curr[0] + change, mulligan)

        print("\tcontinue -> random # =", change, "so state =", temp)

        if (not mulligan):

            action = ["mulligan", "continue", "mulligan"][mulligan_index] #random.choices(["continue", "mulligan"], [0.5, 0.5])

            mulligan_index += 1
        
            if (action == "mulligan"):

                print("\n\tMulligan mood")

                mulligan = True

                continue
        
        s_next = temp

        max_table = max(table["state"])[0]

        if (s_next[0] > max_table):

            a_max = -3
        
        else:

            a_max = max(expected_value(s_next, "stop"), expected_value(s_next, "continue"), expected_value(s_next, "mulligan"))

        print("\tresult =", a_max)

        update = alpha * (a_max - expected_value(s_curr, "continue"))

        table["continue"][table["state"].index(s_curr)] += update
        
        print("\tupdate = ", update)

        s_curr = s_next

        s_next = 0

        print("\n", table)

        if (s_curr[0] >= max_table):
            
            break

    if (action == "stop"):

        temp = s_curr
        
        if (mulligan):
            
            temp = s_next

            print("\tstop -> state =", temp)

            max_table = max(table["state"])[0]

            if (s_next[0] > max_table):

                a_max = -3
            
            else:

                a_max = max(expected_value(s_next, "stop"), expected_value(s_next, "continue"))

            #print("\tresult =", a_max)

            update = alpha * (a_max - expected_value(s_curr, "mulligan"))

            table["mulligan"][table["state"].index(s_curr)] += update
            
            print("\tupdate = ", update)

        mulligan = False
        
        if (temp[0] > max(table["state"])[0]):

            a_max = -3
        
        else:

            a_max = expected_value(temp, "stop")

        print("\tresult =", a_max)

        game += 1

        continue