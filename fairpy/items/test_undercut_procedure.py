#!python3
"""
Implementing the algorithm in the following article: "A note on the undercut procedure"
By Haris Aziz
2014
Link to the article: https://arxiv.org/pdf/1312.6444.pdf
Programmer: Helen Yonas
Date: 2022-05
The undercut procedure is a procedure for fair item assignment between *two* people.
"""

from fairpy.items.undercut_procedure  import undercut
from fairpy.allocations import Allocation
import unittest
import fairpy


class TestAlgo(unittest.TestCase):
    def setUp(self):
        self.allocation={}
        
    def test_normal_cases(self):
        
        
        Alice = fairpy.agents.AdditiveAgent({"a": 7, "b": 4, "c": 3, "d":2}, name="Alice")
        Bob = fairpy.agents.AdditiveAgent({"a": 1, "b": 7, "c": 3, "d":2}, name="Bob")
        items=['a','b','c','d']
        allocation1 = undercut([Alice,Bob],items)
        allocation2 =  Allocation([Alice,Bob],[['a','d'],['b','c']])
        self.assertEqual(allocation1.str_with_values(),allocation2.str_with_values())
        
        
        agents_dict = {"Alice":{"a": 8, "b": 7, "c": 6, "d":3},"George":{"a": 8, "b": 7, "c": 6, "d":3}}
        allocation = undercut(agents_dict,items)
        self.assertEqual(allocation, "There is no envy-free division")
    

    def test_special_cases(self):
        
        #no objects
        Alex = fairpy.agents.AdditiveAgent({}, name="Alex")
        George = fairpy.agents.AdditiveAgent({}, name="George")
        allocation = undercut([Alex,George],[])
        allocation2 =  Allocation([Alex,George],[[],[]])
        self.assertEqual(allocation.str_with_values(),allocation2.str_with_values())
        
        #same values
        agents_dict = {"Alice":{"a": 4, "b": 4, "c": 4, "d":4},"Bob":{"a": 4, "b": 4, "c": 4, "d":4}}
        bundles = {"Alice": {'a', 'd'}, "Bob":{'b', 'c'}}
        allocation = undercut(agents_dict,['a','b','c','d'])
        allocation2 =  Allocation(agents_dict,bundles)
        self.assertEqual(allocation.str_with_values(),allocation2.str_with_values())
        
        
        Alice = fairpy.agents.AdditiveAgent({"a": 1,"b": 2, "c": 3, "d":4,"e": 5, "f":14}, name="Alice")
        Bob = fairpy.agents.AdditiveAgent({"a":1,"b": 1, "c": 1, "d":1,"e": 1, "f":7}, name="Bob")
        allocation = undercut([Alice,Bob],['a','b','c','d','e','f'])  
        allocation2 = Allocation([Alice,Bob],[['a','b','c','d','e'],['f']])  
        self.assertEqual(allocation.str_with_values(), allocation2.str_with_values())
        
        #no allocation
        A = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Bob")
        allocation = undercut([A,B],['a','b','c','d'])
        self.assertEqual(allocation, "There is no envy-free division")

    def test_envy_free(self):
      
        A = fairpy.agents.AdditiveAgent({"a": 7, "b": 4, "c": 3, "d":2}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": 1, "b": 7, "c": 3, "d":2}, name="Bob")
        allocation = undercut([A,B],['a','b','c','d'])  
        self.assertTrue(A.is_EF(allocation[0],allocation)) and B.is_EF(allocation[1], allocation)

        A = fairpy.agents.AdditiveAgent({"a": 7, "b": 4, "c": 3, "d":2}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": 7, "b": 1, "c": 3, "d":2}, name="Bob")
        allocation = undercut([A,B],['a','b','c','d'])  
        self.assertTrue(A.is_EF(allocation[0],allocation)) and B.is_EF(allocation[1], allocation)

        A = fairpy.agents.AdditiveAgent({"a": 5, "b": 5, "c": 5, "d":5}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": 5, "b": 5, "c": 5, "d":5}, name="Bob")
        allocation = undercut([A,B],['a','b','c','d'])  
        self.assertTrue(A.is_EF(allocation[0],allocation) and B.is_EF(allocation[1], allocation))

        A = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Bob")
        self.assertFalse(A.is_EF({"a","b"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}]) and B.is_EF({"d","c"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}]))
        self.assertFalse(B.is_EF({"a","c"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}]) and  A.is_EF({"b","d"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}]))

        A = fairpy.agents.AdditiveAgent({"a": 5}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": -4}, name="Bob")
        allocation = undercut([A,B],['a'])  
        self.assertTrue(A.is_EF(allocation[0],allocation) and B.is_EF(allocation[1], allocation))


        A = fairpy.agents.AdditiveAgent({}, name="Alice")
        B = fairpy.agents.AdditiveAgent({}, name="Bob")
        allocation = undercut([A,B],[])  
        self.assertTrue(A.is_EF(allocation[0],allocation) and B.is_EF(allocation[1], allocation))


if __name__ == '__main__':
    unittest.main()