import math

# justin loopy method

slacks = {"x_4": [55, -3, -2, -5], # [constant, x_1, x_2, x_3, ...]
           "x_5": [26, -2, -1, -1],
           "x_6": [30, -1, -1, -3],
           "x_7": [57, -5, -2, -4]}
original_constraint_length = 3
max_ = [0, 20, 10, 15] # [constant, x_1, x_2, x_3, ...]
slacks["max"] = max_

def adjust_slacks(slacks):
    adjusted_slacks = {}
    for x, slack in slacks.items():
        adjusted_slacks[x] = slack + [0 for _ in range(len(slacks) - 1)]
    return adjusted_slacks

def create_substitution_slack(slack, slack_index, largest_index):
    slack_update = [x for x in slack]
    divisor = slack[largest_index]
    for index, coeff in enumerate(slack):
        if index != largest_index:
            if divisor > 0:
                slack_update[index] = coeff / divisor
            elif divisor < 0:
                slack_update[index] = -1 * coeff / divisor
        else:
            slack_update[index] = 0
    slack_update_index = slack_index
    if divisor > 0:
        slack_update[slack_update_index] = -1 / divisor
    elif divisor < 0:
        slack_update[slack_update_index] = 1 / divisor
    return slack_update

def update_slacks(adjusted_slacks, largest_index):
    slack_update = adjusted_slacks["x_" + str(largest_index)]
    updated_slacks = {"x_" + str(largest_index): slack_update}
    for slack_index, slack in adjusted_slacks.items():
        if slack_index == "max" or int(slack_index[-1]) != largest_index:
            updated_slack = []
            multiplier = int(slack[largest_index])
            for coeff_index, coeff in enumerate(slack):
                if coeff_index != largest_index:
                    updated_slack.append(coeff + slack_update[coeff_index] * multiplier)
                else:
                    updated_slack.append(0.0)
        else:
            updated_slack = slack_update
        updated_slacks[slack_index] = updated_slack
    return updated_slacks

for i in range(10):
    largest_index = slacks["max"].index(max(slacks["max"][1:]))
    if slacks["max"][largest_index] <= 0:
        print("\nBest Prediction:", slacks["max"][0], '\n') # no more positive coeffs in max function, best prediction has been reached
        break

    harshest_constraint = []
    for slack_index, slack in slacks.items():
        if slack_index != "max":
            harshest_constraint.append(abs(slack[0] / slack[largest_index]))
    harshest_constraint_index = list(slacks.keys())[harshest_constraint.index(min(harshest_constraint))] # find harshest constraint variable index, example x_7 has the harshest constraint, so 7 is the index

    adjusted_slacks = adjust_slacks(slacks) # append columns so algebra for higher index variables may be done

    variable_change_index = original_constraint_length + list(adjusted_slacks.keys()).index(harshest_constraint_index) + 1 # the variable change in the harshest constraint slack, ex x_7 -> x_1 given x_1 has largest value in max function and x_7 has harshest constraint

    slack_update = create_substitution_slack(adjusted_slacks[harshest_constraint_index], variable_change_index, largest_index) # solve for the variable change index, following previous example ^, solving for x_1
    
    try: 
        del adjusted_slacks["x_" + str(variable_change_index)] # remove old pre-variable-change function, following previous example ^^, removing the x_7 function from the dictionary
    except:
        pass

    adjusted_slacks["x_" + str(largest_index)] = slack_update # add the new varaible changed function, following the previous example ^^^, appending the solved for x_1 function

    updated_slacks = update_slacks(adjusted_slacks, largest_index) # substitute the variable change into the other equations, following previous example ^^^^, substitute x_1 into the other equations

    slacks = updated_slacks # update slack coeffs for next iteration
    
    continue # and repeat

    

        