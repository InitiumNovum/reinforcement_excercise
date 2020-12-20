from wumpusWorld.environment.Environment import *
import random
import networkx as nx

class NavigationMixin:
    @staticmethod
    def create_node_list(gridWidth, gridHeight):
        node_list = []
        for j in range(gridHeight):
            for i in range(gridWidth):
                ladder = (i == 0) and (j == 0)
                node_list.append((i + j * gridWidth, {"x": i,
                                                      "y": j,
                                                      "current_location": False,  # added to make compatible with DeepQ
                                                      "stench": None,
                                                      "breeze": None,
                                                      "glitter": None,
                                                      "ladder": ladder,
                                                      "visited": False}))
        return node_list

    @staticmethod
    def create_edge_list(gridWidth, gridHeight):
        edge_list = []
        for j in range(gridHeight):
            for i in range(gridWidth):
                if i < gridWidth - 1:
                    edge_list.append((i + j * gridWidth, i + 1 + j * gridWidth))
                if j < gridHeight - 1:
                    edge_list.append((i + j * gridWidth, i + (j + 1) * gridWidth))
        return edge_list

    @staticmethod
    def get_direction_angle(direction):
        if direction == (1, 0):
            angle = 0
        elif direction == (-1, 0):
            angle = 180
        elif direction == (0, -1):
            angle = 270
        elif direction == (0, 1):
            angle = 90
        else:
            raise ValueError("invalid direction")

        return angle

    @staticmethod
    def get_direction_conversion(direction):
        if direction == (1, 0):
            angle = 'East'
        elif direction == (-1, 0):
            angle = 'West'
        elif direction == (0, -1):
            angle = 'South'
        elif direction == (0, 1):
            angle = 'North'
        else:
            raise ValueError("invalid direction")

        return angle

    @staticmethod
    def construct_orientation_graph():
        angle_list = []
        edge_list = []
        angle_list.append((0, {"angle":0,
                               "direction":(1,0),
                               "direction2":'East',
                                "current_angle":True}))
        angle_list.append((1, {"angle":90,
                               "direction":(0,1),
                               "direction2":'North',
                                "current_angle":False}))
        angle_list.append((2, {"angle":180,
                               "direction":(-1,0),
                               "direction2":'West',
                                "current_angle":False}))
        angle_list.append((3, {"angle":270,
                               "direction":(0,-1),
                               "direction2":'South',
                                "current_angle":False}))
        edge_list = [(0,1), (1,2), (2,3), (3,0)]

        AngG = nx.Graph()
        AngG.add_nodes_from(angle_list)
        AngG.add_edges_from(edge_list)
        return AngG

    def get_source_and_target(self, source, target):
        for node in self.AngG.nodes():
            if self.AngG.nodes()[node]['direction2'] == source:
                source_i = node
            if self.AngG.nodes()[node]['direction'] == target:
                target_i = node
        return source_i, target_i

    @staticmethod
    def turn_direction(path):
        turns = []
        for i in range(len(path)-1):
            if path[i+1] - path[i] == 3:
                turns.append(TurnRight())
            elif path[i+1] - path[i] == -3:
                turns.append(TurnLeft())
            elif path[i+1] - path[i] == 1:
                turns.append(TurnLeft())
            elif path[i+1] - path[i] == -1:
                turns.append(TurnRight())
        return turns

    def get_turns_and_direction(self, step, orientation):
        source = orientation
        target = step
        source_i, target_i = self.get_source_and_target(source, target)
        path = nx.shortest_path(self.AngG, source_i, target_i)
        turn = self.AngG.subgraph(path)
        return self.turn_direction(path), NavigationMixin.get_direction_conversion(target)

