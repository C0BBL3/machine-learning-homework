import math

slacks = {
    "x_4": [3, 2, 5, 1, 0, 0, 0, 55],
    "x_5": [2, 1, 1, 0, 1, 0, 0, 26],
    "x_6": [1, 1, 3, 0, 0, 1, 0, 30],
    "x_7": [5, 2, 4, 0, 0, 0, 1, 57],
    "max": [-20, -10, -15, 0, 0, 0, 0, 0]
}
original_constraint_length = 3

def create_substitution_slack(slack, slack_index, largest_index):

    slack_update = [x for x in slack]
    divisor = slack[largest_index]

    for i, coeff in enumerate(slack):
        slack_update[i] = round(coeff / divisor, 5)

    return slack_update

def update_slacks(slacks, largest_index):

    slack_update = slacks["x_" + str(largest_index + 1)]
    updated_slacks = {"x_" + str(largest_index + 1): slack_update}

    for slack_key, slack in slacks.items():

        if slack_key != "max" and int(slack_key[-1]) - 1 == largest_index:
            continue

        new_slack = []
        multiplier = slack[largest_index]

        for i, coeff in enumerate(slack):
            delta = slack_update[i] * multiplier
            new_slack.append(round(coeff - delta, 5))

        updated_slacks[slack_key] = new_slack

    return updated_slacks

while slacks["max"][:original_constraint_length].count(0) <= original_constraint_length:

    largest_index = slacks["max"].index(min(slacks["max"][:-1]))

    harshest_constraint = {}
    for slack_key, slack in slacks.items():
        if slack_key != "max" and slack[-1] / slack[largest_index] > 0:
            harshest_constraint[slack_key] = slack[-1] / slack[largest_index]
    harshest_constraint_key = list(harshest_constraint.keys())[list(harshest_constraint.values()).index(min(harshest_constraint.values()))] # find harshest constraint variable index, example x_7 has the harshest constraint, so 7 is the index

    variable_change_index = original_constraint_length + list(slacks.keys()).index(harshest_constraint_key)

    slack_update = create_substitution_slack(slacks[harshest_constraint_key], variable_change_index, largest_index) # solve for the variable change index, following previous example ^, solving for x_1
    try: del slacks[harshest_constraint_key] # remove old pre-variable-change function, following previous example ^^, removing the x_7 function from the dictionary
    except: pass
    slacks["x_" + str(largest_index + 1)] = slack_update # add the new varaible changed function, following the previous example ^^^, appending the solved for x_1 function

    slacks = update_slacks(slacks, largest_index) # substitute the variable change into the other equations, following previous example ^^^^, substitute x_1 into the other equations

    continue # and repeat

print("\nBest Prediction:", slacks["max"][-1], '\n') # no more positive coeffs in max function, best prediction has been reached