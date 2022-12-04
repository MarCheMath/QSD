def print_round(ec,i):
    for e in ec.pairing[i]:
        print(ec.graph.get_names_from_edge(e))

def print_plan(ec):
    ec.set_table()
    for i in range(ec.graph.max_color):
        print("############## Round {} ##############".format(i))
        print(ec.table[i])