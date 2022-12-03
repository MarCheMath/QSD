# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 12:37:40 2022

@author: MarChe
"""
import math
import numpy as np


class graph:       
    def __init__(self,namelist,colorlist):
        self.colorlist = np.asarray(colorlist)
        self.vertexlist = list()
        for v_n in namelist:
            v = graph.vertex(v_n)
            self.init_vertex(v)
            self.vertexlist.append(v)    
        self.edgelist = list()
        self.init_edges()
        
    class vertex:
        def __init__(self,name):
            self.name=name
            self.adjacentvertices = list()
            self.edgelist=list()
            
        def checkfree(self,color):
            return self.free[color]
        
        def getedge(self,z):
            for e in self.edgelist:
                if e.u == z or e.v == z:
                    return e
    class edge:
        def __init__(self,u,v):
            self.u = u
            self.u.adjacentvertices.append(v)
            self.v = v
            self.v.adjacentvertices.append(u)
            self.color = None
        
    def init_vertex(self,v):
        v.free = [None]*len(self.colorlist)
        for color in self.colorlist:
            v.free[color] = True
        #v.edgelist = [x for x in self.vertexlist if x!=v]
        
    def init_edges(self):
        for i_u in range(len(self.vertexlist)):
            u = self.vertexlist[i_u]
            for i_v in range(i_u,len(self.vertexlist)):
                v= self.vertexlist[i_v]
                v.edgelist.append(graph.edge(u,v))
                
    def get_edges_by_color(self):
        pairing = dict()
        for color in self.colorlist:
            pairing[color] = list()
        
        for edge in self.edgelist:
            pairing[color].append(edge)
        return pairing
    
    

class edgeColoring:
    def __init__(self,names):
        self.names = str.split(names,sep=',')
        self.coloring = range(len(self.names))
        self.tables = range(math.ceil(len(self.names)/2))
        self.graph = graph(self.names,self.coloring)
        
    def construct_graph(self):    
        self.graph = dict()
        for name in self.names:
           self.graph[name]=graph.vertex()
    
    def do_coloring(self):
        uncolored_edges = self.graph.edgelist.copy()
        while uncolored_edges:
            e = uncolored_edges.pop(0)
            self.set_a_maximal_fan(e.u,e.v)
            c,d = self.get_free_colors(e)           
            w = self.invert_path(e.u,c,d)
            self.trim_fan(w)
            self.rotate_fan(e.u,d)
        self.process_output()
          
        
    def set_a_maximal_fan(self,u,v):
        self.fan = list()
        eligible_nodes = [x for x in u.adjacentvertices if x!=v]
        
        nf = v
        self.fan.append(nf)
        
        while eligible_nodes:
            nf = self.get_next_free(eligible_nodes,nf)
            self.fan.append(nf)
        
    def get_next_free(self,vertex_list, v):
        for i_x in range(len(vertex_list)):
            x = vertex_list[i_x]
            for color in self.graph.colorlist[v.free]:
                if x.checkfree(color):
                    return vertex_list.pop(i_x)
        
    def get_free_colors(self, e):
        i_c = np.where(e.u.free)
        i_d = np.where((self.fan)[-1].free) 
        c = self.graph.colorlist[i_c]        
        d = self.graph.colorlist[i_d] 
        return(c,d)
        
    def invert_path(self,u,c,d):    
        edgelist_path = list()
        vertexfan = self.fan[-1]
        current_color = d
        current_node = u
        pathnotend = True
        
        while pathnotend:
            current_node, current_color,e = edgeColoring.find_next_color(current_color,c,d, current_node)
            if e:
                edgelist_path.append(e)
                if current_node in self.fan:
                    vertexfan = current_node
            else:
                pathnotend = False
        
        for e in edgelist_path:
            e.color = c if e.color == d else d
        
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
    
    def find_next_color(current_color,c,d, current_node):
        for e in current_node.edgelist:
            if e.color == current_color:
                next_v = e[0] if e[0]!=current_node else e[1]
                current_color = c if current_color == d else d
                return (next_v,current_color,e)
        return (None,None,False)
        
        
    def rotate_fan(self,u,d):
        for i_vertex in range(len(self.fan)-1):
            vertex = self.fan[i_vertex]
            vertex_plusone = self.fan[i_vertex+1]
            u.getedge(vertex).color = u.getedge(vertex_plusone).color
            
        self.fan[-1].getedge(u).color = d
        
    def process_output(self):
        self.pairing = self.graph.get_edges_by_color()
        
    def print_round(self,i):
        for e in self.pairing[i]:
            print(e.u.name,e.v.name)
            
names = "Mark, Robert, Tom, Johannes, Birk, Stefan"
ec = edgeColoring(names)
ec.do_coloring()
i=0
ec.print_round(i)
        