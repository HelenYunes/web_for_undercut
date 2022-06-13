from fairpy.items.undercut_procedure import undercut

class AlgoOutput:
 
    def __init__(self, algo: str, allocation: str):
        self.algo = algo
        self.allocation = allocation

def get_solution(algo_request):
    algo = algo_request.get('algorithm')
    items = algo_request.get('items')
    Alice = algo_request.get('preferences_a')
    Bob = algo_request.get('preferences_b')
    a={}
    b={}

    for index,item in enumerate(items):
        a[item] =int(Alice[index])
        b[item] =int(Bob[index])
    agents=[a,b]

    allocation = undercut(agents,items)
    return AlgoOutput(algo=algo, allocation=allocation)
