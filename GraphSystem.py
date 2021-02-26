from logging import root
from manim import *
import codecs
# from manimlib import *
class Node:

    def __init__(self, name,scale,node_color=WHITE):
        self.parent = None
        self.left = None
        self.right = None
        self.name = name
        self.right_edge = None
        self.left_edge = None
        self.visual_shape = Circle()
        self.scale = scale
        self.depth = 0
        self.order = 0
        self.visual_shape.set_color(node_color)
    def set_pos(self,x,y):
        self.x = x
        self.y = y
        self.visual_name = Text(str(self.name))
        self.visual_name.move_to([x, y, 0])
        self.visual_shape.move_to([x, y, 0])
        self.graphics = VGroup(self.visual_name,self.visual_shape)
        self.visual_name.scale(self.scale)
        self.visual_shape.scale(self.scale)
        


class Graph:
    def __init__(self,scale,root = None):
        self.root = root
        self.scale = scale
        self.map = {}
        self.nodes = {}
        if root is not None:
            self.map[root] = []

    def insert(self,new_node,old_node):
        if not self.map.keys().__contains__(old_node):
            self.map[old_node] = []
        (self.map[old_node]).append(new_node)
        new_node.depth = old_node.depth+1
        new_node.order = self.branching_factors[new_node.depth]
        self.branching_factors[new_node.depth]+=1
    
    def read_from_file(self,path):
        with codecs.open(path, 'r') as f:
            Lines = f.readlines()
            max_depth = int(Lines[0].split(" ")[0])
            self.branching_factors = []
            for i in range(max_depth):
                self.branching_factors.append(0)

            all_nodes = Lines[1].split(" ")
            all_nodes[len(all_nodes) -1] = all_nodes[len(all_nodes) -1].replace("\n","")

            for j in range(0,len(all_nodes)):
                self.nodes[all_nodes[j]] = Node(all_nodes[j],self.scale)
            self.root = self.nodes[all_nodes[0]]
            # adding links between nodes
            index = 0
            for i in range(2,len(Lines)):
                links = Lines[i].split(" ")
                links[len(links) -1] = links[len(links) -1].replace("\n","")
                for j in range(1,len(links)):
                    self.insert(self.nodes[links[j]],self.nodes[links[0]])
    
    def show_complete_graph(self,scene,RIGHT_X_AREA,LEFT_X_AREA):
            y_bias = 3
            group = VGroup()
            # adding nodes
            for i in self.nodes:
                node = self.nodes[i]
                current_y_point = y_bias - (self.scale*2 + self.scale) * node.depth

                current_x_point = (RIGHT_X_AREA + LEFT_X_AREA)/2
                if self.branching_factors[node.depth] > 1:
                    current_x_point = LEFT_X_AREA + ((RIGHT_X_AREA - LEFT_X_AREA) / (self.branching_factors[node.depth]-1))*node.order
                
                node.set_pos(current_x_point,current_y_point)
                group.add(node.graphics)
                scene.add(node.graphics)

            scene.add(node.graphics)
            
            # adding edges
            for i in self.map:
                nodes = self.map[i]
                for j in nodes:
                    arrow = Arrow([i.x,i.y,0],[j.x,j.y,0],stroke_width=1,buff= self.scale)
                    group.add(arrow)
                    scene.add(arrow)
            return group
    
    def get_node_relative_pos(self,node,RIGHT_X_AREA,LEFT_X_AREA):
        y_bias = 3
        current_y_point = float(y_bias - (self.scale*2 + self.scale) * node.depth)

        current_x_point = (RIGHT_X_AREA + LEFT_X_AREA)/2
        if self.branching_factors[node.depth] > 1:
            current_x_point = float(LEFT_X_AREA + ((RIGHT_X_AREA - LEFT_X_AREA) / (self.branching_factors[node.depth]-1))*node.order)
        return [current_x_point,current_y_point,0]