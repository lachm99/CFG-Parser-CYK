
class CFG:
    def __init__(self, vas, tes, start, rules):
        self.vars = vas
        self.ters = tes
        self.start = start
        self.rules = [ProductionRule(rule[0], rule[1]) for rule in rules]

    def genCombinationProducers(self, cellA, cellB):
        entries = list()
        for varA in cellA.entries:
            for varB in cellB.entries:
                producers = self.findVarProducers(varA.producerVar, varB.producerVar)
                for producer in self.findVarProducers(varA.producerVar, varB.producerVar):
                    entries.append(CellEntry(producer, varA, varB))
        return entries

    def findVarProducers(self, varA, varB):
        producers = list()
        for rule in self.rules:
            if rule.produces(varA, varB):
                producers.append(rule.var)
        return producers

    def findTerProducers(self, symbol):
        producers = list()
        for rule in self.rules:
            if rule.produces(symbol):
                producers.append(rule.var)
        return producers

    def generateTable(self, in_string):
        l = len(in_string)
        # 2d Array, each cell is a set. Zeroth row has length entries, etc.
        table = [[TableCell() for i in range(l - j)] for j in range(l)]

        # Input terminal producers on first row
        for i in range(l):
            prod = self.findTerProducers(in_string[i])
            [table[0][i].entries.append(CellEntry(var,None,None, in_string[i])) for var in self.findTerProducers(in_string[i])]

        # Work through variable producers
        for row_ind in range(1, l):
            for col_ind in range(l - row_ind):
                targetCell = table[row_ind][col_ind]
                for perm in range(row_ind):
                    cellA = table[perm][col_ind]
                    cellB = table[row_ind-perm-1][col_ind+perm+1]
                    [targetCell.entries.append(cellEntry) for cellEntry in self.genCombinationProducers(cellA, cellB)]
        return table

    def checkMembership(self, table):
        return True if (self.start in self.topCell(table).entries) else False

    def printRightmostDerivation(self, table):
        e_stack = list()
        t_stack = list()
        for entry in self.topCell(table).entries:
            if (entry == self.start):
                e_stack.append(entry)
                break
        line = ""
        while (len(e_stack) > 0):
            line += "".join([repr(e) for e in e_stack])
            line += "".join(t_stack) + "\n"
            rightmost = e_stack.pop(-1)
            if (rightmost.backTerminal == None):
                e_stack.append(rightmost.backEntryA)
                e_stack.append(rightmost.backEntryB)
            else:
                t_stack.insert(0, rightmost.backTerminal)
        line += "".join((t_stack))
        print(line) if line else print("No derivation")


    def checkAmbiguity(self, table):
        derivations = self.topCell(table).entries.count(self.start)
        return (derivations > 1)

    def topCell(self, table):
        return table[len(table)-1][0]


class ProductionRule:
    def __init__(self, producerVariable, producedTuple):
        self.var = producerVariable
        self.p1 = producedTuple[0]
        self.p2 = producedTuple[1] if (len(pTuple) > 1) else None
        self.is_terminal = (self.p2==None)

    def produces(self, product1, product2=None):
        return True if (self.product1==p1 and self.product2==p2) else False


class TableCell:
    def __init__(self):
        self.entries = list()

    def contains(self, producerVar):
        return (producerVar in self.entries)

class CellEntry:
    def __init__(self, producerVar, backEntryA=None, backEntryB=None, backTerminal=None):
        self.producerVar = producerVar
        self.backEntryA = backEntryA
        self.backEntryB = backEntryB
        self.backTerminal = backTerminal

    def __repr__(self):
        return self.producerVar

    # A really shallow equality check - only checks if the producer variable is the same
    def __eq__(self, other):
        return (self.producerVar == other)

    def __repr__(self):
        return self.producerVar



