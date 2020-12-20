from unittest import TestCase
from wumpusWorld.agent.BeelineAgent import *

class TestBeelineAgent(TestCase):
    """
    mostly setting up a bunch of scenarios to make sure that the agent will travel as expected.
    """
    def setUp(self):
        self.beeline = BeelineAgent(gridWidth=4, gridHeight=4)
        self.agent = self.beeline.create_Agent()
        self.percept = Percept.create_Percept(isStench=False, isBreeze=False, isGlitter=False)

    def test_proper_start(self):
        action = self.beeline.nextAction(self.percept, self.agent)
        self.assertTrue(self.beeline.G.nodes()[0]['visited'])
        self.assertEqual(self.agent.orientation, 'East')
        self.assertTrue(issubclass(type(action), IAction))
    def test_first_move_forward(self):
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.forward(4, 4)
        self.assertFalse(self.beeline.G.nodes()[1]['visited'])
        self.assertEqual(self.agent.location.x, 1)
        self.assertEqual(self.agent.location.y, 0)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.assertTrue(self.beeline.G.nodes()[1]['visited'])

    def test_first_turn_left(self):
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.forward(4, 4)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.turnLeft()
        action = self.beeline.nextAction(self.percept, self.agent)
        self.assertTrue(self.beeline.G.nodes()[1]['visited'])
        self.assertEqual(self.agent.location.x, 1)
        self.assertEqual(self.agent.location.y, 0)
        self.assertEqual(self.agent.orientation, 'North')
        self.agent.forward(4,4)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.assertTrue(self.beeline.G.nodes()[5]['visited'])
        self.assertEqual(self.agent.location.x, 1)
        self.assertEqual(self.agent.location.y, 1)

    def test_long_travel_forward(self):
        # then test long travel back
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.forward(4, 4)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.turnLeft()
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.forward(4,4)
        action = self.beeline.nextAction(self.percept, self.agent)

        self.agent.forward(4,4)
        action = self.beeline.nextAction(self.percept, self.agent)

        self.assertTrue(self.beeline.G.nodes()[9]['visited'])
        self.assertEqual(self.agent.location.x, 1)
        self.assertEqual(self.agent.location.y, 2)
        self.assertEqual(self.agent.orientation, 'North')

        self.agent.turnRight()
        action = self.beeline.nextAction(self.percept, self.agent)

        self.assertTrue(self.beeline.G.nodes()[9]['visited'])
        self.assertEqual(self.agent.location.x, 1)
        self.assertEqual(self.agent.location.y, 2)
        self.assertEqual(self.agent.orientation, 'East')

        self.agent.forward(4, 4)
        action = self.beeline.nextAction(self.percept, self.agent)

        self.assertTrue(self.beeline.G.nodes()[10]['visited'])
        self.assertEqual(self.agent.location.x, 2)
        self.assertEqual(self.agent.location.y, 2)
        self.assertEqual(self.agent.orientation, 'East')

    def test_long_travel_back(self):
        # then test long travel back
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.forward(4, 4)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.turnLeft()
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.forward(4,4)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.forward(4,4)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.turnRight()
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.forward(4, 4)
        action = self.beeline.nextAction(self.percept, self.agent)

        self.agent.hasGold = True

        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.turnLeft()
        self.assertEqual(type(action), TurnLeft)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.turnLeft()
        self.assertEqual(type(action), TurnLeft)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.forward(4, 4)
        self.assertEqual(type(action), Forward)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.turnLeft()
        self.assertEqual(type(action), TurnLeft)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.forward(4, 4)
        self.assertEqual(type(action), Forward)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.forward(4, 4)
        self.assertEqual(type(action), Forward)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.turnRight()
        self.assertEqual(type(action), TurnRight)
        action = self.beeline.nextAction(self.percept, self.agent)
        self.agent.forward(4, 4)
        self.assertEqual(type(action), Forward)
        self.assertEqual(self.agent.location, Coords(0,0))
        action = self.beeline.nextAction(self.percept, self.agent)
        self.assertEqual(type(action), Climb)

    def test_long_travel_back_2(self):
        self.beeline.G.nodes()[0]['visited'] = True
        self.beeline.G.nodes()[1]['visited'] = True
        self.beeline.G.nodes()[2]['visited'] = True
        self.beeline.G.nodes()[3]['visited'] = True
        self.beeline.G.nodes()[4]['visited'] = True
        self.beeline.G.nodes()[5]['visited'] = True
        self.beeline.G.nodes()[6]['visited'] = True
        self.beeline.G.nodes()[8]['visited'] = True
        self.beeline.G.nodes()[9]['visited'] = True
        self.beeline.G.nodes()[10]['visited'] = True
        self.beeline.G.nodes()[12]['visited'] = True
        self.beeline.G.nodes()[13]['visited'] = True
        self.beeline.G.nodes()[14]['visited'] = True
        self.beeline.G.nodes()[15]['visited'] = True

        self.agent.location.x = 1
        self.agent.location.y = 2
        self.agent.orientation = 'South'
        self.agent.hasGold = True
        action = self.beeline.nextAction(self.percept, self.agent)





