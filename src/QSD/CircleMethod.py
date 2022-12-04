import configuration
from utils import names_to_list
import math
import pandas as pd
import numpy as np
import importlib
import Language

dummy = Language.dummy[configuration.LANGUAGE]

class CircleMethod:
    def __init__(self,names):
        self.names = np.array(names_to_list(names))
        self.permutation = list(range(len(self.names)))
        self.simultaneousMatches = math.floor(len(self.names)/2)
        self.maximal_round = len(self.names)-1 if len(self.names)%2 == 0 else len(self.names)
        self.roundTable = {}
        for round in range(self.maximal_round):
            self.roundTable[round] = {}

    def compute_step(self,round):
        self.roundTable[round] = pd.DataFrame.from_dict(
            {
                "Person A": self.names[self.permutation][:self.simultaneousMatches],
                "Person B": self.names[self.permutation][self.simultaneousMatches:][::-1]
            }
        )
        cut_indices = self.permutation[1:-1]
        self.permutation = [0] + [self.permutation[-1]] + cut_indices
    
    def compute_table(self):
        for round in range(self.maximal_round):
            self.compute_step(round)
    
    def online_compute(self):
        for round in range(self.maximal_round):
            self.compute_step(round)
            print(Language.round_output[configuration.LANGUAGE].format(round+1))
            print(self.roundTable[round])  
            mode = self.input_handler()
            if mode == 'added':
                self.handle_person_added()

    def input_handler(self):
        input()
        importlib.reload(configuration)
        names = names_to_list(configuration.NAMES)
        real_names = len([x for x in names if x != dummy])
        old_real_names = len([x for x in self.names if x != dummy])
        if real_names > old_real_names: #assumes people either leave or join
            self.handle_person_added(names)

    def handle_person_added(self,names):
        added_persons = [x for x in names if x not in self.names]
        if (dummy in self.names) and (dummy not in names):
            first_newcomer = added_persons.pop()
            self.names = list(map(lambda x: x.replace(dummy, first_newcomer), self.names))
        indices_added_persons = list(range(len(self.names),len(names)))
        self.names = np.asarray(list(self.names) + added_persons)
        i_half = int(len(self.names)/2)
        self.permutation = list(self.permutation[:i_half]) + indices_added_persons + list(self.permutation[i_half:])
        self.simultaneousMatches = math.floor(len(self.names)/2)
        self.maximal_round = len(self.names)-1 if len(self.names)%2 == 0 else len(self.names)
        for round in range(len(self.roundTable),self.maximal_round):
            self.roundTable[round] = {}
    

def print_CMRT(cm: CircleMethod):
    for round, table in cm.roundTable.items():
        print(Language.round_output[configuration.LANGUAGE].format(round+1))
        print(table)  