import gurobipy as gp
import numpy as np

class CutModel():

    def __init__(self, size, amount, width) -> None:
        self.size = size
        self.amount = amount
        self.width = width

        self.pricing_prob = None
        self.pattens = np.zeros([size, size])
        self.rmp, self.vars, self.ctns = self.create_rmp(size, amount, width)
        
    def create_rmp(self, size, amount, width):
        rmp = gp.Model('restricted master problem')
        var = rmp.addVars(len(size), vtype=gp.GRB.CONTINUOUS, name='x')

        rmp.setObjective(var.sum('*'), gp.GRB.MINIMIZE)

        for i in range(len(size)):
            self.pattens[i][i] = width//size[i]
        ctns = rmp.addConstrs((width//size[i]) * var[i] >= amount[i] for i in range(len(Size)))
        
        return rmp, var, ctns
    
    def create_pricing_problem(self, size, prices, width):
        mdl = gp.Model('pricing')

        for i in range(len(size)):
            mdl.a[i] = mdl.addVar(gp.GRB.INTEGER, ub=width//size[i], name='a')
        
        mdl.setObjective(1 - gp.quicksum([mdl.a[i]*prices[i] for i in range(len(prices))]), gp.GRB.MINIMIZE)
        mdl.addConstr(gp.quiksum([mdl.a[i]*size[i]] for i in range(len(size))) <= width)

        return mdl


