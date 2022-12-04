# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 00:48:05 2022

@author: MarChe

Speeddating solver. Choose
"""
from typing import Optional
from Graph import Graph
from EdgeColoring import EdgeColoring, print_plan
from CircleMethod import CircleMethod, print_CMRT
import Language
import configuration
if hasattr(configuration,'MODE'):
    mode = configuration.MODE
else:
    mode = None
         
def solve_queer_speeddating_EC(ec:EdgeColoring):
    """
    Solve the problem using the Misra & Gries edge coloring algorithm, effectively modeling the problem as minimal edge coloring. 
    Advantage: Strong support for favoring desired matches. #TODO: implement weak support for desired matches
    Disadvantage: Potentially one round more than necessary, slower.
    Remark: Can solve any graph with an almost optimal number of rounds (either exactly optimal or just 1 higher).
    Args:
        names: single string with names separated by comma
    """
    ec.do_coloring()
    print_plan(ec)

def solve_queer_speeddating_CM(names: str, mode: Optional[str] = None):
    """
    Solve the problem using the circle method for a round table tournament. 
    Advantage: fast solver. 
    Disadvantage: Only weak support for favoring desired matches. #TODO: implement weak support for desired matches
    Args:
        names: single string with names separated by comma
    """
    if mode == "offline":
        cm = CircleMethod(names)
        cm.compute_table()
        print_CMRT(cm)
    elif mode == "online" or mode is None:
        cm = CircleMethod(names)
        cm.online_compute()
    else:
        raise ValueError(Language.errorMessageModeNotImplemented[configuration.LANGUAGE].format(mode))

# ec = EdgeColoring.get_EC_for_complete_graph(NAMES)
# solve_queer_speeddating_EC(ec)

solve_queer_speeddating_CM(configuration.NAMES,mode)