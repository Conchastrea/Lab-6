# 1. initialize formulas
# 2. loop time already?
# a) check for sol'n
# b) units
# c) pure literals
# d) atomic formulas
# e) heuristics

import sys
import Formula
import datetime

def theLoop(formula, branch):

    # print()
    # print("Start", "formula", formula.model, "Formula", formula.model)

    # check for tautology and contradiction
    if formula.istrue() == True:
        # print("Taut True")
        return True, formula.model, branch
    elif formula.isfalse() == True:
        # print("Contra False")
        return False, formula.model, branch

    # loop in case pure literals create units
    changed = True
    while changed:
        changed = False

        # check for units
        unit = formula.unit()
        while unit != None:
            # print("unit", unit)
            formula.assign(unit)
            changed = True
            if formula.istrue() == True:
                # print("Unit True")
                return True, formula.model, branch
            elif formula.isfalse() == True:
                # print("Unit False")
                return False, formula.model, branch
            unit = formula.unit()

        # check for pure literals
        pure = formula.pure()
        while pure != None:
            # print("pure", pure)
            formula.assign(pure)
            changed = True
            if formula.istrue() == True:
                # print("Pure True")
                return True, formula.model, branch
            elif formula.isfalse() == True:
                # print("Pure False")
                return False, formula.model, branch
            pure = formula.pure()

    # check for tautology and contradiction
    if formula.istrue() == True:
        # print("Taut True")
        return True, formula.model, branch
    elif formula.isfalse() == True:
        # print("Contra False")
        return False, formula.model, branch

    # if any changes were made to formula, they get copied here
    # formula.model = formula.model.copy()
    # formula.clauses = formula.clauses.copy()

    # heuristic search
    # print("Clauses", formula.clauses)
    if len(formula.clauses) != 0:

        minLen = min(len(c) for c in formula.clauses)
        # lengths = {}

        # creates a dictionary of all lengths
        # for l in clauseLen:
        #     lengths[l] = 1

        # iterates over all lengths
        # for l in lengths.keys():
        #     minLen = l

        maxVar = {}
        for c in formula.clauses:
            if len(c) == minLen:
                for var in c:
                    maxVar[var] = maxVar.get(var, 0) + 1


        # print()
        # print("max", maxVar)
        # print()

        # if branch % 25 == 0 and branch != 0:
        #     print(branch)
        #     return None

        # checks the var is actually still in a clause
        if maxVar != {}:
            branch += 1
            chosen = max(maxVar, key=maxVar.get)
            formula.assign(chosen)
            # print("chosen", chosen, "model", formula.model)

            # tempFormula = Formula.Formula()
            # tempFormula.clauses = formula.clauses.copy()
            # tempFormula.model = formula.model.copy()
            # tempFormula.n = formula.n
            # tempFormula.m = formula.m
            # tempFormula.assign(chosen)

            savedClauses = [c[:] for c in formula.clauses]
            savedModel = dict(formula.model)

            # print("clauses", tempFormula.clauses)
            # repeat! first with given result
            result, solnModel, finalCount = theLoop(formula, branch)

            # print("branch " + str(branch))
            # print("solnModel", solnModel)
            if result == True:
                # print("Result True")
                return True, solnModel, finalCount

            # test, opposite result? but undo result
            formula.model = savedModel
            formula.clauses = savedClauses

            formula.assign(-chosen)
            result, solnModel, finalCount2 = theLoop(formula, branch)
            # print(solnModel)
            if result == True:
                # print("Result True")
                return True, solnModel, finalCount2

            # print("formula", formula.model,"Formula", formula.model)
            # print()

    # print("End Tuple False")
    return False, formula.model, finalCount2

# for printing the results of the file
def printSoln(formula, model, boolean, branch, givenFile):
    # creating a string for naming a file after the current time
    now = datetime.datetime.now()
    now_string = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + "-" + str(now.minute)

    if givenFile.find("/") != -1:
        givenFile = givenFile.split("/",1)[1]
    if givenFile.find(".") != -1:
        givenFile = givenFile.split(".",1)[0]

    # creating a file
    filename = f"Solution for {givenFile} - {now_string}.txt"
    solnFile = open(filename, "w")

    # print(model)
    if boolean == True:
        # writes header
        solnFile.write(f"s cnf 1 {formula.n} {formula.m}\n")

        varList = list(model.keys())

        # a loop to write eachs of the vertices and it's colors
        for x in range(len(varList)):
            if model[varList[x]] == True:
                solnFile.write(f"v {x+1} \n")
            else:
                solnFile.write(f"v -{x+1} \n")
    else:
        # writes header which is everything
        solnFile.write(f"s cnf 0 {formula.n} {formula.m}\n")

    solnFile.write(f"branches {branch}")

    # close the file
    solnFile.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python DPLLSolver.py <formula>")
        sys.exit(1)

    formula = Formula.Formula()
    file = open(sys.argv[1], "r")
    formula.readcnf(file)
    file.close()

    branch = 0
    statement, model, branch = theLoop(formula, branch)
    # print("passed model, end", model)
    if statement == True:
        printSoln(formula, model, True, branch, sys.argv[1])
        print(statement)
    elif statement == False:
        printSoln(formula, model, False, branch, sys.argv[1])
        print(statement)
        
        

