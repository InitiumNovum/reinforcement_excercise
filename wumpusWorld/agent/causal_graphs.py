import pomegranate as pm
from wumpusWorld.environment.Environment import *

def general_generate_condition_table(num, cause=['Pit', 'No_Pit'], effect=['Breeze', 'No_Breeze']):
    """
    cause = ['Wumpus', 'No_Wumpus']
    effect = ['Stench', 'No_Stench']
    :param num:
    :param cause:
    :param effect:
    :return:
    """
    sides = []

    if num == 2:
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    if i == 1 and j == 1:
                        sides.append([cause[i], cause[j], effect[k], 1 if k == 1 else 0])
                    else:
                        sides.append([cause[i], cause[j], effect[k], 0 if k == 1 else 1])
    elif num == 3:
        for i in range(2):
            for j in range(2):
                for l in range(2):
                    for k in range(2):
                        if i == 1 and j == 1 and l == 1:
                            sides.append([cause[i], cause[j], cause[l], effect[k], 1 if k == 1 else 0])
                        else:
                            sides.append([cause[i], cause[j], cause[l], effect[k], 0 if k == 1 else 1])
    elif num == 4:
        for i in range(2):
            for j in range(2):
                for l in range(2):
                    for m in range(2):
                        for k in range(2):
                            if i == 1 and j == 1 and l == 1 and m == 1:
                                sides.append([cause[i], cause[j], cause[l], cause[m], effect[k], 1 if k == 1 else 0])
                            else:
                                sides.append([cause[i], cause[j], cause[l], cause[m], effect[k], 0 if k == 1 else 1])

    else:
        raise ValueError("num must be 2, 3, 4 or 5")

    return sides

class PitBeliefNetwork:
    @staticmethod
    def generate_condition_table(num):
        return general_generate_condition_table(num, cause=['Pit', 'No_Pit'], effect=['Breeze', 'No_Breeze'])
        return sides


    def generate_pit_states(self, environment: Environment):
        pit_dists = dict()
        pit_states = dict()
        for j in range(environment.gridHeight):
            for i in range(environment.gridWidth):
                if i==0 and j==0:
                    pit_dists['%02d_%02d' % (i, j)] = pm.DiscreteDistribution({'Pit': 0.0, 'No_Pit': 1.0})
                else:
                    pit_dists['%02d_%02d' % (i, j)] = pm.DiscreteDistribution({'Pit': 0.2, 'No_Pit': 0.8})
                pit_dists['%02d_%02d' % (i, j)].name = '%02d_%02d' % (i, j)
                pit_states['%02d_%02d' % (i, j)] = pm.State(pit_dists['%02d_%02d' % (i, j)], name="pit_state_%02d_%02d" % (i, j))
        return pit_dists, pit_states

    def generate_breeze_states(self, environment: Environment, pit_dists):
        breeze_dists = dict()
        breezes = []
        breeze_states = dict()
        for j in range(environment.gridHeight):
            for i in range(environment.gridWidth):
                coords = environment.adjacentCells(Coords(i, j))
                pit_list = [pit_dists["%02d_%02d" % (coord.x, coord.y)] for coord in coords]
                if len(coords) == 2:
                    breeze_dists["%02d_%02d" % (i, j)] = pm.ConditionalProbabilityTable(self.generate_condition_table(2), pit_list)
                elif len(coords) == 3:
                    breeze_dists["%02d_%02d" % (i, j)] = pm.ConditionalProbabilityTable(self.generate_condition_table(3), pit_list)
                elif len(coords) == 4:
                    breeze_dists["%02d_%02d" % (i, j)] = pm.ConditionalProbabilityTable(self.generate_condition_table(4), pit_list)
                else:
                    raise ValueError("coords is not right length!")

                breeze_states['%02d_%02d' % (i, j)] = pm.State(breeze_dists['%02d_%02d' % (i, j)],
                                                               name="breeze_state_%02d_%02d" % (i, j))
        return breeze_dists, breeze_states

    def __init__(self, environment: Environment):

        pit_dists, pit_states = self.generate_pit_states(environment)
        breeze_dists, breeze_states = self.generate_breeze_states(environment, pit_dists)

        all_breeze_states = [breeze_states[state] for state in breeze_states]
        all_pit_states = [pit_states[state] for state in pit_states]

        self.model = pm.BayesianNetwork("Breezes Problem")
        self.model.add_states(*all_pit_states, *all_breeze_states)

        for j in range(environment.gridHeight):
            for i in range(environment.gridWidth):
                coords = environment.adjacentCells(Coords(i, j))
                pit_list = [pit_states["%02d_%02d" % (coord.x, coord.y)] for coord in coords]
                for pit_state in pit_list:
                    self.model.add_edge(pit_state, breeze_states["%02d_%02d" % (i, j)])

        self.model.bake()

