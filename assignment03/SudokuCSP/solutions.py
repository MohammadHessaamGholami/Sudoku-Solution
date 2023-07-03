from utils import first
import queue


# Variable ordering

def first_unassigned_variable(assignment, csp):
    """The default variable order."""
    return first([var for var in csp.variables if var not in assignment])


def mrv(assignment, csp):
    #{0: '123456789', 1: '123456789', 2: '123456789', 3: '2', 4: '6', 5: '123456789', 6: '7', 7: '123456789', 8: '1', 9: '6', 10: '8', 11: '123456789', 12: '123456789', 13: '7', 14: '123456789'
    #print(assignment)
    #assingnment:
    '''
    {}
    {0: '1'}
    {0: '1', 1: '2'}
    {0: '1', 1: '2', 2: '3'}
    {0: '1', 1: '2', 2: '4'}
    {0: '1', 1: '2', 2: '5'}
    {0: '1', 1: '2', 2: '6'}
    {0: '1', 1: '2', 2: '7'}
    {0: '1', 1: '2', 2: '8'}
    {0: '1', 1: '2', 2: '9'}
    {0: '1', 1: '3'}
    {0: '1', 1: '3', 2: '9'}
    {0: '1', 1: '3', 2: '9', 3: '2'}
    {0: '1', 1: '3', 2: '9', 3: '2', 4: '6'}
    {0: '1', 1: '3', 2: '9', 3: '2', 4: '6', 5: '4'}
    {0: '1', 1: '3', 2: '9', 3: '2', 4: '6', 5: '4', 6: '7'}
    {0: '1', 1: '3', 2: '9', 3: '2', 4: '6', 5: '4', 6: '7', 7: '5'}
    {0: '1', 1: '3', 2: '9', 3: '2', 4: '6', 5: '4', 6: '7', 7: '8'}
    '''
    """
       Q1
       Minimum-remaining-values heuristic.
       returns minimun remaining value for variables
       """
    min_value = 100
    min_variable = 81
    for i in range(len(csp.curr_domains)):
        if (i in assignment):
            continue;
        if (len(csp.curr_domains[i]) < min_value):
            min_value = len(csp.curr_domains[i])
            min_variable = i
    return min_variable

# Value ordering

def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)


def lcv(var, assignment, csp):

    """
    Q2
    Least-constraining-values heuristic.
	returns list of variables
    """
    my_data ={}
    for number_value in csp.curr_domains[var]:
        my_data[int(number_value)]=0
        for neighbor_variable in csp.neighbors[var]:  # NEIGHBORS[VAR]
                if (neighbor_variable not in assignment and number_value in csp.curr_domains[neighbor_variable]):
                    my_data[int(number_value)] = my_data[int(number_value)] + 1
                    # if we put number_value in variable delete my_data[int(number_value)] from its domains
    SortedArray=sorted(my_data.items(), key=lambda kv: (kv[1], kv[0]))
    output=[]
    #print("*******")
    #print(SortedArray)
    for item in SortedArray:
        output.append(str(item[0]))
    #print(output)
    # we find minimum value
    return output

def no_inference(csp, var, value, assignment, removals):
    return True


def forward_checking(csp, var, value, assignment, removals):
    """
        Q3
        Prune neighbor values inconsistent with var=value.
    """

    for neighbor in csp.neighbors[var]:
        if neighbor in assignment:
            continue
        if value in csp.curr_domains[neighbor]:
            if (len(csp.curr_domains[neighbor]) == 1):
                csp.prune(neighbor, value, removals)
                return False
            else:
                csp.prune(neighbor, value, removals)

    return True


def arc_cons(csp, var, value, assignment, removals):
    """
    Q4
    Maintain arc consistency.
    """
    my_queue=queue.Queue()
    for neighbor in csp.neighbors[var]:
        my_queue.put((neighbor,value))
    #print(var)
    #print(value)
    #print(csp.display(csp.infer_assignment()))
    while (not my_queue.empty()):
        item = my_queue.get()
        neighbor = item[0]
        value = item[1]
        if neighbor in assignment:
            continue
        if value in csp.curr_domains[neighbor]:
            if (len(csp.curr_domains[neighbor]) == 1):
                csp.prune(neighbor, value, removals)
                return False
            else:
                csp.prune(neighbor, value, removals)
                if (len(csp.curr_domains[neighbor]) == 1 ):
                    for neighbor_of_neighbor in csp.neighbors[neighbor]:
                        if(neighbor_of_neighbor not in assignment and int(csp.curr_domains[neighbor][0]) in csp.curr_domains[neighbor_of_neighbor] ):
                                my_queue.put((neighbor_of_neighbor,int(csp.curr_domains[neighbor][0])))
    #print(csp.curr_domains)
    #print("*******************************************************************************************")
    return True


def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=forward_checking):



    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None


    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result
