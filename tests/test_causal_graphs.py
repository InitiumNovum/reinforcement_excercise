import unittest
from wumpusWorld.agent.causal_graphs import *
from wumpusWorld.environment.Environment import *

class MyTestCase(unittest.TestCase):
    def test_pit_belief_network(self):
        self.env = Environment(gridWidth=4,
                               gridHeight=4,
                               allowClimbWithoutGold=False,
                               pitLocations=[Coords(0, 2), Coords(1, 2)],
                               terminated=False,
                               wumpusLocation=Coords(2, 2),
                               wumpusAlive=True,
                               goldLocation=Coords(3, 3))

        self.pit_belief = PitBeliefNetwork(self.env)
        self.assertTrue(self.pit_belief.model.states[4].distribution.parameters[0]['Pit'] == 0.2)
        self.assertTrue(self.pit_belief.model.states[4].distribution.parameters[0]['No_Pit'] == 0.8)

if __name__ == '__main__':
    unittest.main()