class PitBeliefNetwork_with_center:
    @staticmethod
    def generate_condition_table(num):
        if num == 2:
            sides = [['Pit', 'Pit', 'Breeze', 1.0],
                         ['Pit', 'Pit', 'No_Breeze', 0.0],
                         ['Pit', 'No_Pit', 'Breeze', 1.0],
                         ['Pit', 'No_Pit', 'No_Breeze', 0.0],
                         ['No_Pit', 'Pit', 'Breeze', 1.0],
                         ['No_Pit', 'Pit', 'No_Breeze', 0.0],
                         ['No_Pit', 'No_Pit', 'Breeze', 0.0],
                         ['No_Pit', 'No_Pit', 'No_Breeze', 0.0]]
        elif num == 3:
            sides = [['Pit', 'Pit', 'Pit', 'Breeze', 1.0],
                           ['Pit', 'Pit', 'Pit', 'No_Breeze', 0.0],
                           ['Pit', 'Pit', 'No_Pit', 'Breeze', 1.0],
                           ['Pit', 'Pit', 'No_Pit', 'No_Breeze', 0.0],
                           ['Pit', 'No_Pit', 'Pit', 'Breeze', 1.0],
                           ['Pit', 'No_Pit', 'Pit', 'No_Breeze', 0.0],
                           ['Pit', 'No_Pit', 'No_Pit', 'Breeze', 1.0],
                           ['Pit', 'No_Pit', 'No_Pit', 'No_Breeze', 0.0],
                           ['No_Pit', 'Pit', 'Pit', 'Breeze', 1.0],
                           ['No_Pit', 'Pit', 'Pit', 'No_Breeze', 0.0],
                           ['No_Pit', 'Pit', 'No_Pit', 'Breeze', 1.0],
                           ['No_Pit', 'Pit', 'No_Pit', 'No_Breeze', 0.0],
                           ['No_Pit', 'No_Pit', 'Pit', 'Breeze', 1.0],
                           ['No_Pit', 'No_Pit', 'Pit', 'No_Breeze', 0.0],
                           ['No_Pit', 'No_Pit', 'No_Pit', 'Breeze', 0.0],
                           ['No_Pit', 'No_Pit', 'No_Pit', 'No_Breeze', 1.0]]
        elif num == 4:
            sides = [['Pit', 'Pit', 'Pit', 'Pit', 'Breeze', 1.0],
                          ['Pit', 'Pit', 'Pit', 'Pit', 'No_Breeze', 0.0],
                          ['Pit', 'Pit', 'Pit', 'No_Pit', 'Breeze', 1.0],
                          ['Pit', 'Pit', 'Pit', 'No_Pit', 'No_Breeze', 0.0],
                          ['Pit', 'Pit', 'No_Pit', 'Pit', 'Breeze', 1.0],
                          ['Pit', 'Pit', 'No_Pit', 'Pit', 'No_Breeze', 0.0],
                          ['Pit', 'Pit', 'No_Pit', 'No_Pit', 'Breeze', 1.0],
                          ['Pit', 'Pit', 'No_Pit', 'No_Pit', 'No_Breeze', 0.0],
                          ['Pit', 'No_Pit', 'Pit', 'Pit', 'Breeze', 1.0],
                          ['Pit', 'No_Pit', 'Pit', 'Pit', 'No_Breeze', 0.0],
                          ['Pit', 'No_Pit', 'Pit', 'No_Pit', 'Breeze', 1.0],
                          ['Pit', 'No_Pit', 'Pit', 'No_Pit', 'No_Breeze', 0.0],
                          ['Pit', 'No_Pit', 'No_Pit', 'Pit', 'Breeze', 1.0],
                          ['Pit', 'No_Pit', 'No_Pit', 'Pit', 'No_Breeze', 0.0],
                          ['Pit', 'No_Pit', 'No_Pit', 'No_Pit', 'Breeze', 1.0],
                          ['Pit', 'No_Pit', 'No_Pit', 'No_Pit', 'No_Breeze', 0.0],
                          ['No_Pit', 'Pit', 'Pit', 'Pit', 'Breeze', 1.0],
                          ['No_Pit', 'Pit', 'Pit', 'Pit', 'No_Breeze', 0.0],
                          ['No_Pit', 'Pit', 'Pit', 'No_Pit', 'Breeze', 1.0],
                          ['No_Pit', 'Pit', 'Pit', 'No_Pit', 'No_Breeze', 0.0],
                          ['No_Pit', 'Pit', 'No_Pit', 'Pit', 'Breeze', 1.0],
                          ['No_Pit', 'Pit', 'No_Pit', 'Pit', 'No_Breeze', 0.0],
                          ['No_Pit', 'Pit', 'No_Pit', 'No_Pit', 'Breeze', 1.0],
                          ['No_Pit', 'Pit', 'No_Pit', 'No_Pit', 'No_Breeze', 0.0],
                          ['No_Pit', 'No_Pit', 'Pit', 'Pit', 'Breeze', 1.0],
                          ['No_Pit', 'No_Pit', 'Pit', 'Pit', 'No_Breeze', 0.0],
                          ['No_Pit', 'No_Pit', 'Pit', 'No_Pit', 'Breeze', 1.0],
                          ['No_Pit', 'No_Pit', 'Pit', 'No_Pit', 'No_Breeze', 0.0],
                          ['No_Pit', 'No_Pit', 'No_Pit', 'Pit', 'Breeze', 1.0],
                          ['No_Pit', 'No_Pit', 'No_Pit', 'Pit', 'No_Breeze', 0.0],
                          ['No_Pit', 'No_Pit', 'No_Pit', 'No_Pit', 'Breeze', 0.0],
                          ['No_Pit', 'No_Pit', 'No_Pit', 'No_Pit', 'No_Breeze', 1.0]]
        else:
            raise ValueError("num must be 2, 3 or 4")

        return sides

    def generate_pit_states(self, environment: Environment):
        pit_dists = dict()
        pit_states = dict()
        for j in range(environment.gridHeight):
            for i in range(environment.gridWidth):
                if i==0 and j==0:
                    pit_dists['%02d_%02d' % (i, j)] = pm.DiscreteDistribution({'Pit': 0.0, 'No_Pit': 1.0})
                else:
                    pit_dists['%02d_%02d' % (i, j)] = pm.DiscreteDistribution({'Pit': 0.2, 'No_Pit': 0.8})
                pit_dists['%02d_%02d' % (i, j)].name = '%02d_%02d' % (i, j)
                pit_states['%02d_%02d' % (i, j)] = pm.State(pit_dists['%02d_%02d' % (i, j)], name="pit_state_%02d_%02d" % (i, j))
        return pit_dists, pit_states

    def generate_breeze_states(self, environment: Environment, pit_dists):
        breeze_dists = dict()
        breezes = []
        breeze_states = dict()
        for j in range(environment.gridHeight):
            for i in range(environment.gridWidth):
                coords = environment.adjacentCells(Coords(i, j))
                pit_list = [pit_dists["%02d_%02d" % (coord.x, coord.y)] for coord in coords]
                if len(coords) == 2:
                    breeze_dists["%02d_%02d" % (i, j)] = pm.ConditionalProbabilityTable(self.generate_condition_table(2), pit_list)
                elif len(coords) == 3:
                    breeze_dists["%02d_%02d" % (i, j)] = pm.ConditionalProbabilityTable(self.generate_condition_table(3), pit_list)
                elif len(coords) == 4:
                    breeze_dists["%02d_%02d" % (i, j)] = pm.ConditionalProbabilityTable(self.generate_condition_table(4), pit_list)
                else:
                    raise ValueError("coords is not right length!")

                breeze_states['%02d_%02d' % (i, j)] = pm.State(breeze_dists['%02d_%02d' % (i, j)],
                                                               name="breeze_state_%02d_%02d" % (i, j))
        return breeze_dists, breeze_states

    def __init__(self, environment: Environment):

        pit_dists, pit_states = self.generate_pit_states(environment)
        breeze_dists, breeze_states = self.generate_breeze_states(environment, pit_dists)

        all_breeze_states = [breeze_states[state] for state in breeze_states]
        all_pit_states = [pit_states[state] for state in pit_states]

        self.model = pm.BayesianNetwork("Breezes Problem")
        self.model.add_states(*all_pit_states, *all_breeze_states)

        breeze_dists = dict()
        breezes = []
        for j in range(environment.gridHeight):
            for i in range(environment.gridWidth):
                coords = environment.adjacentCells(Coords(i, j))
                pit_list = [pit_states["%02d_%02d" % (coord.x, coord.y)] for coord in coords]
                for pit_state in pit_list:
                    self.model.add_edge(pit_state, breeze_states["%02d_%02d" % (i, j)])

        self.model.bake()

