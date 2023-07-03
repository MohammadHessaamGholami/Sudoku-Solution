from utils import count, first
import search


class CSP(search.Problem):
    """This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b

    the class supports data structures and methods that help you
    solve CSPs by calling a search function on the CSP. Methods and slots are
    as follows, where the argument 'a' represents an assignment, which is a
    dict of {var:val} entries:
        assign(var, val, a)     Assign a[var] = val; do other bookkeeping
        unassign(var, a)        Do del a[var], plus other bookkeeping
        nconflicts(var, val, a) Return the number of other variables that
                                conflict with var=val
        curr_domains[var]       Slot: remaining consistent values for var
                                Used by constraint propagation routines.
    The following are just for debugging purposes:
        nassigns                Slot: tracks the number of assignments made
        display(a)              Print a human-readable representation
    """

    def __init__(self, variables, domains, neighbors, constraints):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        variables = variables or list(domains.keys())
        '''domains:
        {0: '123456789', 1: '123456789', 2: '123456789', 3: '2'}
        
        variables:
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
        
        neighbors:
        {... ,80: {35, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 8, 17, 44, 53, 26, 60, 61, 62} }
        
        constraints(1,5,2,6):
            if isConflict(var(1) = 5 and var(2)=6):
                return True
        
        print(self.display(self.infer_assignment())):
            just show the soduko board
            
        
        
        """ ****************************
        my =[]
        self.prune(0,'1',my)
        print(self.curr_domains):
                {0: ['2', '3', '4', '5', '6', '7', '8', '9'], 1: ['1', '2', '3', '4', '5', '6', '7', '8', '9'], 2: ['1', '2', '3', '4', '5', '6', '7', '8', '9'], ... }

        print(my): [(0, '1')]
        
        self.restore(my)
        print(self.curr_domains):
                {0: ['2', '3', '4', '5', '6', '7', '8', '9', '1'], 1: ['1', '2', '3', '4', '5', '6', '7', '8', '9'], 2: ['1', '2', '3', '4', '5', '6', '7', '8', '9'], ...}
        """
        
          
        
        """
        print(self.curr_domains)
            {0: ['1', '2', '3', '4', '5', '6', '7', '8', '9'], 1: ['1', '2', '3', '4', '5', '6', '7', '8', '9'], ... }
        
        print(self.suppose(0,'9'))
        
        print(self.curr_domains)
            {0: ['9'], 1: ['1', '2', '3', '4', '5', '6', '7', '8', '9'], 2: ['1', '2', '3', '4', '5', '6', '7', '8', '9'],...}
        """
        
              
        """
            self.support_pruning()
            print(self.choices(0)):
                ['1', '2', '3', '4', '5', '6', '7', '8', '9']
                
            print(self.choices(3)):
                ['2']    
                    
        """
        
        print(self.infer_assignment()):
            {3: '2', 4: '6', 6: '7', 8: '1', 9: '6', 10: '8', 13: '7', 16: '9', 18: '1', 19: '9', 23: '4', 24: '5', 27: '8', 28: '2', 30: '1', 34: '4', 38: '4', 39: '6', 41: '2', 42: '9', 46: '5', 50: '3', 52: '2', 53: '8', 56: '9', 57: '3', 61: '7', 62: '4', 64: '4', 67: '5', 70: '3', 71: '6', 72: '7', 74: '3', 76: '1', 77: '8'}



        self.support_pruning()
        self.unassign(1,self.domains)
        print(domains):
            {0: '123456789', 2: '123456789', 3: '2', 4: '6', 5: '123456789',... }
            
            
            
        self.support_pruning()
        self.unassign(1,self.curr_domains)
        print(self.curr_domains):
            ERORRRRRRRRRRRRRRRRRR
            
        
        
            
        self.assign(1,5,self.domains)
        print(self.domains):
            {0: '123456789', 1: 5, 2: '123456789', 3: '2', 4: '6',...}
        
        
        
        self.support_pruning()    
        self.assign(1,'5',self.curr_domains)
        print(self.curr_domains):
           {0: ['1', '2', '3', '4', '5', '6', '7', '8', '9'], 1: '5', 2: ['1', '2', '3', '4', '5', '6', '7', '8', '9'], ... } 
        
        
        print(self.nconflicts(1,'8',self.domains)):
            1
       
        print(self.nconflicts(0,'6',self.domains)):
            2

        '''
        #print(neighbors[80])
        #print(domains)
        variables.pop()
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0
#        self.support_pruning()
        self.support_pruning()
        #print(self.variables)
        #print(self.neighbors[0])




    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""

        # Subclasses may implement this more efficiently
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))

        return count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        # Subclasses can print in a prettier way, or display with a GUI
        print('CSP:', self, 'with assignment:', assignment)

    # These methods are for the tree and graph-search interface:

    def actions(self, state):
        """Return a list of applicable actions: nonconflicting
        assignments to an unassigned variable."""
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        """Perform an action and return the new state."""
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    # These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        """Return the partial assignment implied by the current inferences."""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

    # This is for min_conflicts search

    def conflicted_vars(self, current):
        """Return a list of variables in current assignment that are in conflict"""
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]
