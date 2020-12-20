from unittest import TestCase
from wumpusWorld.environment.Environment import *
from wumpusWorld.environment.Agent import *

class TestPercept(TestCase):
    def setUp(self) -> None:
        self.forward = Forward()
        self.percept = Percept(stench=False,
                               breeze=False,
                               glitter=False,
                               bump=False,
                               scream=False,
                               isTerminated=False,
                               reward=0)

    def test_show(self):
        res = {'stench': False,
                 'breeze': False,
                 'glitter': False,
                 'bump': False,
                 'scream': False,
                 'isTerminated': False,
                 'reward': 0}

        self.assertTrue(self.percept.show() == res)

    def test_stench_get(self):
        self.assertTrue(self.percept.stench == False)

    def test_stench_set(self):
        self.percept.stench = True
        self.assertTrue(self.percept.stench == True)

    def test_breeze_get(self):
        self.assertTrue(self.percept.breeze == False)

    def test_breeze_set(self):
        self.percept.breeze = True
        self.assertTrue(self.percept.breeze == True)

    def test_glitter_get(self):
        self.assertTrue(self.percept.glitter == False)

    def test_glitter_set(self):
        self.percept.glitter = True
        self.assertTrue(self.percept.glitter == True)

    def test_bump_get(self):
        self.assertTrue(self.percept.bump == False)

    def test_bump_set(self):
        self.percept.bump = True
        self.assertTrue(self.percept.bump == True)

    def test_scream_get(self):
        self.assertTrue(self.percept.scream == False)

    def test_scream_set(self):
        self.percept.scream = True
        self.assertTrue(self.percept.scream == True)

    def test_isTerminated_get(self):
        self.assertTrue(self.percept.isTerminated == False)

    def test_isTerminated_set(self):
        self.percept.isTerminated = True
        self.assertTrue(self.percept.isTerminated == True)

    def test_reward_get(self):
        self.assertTrue(self.percept.reward == 0)

    def test_reward_set(self):
        self.percept.reward = self.percept.reward + 1
        self.assertTrue(self.percept.reward == 1)

class TestEnvironment(TestCase):
    def setUp(self) -> None:
        self.env = Environment(gridWidth=4,
                               gridHeight=4,
                               #pitProb=0.1,
                               allowClimbWithoutGold=False,
                               pitLocations=[Coords(0, 2), Coords(1, 2)],
                               terminated=False,
                               wumpusLocation=Coords(2, 2),
                               wumpusAlive=True,
                               goldLocation=Coords(3, 3))
        self.agent_1 = Agent()
        self.percept_1 = Percept(stench=False,
                               breeze=False,
                               glitter=False,
                               bump=False,
                               scream=False,
                               isTerminated=False,
                               reward=0)

    def test_isPitAt(self):
        self.assertFalse(self.env.isPitAt(Coords(1, 1)))
        self.assertTrue(self.env.isPitAt(Coords(0, 2)))
        self.assertTrue(self.env.isPitAt(Coords(1, 2)))

    def test_isWumpusAt(self):
        self.assertFalse(self.env.isWumpusAt(Coords(1, 1)))
        self.assertTrue(self.env.isWumpusAt(Coords(2, 2)))

    def test_isGoldAt(self):
        self.assertTrue(self.env.isGoldAt(Coords(3,3)))

    def test_isGlitter(self):
        self.assertTrue(self.env.isGlitter(Coords(3, 3)))

    def test_adjacentCells(self):
        cells = self.env.adjacentCells(Coords(0, 1))
        self.assertEqual(cells[0], Coords(1, 1))
        self.assertEqual(cells[1], Coords(0, 0))
        self.assertEqual(cells[2], Coords(0, 2))

    def test_isPitAdjacent(self):
        #(0, 2)
        self.assertTrue(self.env.isPitAdjacent(Coords(0, 1)))
        self.assertTrue(self.env.isPitAdjacent(Coords(0, 3)))
        self.assertTrue(self.env.isPitAdjacent(Coords(1, 2)))
        # (1, 2)
        self.assertTrue(self.env.isPitAdjacent(Coords(1, 1)))
        self.assertTrue(self.env.isPitAdjacent(Coords(1, 3)))
        self.assertTrue(self.env.isPitAdjacent(Coords(0, 2)))
        self.assertTrue(self.env.isPitAdjacent(Coords(2, 2)))

    def test_isWumpusAdjacent(self):
        #(2, 2)
        self.assertTrue(self.env.isWumpusAdjacent(Coords(2, 3)))
        self.assertTrue(self.env.isWumpusAdjacent(Coords(2, 1)))
        self.assertTrue(self.env.isWumpusAdjacent(Coords(1, 2)))
        self.assertTrue(self.env.isWumpusAdjacent(Coords(3, 2)))

    def test_isBreeze(self):
        #(0, 2)
        self.assertTrue(self.env.isBreeze(Coords(0, 1)))
        self.assertTrue(self.env.isBreeze(Coords(0, 3)))
        self.assertTrue(self.env.isBreeze(Coords(1, 2)))
        # (1, 2)
        self.assertTrue(self.env.isBreeze(Coords(1, 1)))
        self.assertTrue(self.env.isBreeze(Coords(1, 3)))
        self.assertTrue(self.env.isBreeze(Coords(0, 2)))
        self.assertTrue(self.env.isBreeze(Coords(2, 2)))

    def test_isStench(self):
        self.assertTrue(self.env.isStench(Coords(2, 2)))
        self.assertTrue(self.env.isStench(Coords(2, 3)))
        self.assertTrue(self.env.isStench(Coords(2, 1)))
        self.assertTrue(self.env.isStench(Coords(1, 2)))
        self.assertTrue(self.env.isStench(Coords(3, 2)))

    def test_applyAction_Forward(self):
        action = Forward()
        agent, percept = self.env.applyAction(action, self.percept_1, self.agent_1)
        print("DONE")
        self.assertTrue(agent.hasArrow)
        self.assertFalse(agent.hasBumped)
        self.assertFalse(agent.hasGold)
        self.assertTrue(agent.isAlive)
        self.assertEqual(agent.location, Coords(1, 0))
        self.assertEqual(agent.orientation, 'East')

    def test_EnvironmentFactory(self):
        env = Environment.create_FourByFourRandomEnvironment(4, 4, Bayes.Probability(0.2), False)
        self.assertFalse(env.allowClimbWithoutGold)
        self.assertEqual(env.gridWidth, 4)
        self.assertEqual(env.gridHeight, 4)
        self.assertFalse(env.terminated)
        self.assertTrue(env.wumpusAlive)