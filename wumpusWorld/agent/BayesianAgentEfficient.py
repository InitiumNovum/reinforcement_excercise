from wumpusWorld.environment.Agent import *
from wumpusWorld.environment.Percept import *
from wumpusWorld.agent.BayesianAgent import *
import random
import networkx as nx
import math

class BayesianAgentEfficient(BayesianAgent):
    def __init__(self, gridWidth=4, gridHeight=4, dangerThreshold=0.45, allowClimbWithoutGold=True):
        BayesianAgent.__init__(self, gridWidth, gridHeight, dangerThreshold, allowClimbWithoutGold)

    def get_cells_of_equal_danger(self, cells) -> list:
        i = 0
        target_cells = []
        for i in range(len(cells)):
            if cells[i][1] == cells[0][1]:
                target_cells.append(cells[i][0])
            else:
                break
        return target_cells

    def choose_shortest_alternative_path(self, cells, location: Coords):
        path_length = math.inf
        target_cell_choice = None
        for cell in cells:
            available = self.getAvailableCells(cell)
            temp_path = self.getShortestPath(available, location, cell)
            temp_len = len(temp_path)
            if temp_len < path_length:
                path_length = temp_len
                target_cell_choice = cell
        return target_cell_choice

    def find_safest_unexplored_cells(self, potential_cells, pit_beliefs, wumpus_beliefs):
        danger_level = []
        for cell in potential_cells:
            if self.wumpusAlive:
                # without combining the two beleif networks, I simply choose to take the max of the two dangers
                danger_level.append(max(pit_beliefs[cell], wumpus_beliefs[cell]))
            else:
                danger_level.append(pit_beliefs[cell])

        sorted_by_second = sorted(list(zip(potential_cells, danger_level)), key=lambda tup: tup[1])
        if (sorted_by_second[0][1] > self.dangerThreshold) and self.allowClimbWithoutGold:
            equal_danger_cells = [0]
        else:
            equal_danger_cells = self.get_cells_of_equal_danger(sorted_by_second)
        return equal_danger_cells

    def create_next_exploring_actions(self, agent: Agent, percept: Percept, pit_beliefs, wumpus_beliefs):
        """
        actions carried out to explore environment with the least amount of risk.
        """
        selected_nodes = self.get_visted_cells()
        potential_cells = self.get_potential_cells(selected_nodes)
        target_cells = self.find_safest_unexplored_cells(potential_cells, pit_beliefs, wumpus_beliefs)
        target_cell = self.choose_shortest_alternative_path(target_cells, agent.location)
        return self.constructBeelinePlan(agent.location, agent.orientation, target_cell)
