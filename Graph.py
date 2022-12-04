import numpy as np

class Graph:
    def __init__(self,namelist,edgematrix):
        self.namelist = namelist
        self.vertices = list(range(edgematrix.shape[0]))
        self.edgelist = np.where(edgematrix.flatten())[0].tolist()
        self.max_color = np.max(np.sum(edgematrix,axis=0))+1
        self.edgematrix = edgematrix
        self.color_onehot = np.full((len(self.vertices),self.max_color),False)
        self.color_assignment = [np.NaN]*(self.edgematrix.shape[0]*self.edgematrix.shape[1])
        
        
    def create_complete_Graph(namelist):      
        num_names = len(namelist)
        edgematrix = np.full((num_names,num_names),True)
        edgematrix = ~np.tril(edgematrix)
        graph = Graph(namelist,edgematrix)
        return graph
    
    def get_adjacent_nodes(self,v):
        adjacent_nodes = np.where(self.edgematrix[v,:])[0]
        return adjacent_nodes.tolist()
    
    def get_edge(self,u,v):
        if u < v:
            return len(self.vertices)*u+v
        else:
            return len(self.vertices)*v+u
    
    def get_vertices(self,e):
        u = e//len(self.vertices)
        v = e%len(self.vertices)
        return (u,v)
    
    def get_edges_by_color(self):
        pairing = dict()
        for color in range(self.max_color):
            pairing[color] = list()
        
        for edge in self.edgelist:
            pairing[self.get_color(edge)].append(edge)
        return pairing
        
    def get_names_from_edge(self,e):
        persons = self.get_vertices(e)
        name_A = self.namelist[persons[0]]
        name_B = self.namelist[persons[1]]
        return (name_A,name_B)

    def set_color(self,edge,color):
        vertex_1,vertex_2 = self.get_vertices(edge)
        old_color = self.get_color(edge)
        self.update_vertices(vertex_1,vertex_2,old_color,False)
        self.color_assignment[edge] = color
        self.update_vertices(vertex_1,vertex_2,color,True)
    
    def update_vertices(self,vertex_1, vertex_2,color,to_assign):
        if not np.isnan(color):
            self.color_onehot[vertex_1,color] = to_assign
            self.color_onehot[vertex_2,color] = to_assign

    def get_color(self,edge):
        return self.color_assignment[edge]

    def check_vertices_compatible(self,v1,v2):
        free_colors = np.where(~np.logical_or(self.color_onehot[v1,:], self.color_onehot[v2,:]))[0]
        if len(free_colors)==0:
            return None
        else:
            return free_colors[0]