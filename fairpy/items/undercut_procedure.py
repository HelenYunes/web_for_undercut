"""
Implementing the algorithm in the following article: "A note on the undercut procedure"
By Haris Aziz
2014
Link to the article: https://arxiv.org/pdf/1312.6444.pdf

Programmer: Helen Yonas
Date: 2022-05

The undercut procedure is a procedure for fair item assignment between *two* people.
"""

from typing import List, Any
from unittest import result
import fairpy
from fairpy import Agent 
from fairpy.allocations import Allocation
from more_itertools import powerset 
from sympy import group
import logging
logger = logging.getLogger(__name__)

Y=False


def undercut(agents: List[Agent], items: List[Any]):
    """
    Undercut Procedure - An algorithm that returns a envy free allocation (if it exists)
    even when the agents may express indifference between objects.
    
    Note: The number of agents should be 2.
    
    :param agents: The agents who participate in the division
    :param items: The items which are divided
    :return: An envey free allocation if it exists
    
    >>> Alice = ({"a": 7, "b": 4, "c": 3, "d":2})
    >>> Bob = ({"a": 1, "b": 7, "c": 3, "d":2})
    >>> items=['a','b','c','d']
    >>> A = fairpy.agents.AdditiveAgent({"a": 7, "b": 4, "c": 3, "d":2}, name="Alice")
    >>> B = fairpy.agents.AdditiveAgent({"a": 1, "b": 7, "c": 3, "d":2}, name="Bob")
    
    >>> print(undercut([Alice,Bob],items))
    Alice gets ['a', 'd'] with value 9.
    Bob gets ['b', 'c'] with value 10.
    <BLANKLINE>
    >>> Y = A.is_EF({"a","d"}, [{"a","d"},{"b","c"}])
    >>> Y
    True

    >>> Alice = ({"a": 8, "b": 7, "c": 6, "d":3})
    >>> Bob = ({"a": 8, "b": 7, "c": 6, "d":3})
    >>> items=['a','b','c','d']
    >>> A = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Alice")
    >>> B = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Bob")
    >>> print(undercut([Alice, Bob],items))
    There is no envy-free division

    """
    """ Algorithm """

    val=0
    num_agents=len(agents)
    num_of_items=len(items)
    values={0:0,1:0} 
    
    
    logger.info("Checking if there are 0 items")
    if (num_of_items==0 or items==None):
        return no_items(items)

    logger.info("Checking if there is a single item") 
    if num_of_items==1:
        return one_item(agents, items)
    
    logger.info("Stage 1")    
    for group in all_combinations(items, num_agents):
            counter=0
            for item in group:
                for item_ in item:
                    val=values[counter]+ agents[counter][item_]
                    values[counter]=val
                counter+=1
            groupi2=group[0]
            groupi=group[1]
            counter_groupi2=len(groupi2)
            counter_groupi=len(groupi)
            counteri=counter_=0
            val2=val22=0
            for item_ in groupi:
                    val2+=agents[0][item_]    
            for item_ in groupi2:
                    val22+=agents[1][item_]   
            if values[0]>=val2: #Alice weakly prefers X to Y
                for item_ in groupi2: #If any single item is moved from X to Y
                    if values[0]-agents[0][item_]>=val2+agents[0][item_]: #then Alice strictly prefers Y to X
                        break
                    counteri=counteri+1
                if counteri==counter_groupi2:
                    result= almost_equal_cut("Alice",agents, items,values,groupi2,groupi,val22,val2,counter_groupi2,counteri)                               
            else:
                if values[1]>=val22: #George weakly prefers Y to X
                    for item_ in groupi: #If any single item is moved from Y to X
                        if values[1]-agents.__getitem__(1)[item_]>=val22+agents.__getitem__(1)[item_]:  #then George strictly prefers X to Y
                            break
                        counter_=counter_+1 
                    result= almost_equal_cut("George", agents, items,values,groupi,groupi2,val22,val2,counter_groupi,counter_)      
            values={0:0,1:0}  
    return result #If we went through all the possible combinations -> no envy-free division


def almost_equal_cut(Name: str, agents: List[Agent], items: List[Any],values,groupi2,groupi,val22,val2,counter_groupi2,counteri) :
        result="There is no envy-free division"
        logger.info("\t{} is almost-equal-cut for agent Alice (prefers {} to {})".format(group, groupi2,groupi))
        #this partition is presented to George
        if Name=="Alice":
            if values[1]>=val22: #George accepts the partition if he prefers Y to X
                logger.info("Stage 2")  
                result= get_allocation(groupi,groupi2,values)
            else: 
                logger.info("Stage 3")   
                #George rejects the partition if he prefers X to Y
                #check if there exists an item x in X such that George prefers X \ x to Y U x
                result= search_subgroup(agents,groupi2,groupi,val22,val2,values[1])
                
        if Name=="George":
            if values[0]>=val2: #Alice accepts the partition if she prefers X to Y
                logger.info("Stage 2")  
                result= get_allocation(groupi,groupi2,values)
            
            else: 
                logger.info("Stage 3")  
                #Alice rejects the partition if she prefers Y to X
                #check if there exists an item y in Y such that Alice prefers Y \ y to X U y
                result= search_subgroup(agents,groupi,groupi2,val2,val22,values[0]) 
        return result
    
                    
