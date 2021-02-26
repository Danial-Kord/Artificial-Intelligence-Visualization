from manim import *
# from manim import *
from manimlib import *
class Node:

    def __init__(self, number,node_color=WHITE):
        self.parent = None
        self.left = None
        self.right = None
        self.number = number


        self.right_edge = None
        self.left_edge = None
        self.visual_shape = Circle()
        self.visual_shape.set_color(node_color)
    def setPos(self,x,y):
        self.x = x
        self.y = y
        self.visual_number = Text(str(self.number))
        self.visual_number.move_to([x, y, 0])
        self.visual_shape.move_to([x, y, 0])
        self.graphics = VGroup(self.visual_number,self.visual_shape)
        


class Graph:
    def __init__(self,root):
        self.root = root
        self.map = {}
        self.map[root] = []
        self.maxIndex=0

    def insert(self,new_node,old_node):
        if not self.map.keys().__contains__(old_node):
            self.map[old_node] = []
        # self.map[old_node].Appened(new_node)
    
    
        