import copy
from manim import *
import codecs
import random

from numpy import cos
# from manimlib import *

RANDOM_POSITINAL_ENABLE = True
POSITIONAL_RANDOMNESS = 0.2
RANDOM_PRECESION = 1000
y_bias = 3


class Node:

    def __init__(self, name,scale,width = 5,node_color=WHITE):
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
        self.random_index = 0
        self.dad = None
        self.arrow = None
        self.visual_shape.set_stroke(width=width,color=BLUE)
        self.visual_shape.set_color(node_color)
        self.H = 0
        self.calculated_cost = 0
        self.visual_calculated_cost = None

        self.seen = False
    def set_pos(self,x,y):
        self.x = x
        self.y = y
        self.visual_name = Text(str(self.name))
        self.visual_name.move_to([x, y, 0])
        self.visual_shape.move_to([x, y, 0])
        self.graphics = VGroup(self.visual_name,self.visual_shape)
        self.visual_name.scale(self.scale)
        self.visual_shape.scale(self.scale)

    def set_dad(self,node,arrow):
        self.dad = node
        self.arrow = arrow

    def set_huristic(self,cost):
        self.H = cost

    def set_calculated_cost(self,cost):
        self.calculated_cost = cost


class Graph:
    def __init__(self,scale,root = None):
        self.root = root
        self.scale = scale
        self.map = {}
        self.nodes = {}
        self.edges = {} # exp: {(A,B):2}
        self.visual_edges = {}
        self.has_cost = False
        if root is not None:
            self.map[root] = []

    def insert(self,new_node,old_node,No_duplicate = False):
        if not self.map.keys().__contains__(old_node):
            self.map[old_node] = []
        if not (self.map[old_node]).__contains__(new_node):
            (self.map[old_node]).append(new_node)
        if new_node.depth == 0:
            new_node.depth = old_node.depth+1
            new_node.order = self.branching_factors[new_node.depth]
            self.branching_factors[new_node.depth]+=1
        elif No_duplicate:
            new_node = copy.deepcopy(new_node)
            new_node.depth = old_node.depth+1
            new_node.order = self.branching_factors[new_node.depth]
            self.branching_factors[new_node.depth]+=1 
        new_node.parent = old_node
            
    def add_edge_cost(self,from_node,to_node,cost):
        self.edges[from_node,to_node] = cost
        return
    
    def read_from_file(self,path):
        with codecs.open(path, 'r') as f:
            Lines = f.readlines()
            max_depth = int(Lines[0].split(" ")[0])
            self.branching_factors = []
            for i in range(max_depth*2+1):
                self.branching_factors.append(0)

            all_nodes = Lines[1].split(" ")
            all_nodes[len(all_nodes) -1] = all_nodes[len(all_nodes) -1].replace("\n","")

            for j in range(0,len(all_nodes)):
                self.nodes[all_nodes[j]] = Node(all_nodes[j],self.scale)
                self.nodes[all_nodes[j]].random_index = random.randint(10,2000)
            self.root = self.nodes[all_nodes[0]]
            # adding links between nodes
            index = 0
            for i in range(2,len(Lines)):
                links = Lines[i].split(" ")
                links[len(links) -1] = links[len(links) -1].replace("\n","")
                for j in range(1,len(links)):
                    self.insert(self.nodes[links[j]],self.nodes[links[0]])

    def read_from_file_with_edge_costs(self,path):
        self.has_cost = True
        with codecs.open(path, 'r') as f:
            Lines = f.readlines()
            max_depth = int(Lines[0].split(" ")[0])
            self.branching_factors = []
            for i in range(max_depth*2+1):
                self.branching_factors.append(0)

            # adding nodes with hiuristic
            all_nodes = Lines[1].split(" ")
            Hiuristics = Lines[2].split(" ")
            Hiuristics[len(Hiuristics) -1] = Hiuristics[len(Hiuristics) -1].replace("\n","")
            all_nodes[len(all_nodes) -1] = all_nodes[len(all_nodes) -1].replace("\n","")

            for j in range(0,len(all_nodes)):
                self.nodes[all_nodes[j]] = Node(all_nodes[j],self.scale)
                self.nodes[all_nodes[j]].random_index = random.randint(10,2000)
                self.nodes[all_nodes[j]].set_huristic(int(Hiuristics[j]))
            self.root = self.nodes[all_nodes[0]]

            # adding links between nodes with edge values
            index = 0
            for i in range(3,len(Lines),2):
                links = Lines[i].split(" ")
                edges = Lines[i + 1].split(" ")
                edges[len(edges) -1] = edges[len(edges) -1].replace("\n","")
                links[len(links) -1] = links[len(links) -1].replace("\n","")
                for j in range(1,len(links)):
                    self.insert(self.nodes[links[j]],self.nodes[links[0]])
                    self.add_edge_cost(self.nodes[links[0]],self.nodes[links[j]],int(edges[j-1]))
                    
        

    def show_complete_graph(self,scene,RIGHT_X_AREA,LEFT_X_AREA):
            group = VGroup()
            # adding nodes
            for i in self.nodes:
                node = self.nodes[i]
                current_y_point = y_bias - (self.scale*2 + self.scale) * node.depth

                current_x_point = (RIGHT_X_AREA + LEFT_X_AREA)/2
                if self.branching_factors[node.depth] > 1:
                    current_x_point = LEFT_X_AREA + ((RIGHT_X_AREA - LEFT_X_AREA) / (self.branching_factors[node.depth]-1))*node.order
                    if RANDOM_POSITINAL_ENABLE:
                        # random.seed(node.random_index)
                        current_x_point += (float(random.randint(-RANDOM_PRECESION*POSITIONAL_RANDOMNESS,RANDOM_PRECESION*POSITIONAL_RANDOMNESS))) / (RANDOM_PRECESION)
                node.set_pos(current_x_point,current_y_point)
                group.add(node.graphics)
                # scene.add(node.graphics)

            # scene.add(node.graphics)
            
            # adding edges
            for i in self.map:
                nodes = self.map[i]
                for j in nodes:
                    arrow = Line([i.x,i.y,0],[j.x,j.y,0],stroke_width=1,buff= self.scale)
                    group.add(arrow)
                    if self.has_cost:
                        cost = Tex(str(self.edges[i,j]))
                        self.visual_edges[i,j] = cost
                        cost.scale(self.scale)
                        
                        a = ( float(i.y - j.y) / float(i.x - j.x) )
                        if a == 0:
                            a = 0.000000000001
                        vertical_perpendicular = -1.0 / a
                        center = (np.array([i.x,i.y,0]) + np.array([j.x,j.y,0])) / 2
                        target_point = np.array([center[0]+1,(center[0]+1.0)*vertical_perpendicular + (center[1] - (center[0]*vertical_perpendicular)),0])
                        
                        vector = np.array(target_point - center)
                        vector = normalize(vector)
                        
                        # temp = Line(center,target_point,stroke_width=1)
                        cost.move_to(center)
                        cost.shift(vector*0.2)
                        group.add(cost)
                        # group.add(temp)

                    # scene.add(arrow)
            return group
    
    def make_nodes_connected_bi_directional(self):
        repeat = True
        map = self.map
        while(repeat):
            try:
                repeat = False
                for i in map:
                    dad = i
                    for j in map[i]:
                        son = j
                        for d in map:
                            for q in map[d]:
                                if q == son and d.name != dad.name:
                                    clone = copy.deepcopy(q)
                                    clone.depth = 0
                                    map[d].remove(q)
                                    self.insert(clone,d)
                                    repeat = True
                                    for x,z in self.edges:
                                        if x.name == d.name and z.name == q.name:
                                            self.add_edge_cost(d,clone,self.edges[x,z])
                                            break

            except:
                print("cleaning")
        map = copy.deepcopy(self.map)
        index = 1
        for i in map:
            for j in map[i]:
                check = True
                if map.keys().__contains__(j) and (map[j]).__contains__(i):
                    check = False
                if check:
                    original = self.nodes[j.name]
                                        
                    node = copy.deepcopy(i)
                    node.depth = 0
                    self.nodes[node.name + str(index)] = node
                    index+=1
                    # node.graphics = j.graphics
                    # node.visual_shape = j.visual_shape
                    # node.visual_name = j.visual_name
                    self.insert(node,original)
                    print("  " + i.name+"   " + original.name)
                    for x,z in self.edges:
                        if x.name == node.name and z.name == original.name:
                            print("we did it" + "  " + original.name+"   " + node.name)
                            self.add_edge_cost(original,node,self.edges[x,z])
                            break
        self.graph_cleaner()
    
    def graph_cleaner(self):
        map = self.map
        for i in map:
            for j in map[i]:
                order = j.order
                depth = j.depth
                parent_order = j.parent.order
                for k in map:
                    for l in map[k]:
                        if l.depth == depth:
                            if l.parent is not None and l.parent.order > parent_order and l.order < order:
                                j.order -= 1
                                l.order += 1







                    


    def get_node_relative_pos(self,node,RIGHT_X_AREA,LEFT_X_AREA):
         return self.get_node_relative_pos2(self.branching_factors[node.depth],node.order,node.depth,RIGHT_X_AREA,LEFT_X_AREA)

    def get_node_relative_pos2(self,branching_factor,order,depth,RIGHT_X_AREA,LEFT_X_AREA):
        current_y_point = float(y_bias - (self.scale*2 + self.scale) * depth)

        current_x_point = (RIGHT_X_AREA + LEFT_X_AREA)/2
        if branching_factor > 1:
            current_x_point = float(LEFT_X_AREA + ((RIGHT_X_AREA - LEFT_X_AREA) / (branching_factor-1))*order)
            if RANDOM_POSITINAL_ENABLE:
                # random.seed(node.random_index)
                current_x_point += (float(random.randint(-RANDOM_PRECESION*POSITIONAL_RANDOMNESS,RANDOM_PRECESION*POSITIONAL_RANDOMNESS))) / (RANDOM_PRECESION)
        return [current_x_point,current_y_point,0]

    def set_node_cost_tex(self,cost_tex):
        self.cost_tex = cost_tex