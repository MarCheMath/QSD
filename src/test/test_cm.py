import pytest
from CircleMethod import CircleMethod, print_CMRT

def get_names_from_table(assignments):
    return assignments[list(assignments.keys())[0]]["Person A"] + assignments[list(assignments.keys())[0]]["Person B"]

@pytest.fixture(name='names')
def get_names():
    names = """
    Mark
    Robert
    Tom
    Johannes
    Birk
    Stefan
    Ole
    Aaron
    Simon
    Malte
    """
    return names

@pytest.fixture(name='assigments')
def get_assignments(names):
        cm = CircleMethod(names)
        cm.compute_table()
        print_CMRT(cm)

def test_check_table(assignments):
    names = get_names_from_table(assignments)
    check_assignment = {}
    for name in names:
        check_assignment[name] = []

    for round, table in assignments.items():
        for idx in range(len(table)):
            assignment = table.iloc[idx]
            if assignment["Person B"] in check_assignment[assignment["Person A"]]:
                print("round {} has to {} the second assignment of {}".format(round,assignment["Person A"],assignment["Person B"])) 
            check_assignment[assignment["Person A"]].append(assignment["Person B"])
            check_assignment[assignment["Person B"]].append(assignment["Person A"])
    
    for person, assignment_list in check_assignment.items():
        assert len(list(set(assignment_list))) == len(assignment_list)
