# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 00:48:05 2022

@author: MarChe
"""
import numpy as np
import math
import pandas as pd

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


class EdgeColoring:
    def __init__(self,names: list,graph:Graph):
        self.names = names 
        self.coloring = range(len(self.names))
        self.tables = range(math.ceil(len(self.names)/2))
        self.graph = graph #Graph(self.names,self.coloring)
        
    def get_EC_for_complete_graph(names):
        names = str.split(names,sep=',')
        ec = EdgeColoring(names,Graph.create_complete_Graph(names))
        return ec
    
    def do_coloring(self):
        uncolored_Edges = self.graph.edgelist.copy()
        cl = []
        while uncolored_Edges:
            cl.append(np.sum(~np.isnan(self.graph.color_assignment)))
            if len(cl)>1 and cl[-1]==cl[-2]:
                print(cl[-2])
            e = uncolored_Edges.pop(0)
            u,v = self.graph.get_vertices(e)
            free_color = self.graph.check_vertices_compatible(u,v)
            if not free_color is None:
                self.graph.set_color(e,free_color)
            else:
                self.set_a_maximal_fan(u,v)
                c,d = self.get_free_colors(u)           
                w = self.invert_path(u,c,d)
                self.trim_fan(w)
                self.rotate_fan(u,d)
        self.process_output()
          
        
    def set_a_maximal_fan(self,u,v):
        self.fan = list()
        eligible_nodes = self.graph.get_adjacent_nodes(u)
        
        nf = v
        if nf in eligible_nodes:
            eligible_nodes.remove(nf)
        self.fan.append(nf)

        fan_not_maximal = len(eligible_nodes)>0 #I like this more than implicit list to boolean conversion
        while fan_not_maximal:
            nf = self.get_next_free(eligible_nodes,u,nf)
            if nf is None or len(eligible_nodes)==0: #I like this more than implicit list to boolean conversion
                fan_not_maximal = False
            else:
                self.fan.append(nf)
        
    def get_next_free(self,vertex_list,u,nf):
        to_remove = []
        for i_x,v in enumerate(vertex_list): 
            potential_d = self.graph.get_color(self.graph.get_edge(u,v))
            if np.isnan(potential_d):
                to_remove.append(v)
                #self.graph.set_color(self.graph.get_edge(u,v),self.graph.check_vertices_compatible(u,v)) #faster
            elif not self.graph.color_onehot[nf,potential_d]:
                for v_to_remove in to_remove:
                    if v_to_remove in vertex_list:
                        vertex_list.remove(v_to_remove)
                return vertex_list.pop(i_x)
        
    def get_free_colors(self,u):
        v_d = self.fan[-1]
        c = self.get_free_color(u)
        d = self.get_free_color(v_d)
        return(c,d)
    
    def get_free_color(self,vertex):
        for c in range(self.graph.max_color):
            if not self.graph.color_onehot[vertex,c]:
                break
        return c       
        
    def invert_path(self,u,c,d):    
        edgelist_path = list()
        vertexfan = self.fan[-1]
        seeked_color = d
        current_node = u
        pathnotend = True
        
        while pathnotend:
            current_node, seeked_color,e = self.find_next_color(seeked_color,c,d, current_node)
            if e:
                if e in edgelist_path:
                    pathnotend = False
                else:
                    edgelist_path.append(e)
                    if current_node in self.fan:
                        vertexfan = current_node
            else:
                pathnotend = False
        
        for e in edgelist_path:
            color_to_assign = c if self.graph.get_color(e) == d else d
            self.graph.set_color(e,color_to_assign)
        
        return vertexfan

    def trim_fan(self,vertexfan):
        trimed_fan = list()
        add = True
        for v in self.fan:
            if add:                
                trimed_fan.append(v)
                if v==vertexfan:
                    add = False
                    break
        self.fan = trimed_fan
    
    def find_next_color(self,seeked_color,c,d, current_node):
        for v in self.graph.get_adjacent_nodes(current_node):
            e = self.graph.get_edge(current_node,v)
            if self.graph.get_color(e) == seeked_color:
                next_v = v
                seeked_color = c if seeked_color == d else d
                return (next_v,seeked_color,e)
        return (None,None,False)
        
        
    def rotate_fan(self,u,d):
        for i_vertex in range(len(self.fan)-1):
            vertex = self.fan[i_vertex]
            vertex_plusone = self.fan[i_vertex+1]
            e_uv = self.graph.get_edge(u,vertex)
            e_uvplus = self.graph.get_edge(u,vertex_plusone)
            self.graph.set_color(e_uv,self.graph.get_color(e_uvplus))
        e_fanu = self.graph.get_edge(self.fan[-1],u)
        self.graph.set_color(e_fanu,d)
        
    def process_output(self):
        self.pairing = self.graph.get_edges_by_color()
        
    def set_table(self):
        self.table = {}
        for round, edges in self.pairing.items():
            name_list = {"Person A" : [], "Person B": []}
            for edge in edges:
                name_1,name_2 = self.graph.get_names_from_edge(edge)
                name_list["Person A"].append(name_1)
                name_list["Person B"].append(name_2)
            self.table[round] = pd.DataFrame.from_dict(name_list)

    def print_round(self,i):
        for e in self.pairing[i]:
            print(self.graph.get_names_from_edge(e))
    
    def print_plan(self):
        self.set_table()
        for i in range(self.graph.max_color):
            print("############## Round {} ##############".format(i))
            print(self.table[i])
            

names = "Mark, Robert, Tom, Johannes, Birk, Stefan, Ole, Aaron"
ec = EdgeColoring.get_EC_for_complete_graph(names)
ec.do_coloring()
ec.print_plan()
