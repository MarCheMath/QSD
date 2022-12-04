# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 12:37:40 2022

@author: MarChe
"""
import math
import numpy as np


class Graph:       
#    def __init__(self,namelist,colorlist):
#        self.colorlist = np.asarray(colorlist)
#        self.vertexlist = list()
#        for v_n in namelist:
#            v = Graph.Vertex(v_n)
#            self.init_vertex(v)
#            self.vertexlist.append(v)    
#        self.edgelist = list()
#        self.init_Edges()
    
    def __init__(self,vertexlist,edgelist):
        self.colorlist = np.array(range(len(vertexlist)+1))
        self.vertexlist = vertexlist
        self.edgelist = edgelist
        
    def create_complete_Graph(namelist):      
        colornum = len(namelist)
        vertexlist = list()
        for v_n in namelist:
            v = Graph.Vertex(v_n,colornum)
            vertexlist.append(v)  
        for v in vertexlist:
            v.set_adjacent_vertices(vertexlist)
        
        edgelist = list()
        for u in vertexlist:
            for v in vertexlist:
                if not u is v:
                    edgelist.append(Graph.Edge(u,v))
        for edge in edgelist:
            edge.u.edgelist.append(edge)
            edge.v.edgelist.append(edge)
        graph = Graph(vertexlist,edgelist)
        return graph
        
    class Vertex:
        """
        Fields:
            name
            adjacentvertices
            edgelist
            free
        """
        def __init__(self,name,colornum):
            self.name=name
            self.adjacentvertices = list()
            self.edgelist=list()
            self.free = np.array([True]*colornum)
            
        def checkfree(self,color):
            return self.free[color]
        
        def getEdge(self,z):
            for e in self.edgelist:
                if e.u == z or e.v == z:
                    return e            
        
        def set_adjacent_vertices(self,adjacentvertices):
            self.adjacentvertices = adjacentvertices
            
    class Edge:
        def __init__(self,u,v):
            self.u = u
            self.u.adjacentvertices.append(v)
            self.v = v
            self.v.adjacentvertices.append(u)
            self.color = None
                       
    def get_edges_by_color(self):
        pairing = dict()
        for color in self.colorlist:
            pairing[color] = list()
        
        for edge in self.edgelist:
            pairing[edge.color].append(edge)
        return pairing
    
    

class EdgeColoring:
    def __init__(self,names,graph):
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
        while uncolored_Edges:
            e = uncolored_Edges.pop(0)
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
        c = None
        for i_c, c_v in self.graph.colorlist:
            if e.u.free[i_c]:
                c=c_v #less pythonic, but clearer
                break
        d = None
        for i_c, c_v in self.graph.colorlist:
            if (self.fan)[-1].free[i_c]:
                d=c_v #less pythonic, but clearer
                break
#        i_c = np.where(e.u.free)
#        i_d = np.where((self.fan)[-1].free) 
#        c = self.graph.colorlist[i_c]        
#        d = self.graph.colorlist[i_d] 
        return(c,d)
        
    def invert_path(self,u,c,d):    
        edgelist_path = list()
        vertexfan = self.fan[-1]
        seeked_color = d
        current_node = u
        pathnotend = True
        
        while pathnotend:
            current_node, seeked_color,e = EdgeColoring.find_next_color(seeked_color,c,d, current_node)
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
    
    def find_next_color(seeked_color,c,d, current_node):
        for e in current_node.edgelist:
            if e.color == seeked_color:
                next_v = e.u if e.u!=current_node else e.v
                seeked_color = c if seeked_color == d else d
                return (next_v,seeked_color,e)
        return (None,None,False)
        
        
    def rotate_fan(self,u,d):
        for i_vertex in range(len(self.fan)-1):
            vertex = self.fan[i_vertex]
            vertex_plusone = self.fan[i_vertex+1]
            u.getEdge(vertex).color = u.getEdge(vertex_plusone).color
        self.fan[-1].getEdge(u).color = d
        
    def process_output(self):
        self.pairing = self.graph.get_edges_by_color()
        
    def print_round(self,i):
        for e in self.pairing[i]:
            print(e.u.name,e.v.name)
            
names = "Mark, Robert, Tom, Johannes, Birk, Stefan"
ec = EdgeColoring.get_EC_for_complete_graph(names)
ec.do_coloring()
i=0
ec.print_round(i)
        