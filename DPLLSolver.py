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
    # creates a copy for testing, allows formula to be for backtracking
    newFormula = Formula.Formula()
    newFormula.clauses = formula.clauses.copy()
    newFormula.model = formula.model.copy()
    newFormula.n = formula.n
    newFormula.m = formula.m

    print()
    print("Start", "newFormula", newFormula.model, "Formula", formula.model)

    # check for tautology and contradiction
    if newFormula.istrue() == True:
        print("Taut True")
        return True, newFormula.model, branch
    elif newFormula.isfalse() == True:
        print("Contra False")
        return False, newFormula.model, branch

    # check for units
    unit = newFormula.unit()
    while unit != None:
        print("unit", unit)
        newFormula.assign(unit)
        if newFormula.istrue() == True:
            print("Unit True")
            return True, newFormula.model, branch
        elif newFormula.isfalse() == True:
            print("Unit False")
            return False, newFormula.model, branch
        unit = newFormula.unit()

    # check for pure literals
    pure = newFormula.pure()
    while pure != None:
        print("pure", pure)
        newFormula.assign(pure)
        if newFormula.istrue() == True:
            print("Pure True")
            return True, formula.model, branch
        elif newFormula.isfalse() == True:
            print("Pure False")
            return False, newFormula.model, branch
        pure = newFormula.pure()

    # check for tautology and contradiction
    if newFormula.istrue() == True:
        print("Taut True")
        return True, newFormula.model, branch
    elif newFormula.isfalse() == True:
        print("Contra False")
        return False, newFormula.model, branch

    # if any changes were made to newFormula, they get copied here
    formula.model = newFormula.model.copy()
    formula.clauses = newFormula.clauses.copy()

    # heuristic search
    # print("Clauses", newFormula.clauses)
    max = {}

    if len(newFormula.clauses) != 0:
        clauseLen = [len(c) for c in newFormula.clauses]
        clauseLen = sorted(clauseLen)
        minLen = clauseLen[0]
        # lengths = {}

        # creates a dictionary of all lengths
        # for l in clauseLen:
        #     lengths[l] = 1

        # iterates over all lengths
        # for l in lengths.keys():
        #     minLen = l

        for n in range(1, newFormula.n+1):
            max[n] = 0
            max[-n] = 0
            for c in newFormula.clauses:
                if len(c) == minLen:
                    for i in range(len(c)):
                        if c[i] == n:
                            max[n] += 1
                        elif c[i] == -n:
                            max[-n] += 1

        # sorts to find the most common var
        maxTuples = [(max[i], i) for i in max.keys()]
        maxTuples.sort(reverse=True)

        print()
        print("max", maxTuples)
        print()

        if branch % 50 == 0 and branch != 0:
            print(branch)
            return None

        # assigns the vars by most common
        for x in range(len(maxTuples)):
            # checks the var is actually still in a clause
            if maxTuples[x][0] != 0:
                branch += 1

                chosen = maxTuples[x][1]
                newFormula.assign(chosen)
                print("chosen", chosen, "model", newFormula.model)

                # tempFormula = Formula.Formula()
                # tempFormula.clauses = newFormula.clauses.copy()
                # tempFormula.model = newFormula.model.copy()
                # tempFormula.n = formula.n
                # tempFormula.m = formula.m
                # tempFormula.assign(chosen)


                    # print("clauses", tempFormula.clauses)
                # repeat! first with given result
                result, solnModel, finalCount = theLoop(newFormula, branch)

                # print("branch " + str(branch))
                # print("solnModel", solnModel)
                if result == True:
                    print("Result True")
                    return True, solnModel, finalCount

                # # test, opposite result? but undo result
                # newFormula.model = formula.model.copy()
                # newFormula.assign(-chosen)
                # result2, solnModel2, finalCount2 = theLoop(newFormula, branch)
                # # print(solnModel)
                # if result2 == True:
                #     return True, solnModel2, finalCount2

                # undo assignments, need to do this anymore with the way formula is handled?
                newFormula.model = formula.model.copy()
                newFormula.clauses = formula.clauses.copy()

                print("newFormula", newFormula.model)
                print("Formula", formula.model)
                print()

    print("End Tuple False")
    return False, formula.model, branch

# for printing the results of the file
def printSoln(formula, model, boolean, branch):
    # creating a string for naming a file after the current time
    now = datetime.datetime.now()
    now_string = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + "-" + str(now.minute)

    # creating a file
    filename = f"Solution for CNF on {formula.n} Vars of {formula.m} Clauses - {now_string} .txt"
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
        printSoln(formula, model, True, branch)
        print(statement)
    elif statement == False:
        printSoln(formula, model, False, branch)
        print(statement)
        
        

