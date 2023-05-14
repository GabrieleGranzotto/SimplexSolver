import gurobipy as gp
from gurobipy import GRB
import numpy as np

def solverSimplex(number_variables, variables_type, matrix_parameter, array_parameter, sign_parameter, objective_function, objective_function_target):
    model = gp.Model()
    model.Params.LogToConsole = 0

    lower_bound = [0] * number_variables
    upper_bound = GRB.INFINITY
    if variables_type == "cont":
        variables = model.addMVar(number_variables, lb=lower_bound, ub=upper_bound)
    if variables_type == "int":
        variables = model.addMVar(number_variables, lb=lower_bound, ub=upper_bound, vtype=GRB.INTEGER)
    if variables_type == "bin":
        variables = model.addMVar(number_variables, lb=lower_bound, ub=upper_bound, vtype=GRB.BINARY)
    model.update()

    A =  np.array(matrix_parameter)
    b = np.array(array_parameter)

    rows = len(b)
    for value in range(rows):
        if sign_parameter[value] == "min":
            model.addConstr(A[value]@variables <= b[value])
        if sign_parameter[value] == "max":
            model.addConstr(A[value]@variables >= b[value])
        if sign_parameter[value] == "eq":
            model.addConstr(A[value]@variables == b[value])
    model.update()

    obj_coefs = np.array(objective_function)
    if objective_function_target == "min":
        model.setObjective(obj_coefs @ variables, GRB.MINIMIZE)
    if objective_function_target == "max":  
        model.setObjective(obj_coefs @ variables, GRB.MAXIMIZE)

    model.optimize()

    solution_variables = list()
    for value in model.getVars():
        solution_variables.append([value.VarName, value.X])
  
    solution_optimal_value = model.ObjVal

    return solution_variables, solution_optimal_value


#############################################################################
number_variables = 5
variables_type = "cont"                             #"cont"/"int"/"bin"
matrix_parameter = [[2., 1.5, 0.5, 2.5, 0.7], 
                    [0.5, 0.25, 0.25, 1, 0.3],
                    [1, 1, 0, 0, 0],
                    [0, 0, 1, 0, -1]]
array_parameter = [100, 50, 10, 0]
sign_parameter = ["min", "min", "max", "eq"]        #"min"/"max"/"eq"
objective_function = [250, 230, 110, 350, 110]
objective_function_target = "max"                   #"min"/"max"
#############################################################################

solution_variables, solution_optimal_value = solverSimplex(number_variables, variables_type, matrix_parameter, array_parameter, sign_parameter, objective_function, objective_function_target)

print("\nUniversita' degli Studi di Trieste \nIntelligenza Artificiale e Data Analytics \nAlgoritmi di Ottimizzazione \na.a. 2022-23 \nGabriele Granzotto \nSM3201357 \n\n")



print("\nThis is the value of the Variables:")
for value in solution_variables:
    print('%s :: %g' % (value[0], value[1]))
print("\nAnd this the value of the Objective Function:")
print('Obj :: %g' % solution_optimal_value)