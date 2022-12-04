# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 00:48:05 2022

@author: MarChe
"""
from Graph import Graph
from EdgeColoring import EdgeColoring
from helper_printer import print_plan, print_round
from configuration import NAMES
         
def solve_queer_speeddating(ec):
    ec.do_coloring()
    print_plan(ec)

ec = EdgeColoring.get_EC_for_complete_graph(NAMES)
solve_queer_speeddating(ec)