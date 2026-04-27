
class Formula(object):
    def __init__(self):
        self.clauses = []
        self.model = {}
        self.n = 0
        self.m = 0

    ## Read formula in DIMACS CNF format
    def readcnf(self,fp):
        raw = fp.readlines()
        lines = []
        for line in raw:
            line = line.strip()
            if line != "" and line[0] != 'c':
                lines.append(line);

        _,_,n,m = lines[0].split()
        self.n, self.m = int(n), int(m)
        del lines[0]
        
        self.clauses = [[]]*self.m

        for i in range(self.m):
            self.clauses[i] = list(map(int,lines[i].split(" ")[:-1]))

    ## Assign a variable to make lit true
    def assign(self,lit):
        ## Remove clauses satisfied when lit = true
        self.clauses = [clause for clause in self.clauses if lit not in clause]

        ## Remove false literals where -lit = false
        for i in range(len(self.clauses)): self.clauses[i] = [l for l in self.clauses[i] if l != -lit]

        ## Add lit to model
        self.model[abs(lit)] = lit > 0;

    ## Find a unit clause
    def unit(self):
        if 1 in map(len,self.clauses):
            return self.clauses[list(map(len,self.clauses)).index(1)][0];        
        else: return None

    ## Find a pure literal
    def pure(self):
        lits = set([lit for clause in self.clauses for lit in clause])
        for lit in lits:
            if -lit not in lits: return lit
        return None

    ## Is this formula a tautology? 
    def istrue(self):
        return len(self.clauses) == 0

    ## Is this formula a contradiction?
    def isfalse(self):
        return [] in self.clauses
