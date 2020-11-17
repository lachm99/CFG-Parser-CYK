
class CFG:
    def __init__(self, vas, tes, start, rules):
        self.vas = vas
        self.tes = tes
        self.start = start
        self.rules = [Production(r[0], r[1]) for r in rules]

    def cyk(self, in_string):
        l = len(in_string)
        # 2d Array, each cell is a set. Zeroth row has length entries, etc.
        table = [[set() for i in range(l - j)] for j in range(l)]

        # Input terminal producers on first row
        for i in range(l):
            for rule in self.rules:
                if (rule.p1 == in_string[i]):
                    table[0][i].add(rule.var)

        # Work through variable producers
        for row_ind in range(1, l):
            for col_ind in range(l - row_ind):
                for perm in range(row_ind):
                    # Check what can produce such a cell
                    combinations = CFG.combine_cells(table[perm][col_ind], table[row_ind-perm-1][col_ind+perm+1])
                    for rule in self.rules:
                        for com in combinations:
                            if (rule.produces(com)):
                                table[row_ind][col_ind].add(rule.var)

        if (self.start in table[l-1][0]):
            print("1")
        else:
            print("0")


    def combine_cells(cellA, cellB):
        combinations = set()
        for varA in cellA:
            for varB in cellB:
                combinations.add((varA, varB))
        return combinations


class Production:
    def __init__(self, var, production):
        self.var = var
        self.is_terminal = True if len(production)==1 else False
        self.p1 = production[0]
        self.p2 = None
        if (not self.is_terminal):
            self.p2 = production[1]


    def produces(self, var_tuple):
        if (self.is_terminal):
            return False
        return True if (var_tuple[0] == self.p1 and var_tuple[1] == self.p2) else False