def get_allocation(groupi,groupi2,values):
    temp = []  
    temp2 = []
    logger.info("Bob accepts the offer because he has more benefit from {} than {}".format(groupi,groupi2))
    for ite in groupi:
        temp.append(ite)
    for ite in groupi2:
        temp2.append(ite)
    temp.sort()
    temp2.sort()   
    result=f"Alice gets {temp2} with value {values[0]}.\n"     
    result+=f"Bob gets {temp} with value {values[1]}.\n" 
    logger.info(result)  
    return result

def search_subgroup(agents,groupi2,groupi,val22,val2,values):
    result="There is no envy-free division"
    temp = []  
    temp2 = []
    logger.info("Bob rejects the offer because he has more benefit from {} than {}".format(groupi2,groupi))
    for item_ in groupi2: # check if there exists an item x in X such that: 
        if val22-agents[1][item_]>=values+agents[1][item_]:  # George prefers X \ x to Y U x
            for i in groupi2:
                if  i is not item_:
                    temp.append(i) #George reports X \ x
            for i in groupi: 
                temp2.append(i) #Alice prefers Y U x to X \ x (Since (X,Y) is an almost-equal-cut for Alice).
            temp2.append(item_) #Y U x
            temp.sort()
            temp2.sort()   
            result=f"Alice gets {temp2} with value {val2+agents[0][item_]}.\n"     
            result+=f"Bob gets {temp} with value {val22-agents[1][item_]}.\n"   
            logger.info(result) 
    return result      

def no_items(items: List[Any]):
    result=f"Alice gets {[]} with value {0}.\n"     #if there are no items then value is 0 for everyone
    result+=f"Bob gets {[]} with value {0}.\n"  
    return result 

def one_item(agents: List[Agent], items: List[Any]):
    temp = []  
    temp2 = []
    item_ = items.pop()
    valA_=agents[0][item_]
    valB_=agents[1][item_]  
    if(valA_<=0 and valB_ >=0 ):
        temp2.append(item_)
        result=f"Alice gets {temp} with value {0}.\n"     
        result+=f"Bob gets {temp2} with value {valB_}.\n"  
        logger.info("\tAgent Alice has a benefit of {} from the item which is negative so Bob who does have a benefit of {} from the item gets it".format(valA_, valB_))
        return result
    elif (valA_>=0 and valB_<=0):
        temp.append(item_)
        result=f"Alice gets {temp} with value {valA_}.\n"     
        result+=f"Bob gets {temp2} with value {0}.\n" 
        logger.info("\tAgent Bob has a benefit of {} from the item which is negative so Alice who does have a benefit of {} from the item gets it".format(valB_, valA_))
        return result
    elif (valA_<=0 and valB_<=0):
        result=f"Alice gets {temp} with value {0}.\n"     
        result+=f"Bob gets {temp2} with value {0}.\n" 
        logger.info("\tBoth agents have a negative benefit from the item so no one gets it")
        return result
    else:
        logger.info("\tIf both agents have a positive benefit from the object - there is no envy-free division")
        return "There is no envy-free division"
    
def all_combinations(gr, num_agents):
    """
    Returns all possible combinations of division into 2 groups
    >>> items=['a','b','c','d']
    >>> group_ = all_combinations(items, 2)
    >>> print(group_)
    [[('a',), ('b', 'c', 'd')], [('b',), ('a', 'c', 'd')], [('c',), ('a', 'b', 'd')], [('d',), ('a', 'b', 'c')], [('a', 'b'), ('c', 'd')], [('a', 'c'), ('b', 'd')], [('a', 'd'), ('b', 'c')]]
    """
    n = len(gr)
    groups = [] 
    def generate_partitions(i):
        if i >= n:
            yield list(map(tuple, groups))
        else:
            if n - i > num_agents - len(groups):
                for group in groups:
                    group.append(gr[i])
                    yield from generate_partitions(i + 1)
                    group.pop()
            if len(groups) < num_agents:
                groups.append([gr[i]])
                yield from generate_partitions(i + 1)
                groups.pop()
    result = generate_partitions(0)
    result = [sorted(ps, key = lambda p: (len(p), p)) for ps in result]
    result = sorted(result, key = lambda ps: (*map(len, ps), ps))
    return result

if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

    
 