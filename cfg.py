
class CFG:
    def __init__(self, vas, tes, start, rules):
        self.vas = vas
        self.tes = tes
        self.start = start
        self.rules = [Production(r[0], r[1]) for r in rules]
        self.table = None

    def genCombinationProducers(self, cellA, cellB):
        entries = set()
        for varA in cellA.stack:
            for varB in cellB.stack:
                producers = self.findVarProducers(varA.producerVar, varB.producerVar)
                for producer in self.findVarProducers(varA.producerVar, varB.producerVar):
                    entries.add(CellEntry(producer, varA, varB))
        return entries

    def findVarProducers(self, varA, varB):
        producers = set()
        for rule in self.rules:
            if rule.produces(varA, varB):
                producers.add(rule.var)
        return producers

    def findTerProducers(self, symbol):
        producers = set()
        for rule in self.rules:
            if rule.produces(symbol):
                producers.add(rule.var)
        return producers

    def generateTable(self, in_string):
        l = len(in_string)
        # 2d Array, each cell is a set. Zeroth row has length entries, etc.
        table = [[Cell() for i in range(l - j)] for j in range(l)]

        # Input terminal producers on first row
        for i in range(l):
            prod = self.findTerProducers(in_string[i])
            [table[0][i].stack.insert(0, CellEntry(var,None,None, in_string[i])) for var in self.findTerProducers(in_string[i])]

        # Work through variable producers
        for row_ind in range(1, l):
            for col_ind in range(l - row_ind):
                targetCell = table[row_ind][col_ind]
                for perm in range(row_ind):
                    cellA = table[perm][col_ind]
                    cellB = table[row_ind-perm-1][col_ind+perm+1]
                    [targetCell.stack.insert(0, cellEntry) for cellEntry in self.genCombinationProducers(cellA, cellB)]
        return table

    def checkMembership(self, table):
        l = len(table)
        return True if self.start in [table[l-1][0].stack[i].producerVar for i in range(len(table[l-1][0].stack))] else False

    def printRightmostDerivation(self, table):
        l = len(table)
        if (not self.checkMembership(table)):
            print("No derivation")
            return

        for entry in table[l-1][0].stack:
            if (entry.producerVar == self.start):
                e_stack = list()
                t_stack = list()
                e_stack.append(entry)
                print(entry.producerVar)
                CFG.printNextGeneration(e_stack, t_stack)
                return


    def printNextGeneration(e_stack, t_stack):
        if (len(e_stack)==0):
            return
        rightmost = e_stack.pop(-1)
        if (rightmost.backEntryA == None or rightmost.backEntryB == None):
            t_stack.insert(0, rightmost.backTerminal)
        else:
            e_stack.append(rightmost.backEntryA)
            e_stack.append(rightmost.backEntryB)
        line = ""
        for e in e_stack:
            line += e.producerVar
        for t in t_stack:
            line += t
        print(line)
        CFG.printNextGeneration(e_stack, t_stack)

    def checkAmbiguity(self, table):
        l = len(table)
        derivations = 0
        for entry in table[l-1][0].stack:
            if (entry.producerVar == self.start):
                derivations += 1
        return derivations


class Production:
    def __init__(self, var, pTuple):
        self.var = var
        self.p1 = pTuple[0]
        self.p2 = pTuple[1] if (len(pTuple) > 1) else None
        self.is_terminal = self.p2==None

    def produces(self, p1, p2=None):
        return True if self.p1==p1 and self.p2==p2 else False


class Cell:
    def __init__(self):
        self.stack = list()

    def __repr__(self):
        out = ""
        for entry in self.stack:
            out += repr(entry) + ","
        return out

    def add(self, cellEntry):
        self.stack.insert(0, cellEntry)


class CellEntry:
    def __init__(self, producerVar, backEntryA=None, backEntryB=None, backTerminal=None):
        self.producerVar = producerVar
        self.backEntryA = backEntryA
        self.backEntryB = backEntryB
        self.backTerminal = backTerminal

    def __repr__(self):
        return self.producerVar



