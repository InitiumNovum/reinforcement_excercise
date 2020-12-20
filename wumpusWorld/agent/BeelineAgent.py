from wumpusWorld.environment.Agent import *
from wumpusWorld.agent.Navigation import *
from wumpusWorld.environment.Environment import *
import random
import networkx as nx

class BeelineAgent(NavigationMixin):
    def __init__(self, gridWidth, gridHeight):
        NavigationMixin.__init__(self)
        self.safe_locations = []
        self.action_list = []
        self.G = nx.Graph()
        self.G.add_nodes_from(BeelineAgent.create_node_list(gridWidth, gridHeight))
        self.G.add_edges_from(BeelineAgent.create_edge_list(gridWidth, gridHeight))
        self.AngG = self.construct_orientation_graph()
        self.count = -1

    @staticmethod
    def create_Agent():
        return Agent(location=Coords(0,0),
                       orientation='East',
                       hasGold=False,
                       hasArrow=True,
                       isAlive=True)

    def constructBeelinePlan(self, agent):
        selected_nodes = [n for n, v in self.G.nodes(data=True) if v['visited'] == True]
        visited = self.G.subgraph(selected_nodes)
        source = BeelineAgent.get_node_from_location(self.G, agent.location)[0]
        shortest_path = nx.shortest_path(visited, source=source, target=0)

        loc = []
        for node in shortest_path:
            loc.append((visited.nodes[node]['x'], visited.nodes[node]['y']))

        steps = []
        for i in range(len(loc) - 1):
            steps.append((loc[i + 1][0] - loc[i][0], loc[i + 1][1] - loc[i][1]))

        action_list = []
        ori0 = agent.orientation
        for step in steps:
            turns, ori0 = self.get_turns_and_direction(step, ori0)
            action_list = action_list + turns
            action_list.append(Forward())

        return action_list

    @staticmethod
    def filter_location(node, location):
        if (node[1]['x'] == location.x) and (node[1]['y'] == location.y):
            return True
        else:
            return False

    @staticmethod
    def get_node_from_location(G, location):
        for node in G.nodes(data=True):
            if BeelineAgent.filter_location(node, location):
                break
        return node

    def nextAction(self, percept: Percept, agent: Agent) -> IAction:
        node = BeelineAgent.get_node_from_location(self.G, agent.location)
        self.G.nodes()[node[0]]['visited'] = True
        if agent.hasGold:
            if agent.location == Coords(0,0):
                return Climb()
            else:
                if self.count == -1:
                    self.action_list = self.constructBeelinePlan(agent)
                    self.count += 1
                    return self.action_list[self.count]
                else:
                    self.count += 1
                    if self.count == len(self.action_list):
                        raise ValueError("self.count is not supposed to reach this high")
                    return self.action_list[self.count]
        elif percept.glitter:
            return Grab()
        else:
            action = random.randint(0,5)
            if action == 0:
              return Forward()
            elif action == 1:
              return TurnLeft()
            elif action == 2:
              return TurnRight()
            elif action == 3:
              return Shoot()
            elif action == 4:
              return Grab()
            elif action == 5:
              return Climb()
