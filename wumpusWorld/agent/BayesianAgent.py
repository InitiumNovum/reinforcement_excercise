from wumpusWorld.environment.Agent import *
from wumpusWorld.environment.Percept import *
from wumpusWorld.agent.BeelineAgent import *
import random
import networkx as nx
import math

class BayesianAgent(BeelineAgent):
    def __init__(self, gridWidth=4, gridHeight=4, dangerThreshold=0.45, allowClimbWithoutGold=True):
        BeelineAgent.__init__(self, gridWidth, gridHeight)
        if gridWidth != 4 and gridHeight != 4:
            raise ValueError("nothing except 4x4 grids work at the moment!!")
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        #TODO make a breeze and stench obervations generator that accounts for different grid sizes.
        self.breeze_observations = [[None, None, None, None,
                                None, None, None, None,
                                None, None, None, None,
                                None, None, None, None,
                                None, None, None, None,
                                None, None, None, None,
                                None, None, None, None,
                                None, None, None, None]]
        self.stench_observations = [[None,
                                None, None, None, None,
                                None, None, None, None,
                                None, None, None, None,
                                None, None, None, None,
                                None, None, None, None,
                                None, None, None, None,
                                None, None, None, None,
                                None, None, None, None]]
        self.action_list = []
        self.G = nx.Graph()
        self.G.add_nodes_from(BayesianAgent.create_node_list(self.gridWidth, gridHeight))
        self.G.add_edges_from(BayesianAgent.create_edge_list(self.gridWidth, gridHeight))
        self.G.nodes()[0]['visited'] = True # initialize graph with first cell already visited
        self.AngG = self.construct_orientation_graph()
        self.count = -1
        self.wumpusAlive = True
        self.allowClimbWithoutGold = allowClimbWithoutGold
        self.tooDangerous = False
        self.dangerThreshold = dangerThreshold

    @staticmethod
    def generate_pit_beliefs(observations, model):
        belief_array = []
        beliefs = model.predict_proba(observations)
        for state, belief in zip(model.states, beliefs[0]):
            if hasattr(belief, 'parameters'):
                if 'Pit' in belief.parameters[0]:
                    belief_array.append(belief.parameters[0]['Pit'])
            elif belief == 'No_Pit':
                belief_array.append(0)
            elif belief == 'Pit':
                belief_array.append(1)
        return belief_array

    @staticmethod
    def generate_wumpus_beliefs(observations, model):
        belief_array = []
        beliefs = model.predict_proba(observations)
        beliefs = model.predict_proba(observations)
        for state, belief in zip(model.states, beliefs[0][1:]):
            if hasattr(belief, 'parameters'):
                if 'Wumpus' in belief.parameters[0]:
                    belief_array.append(belief.parameters[0]['Wumpus'])
            elif belief == 'No_Wumpus':
                belief_array.append(0)
            elif belief == 'Wumpus':
                belief_array.append(1)
        return belief_array

    def cells_in_front(self, agent):
        """
        determines what cell numbers are in front of the agent given the agent's location and orientation
        """

        adj = []
        i = 0
        if agent.orientation == 'North':
            while agent.location.y + i < self.gridHeight - 1:
                i += 1
                adj += [Coords(agent.location.x, agent.location.y + i)]
        elif agent.orientation == 'East':
            while agent.location.x + i < self.gridWidth - 1:
                i += 1
                adj += [Coords(agent.location.x + i, agent.location.y)]
        elif agent.orientation == 'South':
            while agent.location.y - i > 0:
                i += 1
                adj += [Coords(agent.location.x, agent.location.y - i)]
        elif agent.orientation == 'West':
            while agent.location.x - i > 0:
                i += 1
                adj += [Coords(agent.location.x - i, agent.location.y)]
        else:
            raise ValueError("incorrect value present in agent.orientation!!!")
        return adj

    def cells_not_in_front(self, agent: Agent):
        all_cells = []
        for j in range(self.gridHeight):
            for i in range(self.gridWidth):
                all_cells.append(Coords(i, j))
        return all_cells

    def generate_observations(self, agent, percept, breeze_observations, stench_observations):
        breeze_observations[0][agent.location.x + agent.location.y * 4] = 'No_Pit'
        breeze_observations[0][
            agent.location.x + agent.location.y * 4 + 4 * 4] = 'Breeze' if percept.breeze else 'No_Breeze'

        if self.wumpusAlive: # if the wumpus is dead, will not update observations about it
            stench_observations[0][1 + agent.location.x + agent.location.y * 4] = 'No_Wumpus'
            stench_observations[0][
                1 + agent.location.x + agent.location.y * 4 + 4 * 4] = 'Stench' if percept.stench else 'No_Stench'

        if percept.scream:
            self.wumpusAlive = False
            in_front = self.cells_in_front(agent)
            not_in_front = self.cells_not_in_front(agent)
            for cell in in_front:
                if cell in not_in_front:
                    not_in_front.remove(cell)

            for cell in not_in_front:
                stench_observations[0][1 + cell.x + cell.y * 4] = 'No_Wumpus'
        elif percept.shoot_without_scream:
            in_front = self.cells_in_front(agent)

            for cell in in_front:
                stench_observations[0][1 + cell.x + cell.y * 4] = 'No_Wumpus'

        return breeze_observations, stench_observations

    def getShortestPath(self, graph, location: Coords, target_cell: int):
        source = BayesianAgent.get_node_from_location(self.G, location)[0]
        return nx.shortest_path(graph, source=source, target=target_cell)

    def getAvailableCells(self, target_cell):
        selected_nodes = [n for n, v in self.G.nodes(data=True) if v['visited'] == True]
        if target_cell not in selected_nodes: # makes it possible to visit a single unexplored cell
            selected_nodes.append(target_cell)
        return self.G.subgraph(selected_nodes)

    def constructBeelinePlan(self, location: Coords, orientation: str, target_cell: int = 0):
        available = self.getAvailableCells(target_cell)
        shortest_path = self.getShortestPath(available, location, target_cell)

        loc = []
        for node in shortest_path:
            loc.append((available.nodes[node]['x'], available.nodes[node]['y']))

        steps = []
        for i in range(len(loc) - 1):
            steps.append((loc[i + 1][0] - loc[i][0], loc[i + 1][1] - loc[i][1]))

        action_list = []
        ori0 = orientation
        for step in steps:
            turns, ori0 = self.get_turns_and_direction(step, ori0)
            action_list = action_list + turns
            action_list.append(Forward())

        if action_list == []: # if no actions have been created, it's because (0,0) is too dangerous and the mission must be aborted
            action_list = [Climb()]
        return action_list


    def get_visted_cells(self):
        return [n for n, v in self.G.nodes(data=True) if v['visited'] == True]

    def get_potential_cells(self, selected_nodes: list):
        unexplored = []
        for node in selected_nodes:
            for neighbor in self.G.neighbors(node):
                unexplored.append(neighbor)
        unexplored = list(set(unexplored))
        for node in selected_nodes:
            if node in unexplored:
                unexplored.remove(node)
        return unexplored

    def generate_beliefs(self, agent: Agent, percept: Percept, pit_graph, wumpus_graph):
        self.breeze_observations, self.stench_observations = self.generate_observations(agent,
                                                                                     percept,
                                                                                     self.breeze_observations,
                                                                                     self.stench_observations)
        pit_beliefs = self.generate_pit_beliefs(self.breeze_observations, pit_graph.model)
        wumpus_beliefs = self.generate_wumpus_beliefs(self.stench_observations, wumpus_graph.model)

        return pit_beliefs, wumpus_beliefs

    def find_safest_unexplored_cells(self, potential_cells, pit_beliefs, wumpus_beliefs):
        danger_level = []
        for cell in potential_cells:
            if self.wumpusAlive:
                # without combining the two beleif networks, I simply choose to take the max of the two dangers
                danger_level.append(max(pit_beliefs[cell], wumpus_beliefs[cell]))
            else:
                danger_level.append(pit_beliefs[cell])

        sorted_by_second = sorted(list(zip(potential_cells, danger_level)), key=lambda tup: tup[1])

        return 0 if (sorted_by_second[0][1] > self.dangerThreshold) and self.allowClimbWithoutGold else sorted_by_second[0][0]

    def should_agent_shoot(self, agent: Agent, wumpus_beliefs):
        """
        determines what cell numbers are in front of the agent given the agent's location and orientation
        """
        cell_num = -1
        if agent.orientation == 'North':
            if agent.location.y + 1 < self.gridHeight:
                cell_num = agent.location.x + (agent.location.y + 1) * self.gridHeight
                shoot = wumpus_beliefs[cell_num] > 0.499
        elif agent.orientation == 'East':
            if agent.location.x + 1 < self.gridWidth:
                cell_num = agent.location.x + 1 + agent.location.y * self.gridHeight
                shoot = wumpus_beliefs[cell_num]
        elif agent.orientation == 'South':
            if agent.location.y - 1 > 0:
                cell_num = agent.location.x + (agent.location.y - 1) * self.gridHeight
        elif agent.orientation == 'West':
            if agent.location.x - 1 > 0:
                cell_num = agent.location.x - 1 + agent.location.y * self.gridHeight
        else:
            raise ValueError("incorrect value present in agent.orientation!!!")

        if cell_num != -1:
            shoot = (wumpus_beliefs[cell_num] > self.dangerThreshold) and agent.hasArrow
        else:
            shoot = False

        return shoot

    def create_next_exploring_actions(self, agent: Agent, percept: Percept, pit_beliefs, wumpus_beliefs):
        """
        actions carried out to explore environment with the least amount of risk.
        """
        selected_nodes = self.get_visted_cells()
        potential_cells = self.get_potential_cells(selected_nodes)
        target_cell = self.find_safest_unexplored_cells(potential_cells, pit_beliefs, wumpus_beliefs)
        return self.constructBeelinePlan(agent.location, agent.orientation, target_cell)

    def create_next_escape_route_actions(self, agent: Agent, percept: Percept, pit_beliefs, wumpus_beliefs):
        """
        actions carried out to exit the environment with the least amount of risk.
        """
        target_cell = 0
        return self.constructBeelinePlan(agent.location, agent.orientation, target_cell)

    def nextAction(self, percept: Percept, agent: Agent, pit_graph, wumpus_graph) -> IAction:
        node = BayesianAgent.get_node_from_location(self.G, agent.location)
        self.G.nodes()[node[0]]['visited'] = True
        self.pit_beliefs, self.wumpus_beliefs = self.generate_beliefs(agent, percept, pit_graph, wumpus_graph)
        if percept.glitter:
            actions = [Grab()]
            exit_actions = self.create_next_escape_route_actions(agent, percept, self.pit_beliefs, self.wumpus_beliefs)
            for action in exit_actions:
                actions.append(action)
        elif self.should_agent_shoot(agent, self.wumpus_beliefs):
            actions = [Shoot()]
        elif agent.hasGold and (agent.location == Coords(0, 0)):
            actions = [Climb()]
        elif self.tooDangerous and (agent.location == Coords(0, 0)):
            actions = [Climb()]
        else:
            actions = self.create_next_exploring_actions(agent, percept, self.pit_beliefs, self.wumpus_beliefs)

        for action in actions:
            yield action

        return None