class WumpusBeliefNetwork:
    @staticmethod
    def generate_condition_table(num):
        return general_generate_condition_table(num, cause=['Wumpus', 'No_Wumpus'], effect=['Stench', 'No_Stench'])
        return sides

    @staticmethod
    def generate_wumpus_state(environment):
        wumpus_dict = dict()
        for j in range(environment.gridHeight):
            for i in range(environment.gridWidth):
                if i == 0 and j == 0:
                    wumpus_dict['%02d_%02d' % (i, j)] = 0.0
                else:
                    wumpus_dict['%02d_%02d' % (i, j)] = 1.0 / (environment.gridWidth * environment.gridHeight - 1)
        wumpus_dist = pm.DiscreteDistribution(wumpus_dict)
        wumpus_state = pm.State(wumpus_dist, name="wumpus_state")
        return wumpus_dist, wumpus_state

    @staticmethod
    def generate_wumpus_cond_states(environment, wumpus_dist):
        wumpus_cond = dict()
        wumpus_cond_dist = dict()
        wumpus_cond_states = dict()
        for j in range(environment.gridHeight):
            for i in range(environment.gridWidth):
                wumpus_cond = []
                for jj in range(environment.gridHeight):
                    for ii in range(environment.gridWidth):
                        if ii == i and jj == j:
                            wumpus_cond.append(['%02d_%02d' % (ii, jj), 'Wumpus', 1.0])
                            wumpus_cond.append(['%02d_%02d' % (ii, jj), 'No_Wumpus', 0.0])
                        else:
                            wumpus_cond.append(['%02d_%02d' % (ii, jj), 'Wumpus', 0.0])
                            wumpus_cond.append(['%02d_%02d' % (ii, jj), 'No_Wumpus', 1.0])
                wumpus_cond_dist['%02d_%02d' % (i, j)] = pm.ConditionalProbabilityTable(wumpus_cond, [wumpus_dist])
                wumpus_cond_states['%02d_%02d' % (i, j)] = pm.State(wumpus_cond_dist['%02d_%02d' % (i, j)],
                                                                    name="wumpus_cond_state_%02d_%02d" % (i, j))
        return wumpus_cond_dist, wumpus_cond_states

    @staticmethod
    def generate_stench_states(environment, wumpus_cond_dists):
        stench_dists = dict()
        stenches = []
        stench_states = dict()
        for j in range(environment.gridHeight):
            for i in range(environment.gridWidth):
                coords = environment.adjacentCells(Coords(i, j))
                wumpus_list = [wumpus_cond_dists["%02d_%02d" % (coord.x, coord.y)] for coord in coords]
                if len(coords) == 2:
                    stench_dists["%02d_%02d" % (i, j)] = pm.ConditionalProbabilityTable(WumpusBeliefNetwork.generate_condition_table(2),
                                                                                        wumpus_list)
                elif len(coords) == 3:
                    stench_dists["%02d_%02d" % (i, j)] = pm.ConditionalProbabilityTable(WumpusBeliefNetwork.generate_condition_table(3),
                                                                                        wumpus_list)
                elif len(coords) == 4:
                    stench_dists["%02d_%02d" % (i, j)] = pm.ConditionalProbabilityTable(WumpusBeliefNetwork.generate_condition_table(4),
                                                                                        wumpus_list)
                else:
                    raise ValueError("coords is not right length!")

                stench_states['%02d_%02d' % (i, j)] = pm.State(stench_dists['%02d_%02d' % (i, j)],
                                                               name="stench_state_%02d_%02d" % (i, j))

        return stench_dists, stench_states

    def __init__(self, environment: Environment):
        wumpus_dist, wumpus_state = WumpusBeliefNetwork.generate_wumpus_state(environment)
        wumpus_cond_dists, wumpus_cond_states = WumpusBeliefNetwork.generate_wumpus_cond_states(environment, wumpus_dist)
        stench_dists, stench_states = WumpusBeliefNetwork.generate_stench_states(environment, wumpus_cond_dists)

        all_stench_states = [stench_states[state] for state in stench_states]
        all_wumpus_cond_states = [wumpus_cond_states[state] for state in wumpus_cond_states]

        self.model = pm.BayesianNetwork("Stench Problem")
        self.model.add_states(wumpus_state, *all_wumpus_cond_states, *all_stench_states)

        for j in range(environment.gridHeight):
            for i in range(environment.gridWidth):
                self.model.add_edge(wumpus_state, wumpus_cond_states["%02d_%02d" % (i, j)])

        for j in range(environment.gridHeight):
            for i in range(environment.gridWidth):
                coords = environment.adjacentCells(Coords(i, j))
                stench_list = [stench_states["%02d_%02d" % (coord.x, coord.y)] for coord in coords]
                for stench_state in stench_list:
                    self.model.add_edge(wumpus_cond_states["%02d_%02d" % (i, j)], stench_state)

        self.model.bake()
