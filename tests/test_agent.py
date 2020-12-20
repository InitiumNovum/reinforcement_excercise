from unittest import TestCase
from wumpusWorld.environment.Agent import *
from wumpusWorld.environment.Environment import *

class TestAgent(TestCase):
    def setUp(self):
        self.agent = Agent()
    def test_movement(self):
        self.agent.forward(4, 4)
        self.assertEqual(self.agent.location.x, 1)
        self.assertEqual(self.agent.location.y, 0)
        self.agent.turnLeft()
        self.agent.forward(4, 4)
        self.assertEqual(self.agent.location.x, 1)
        self.assertEqual(self.agent.location.y, 1)
        self.agent.forward(4, 4)
        self.agent.forward(4, 4)
        self.assertEqual(self.agent.location.x, 1)
        self.assertEqual(self.agent.location.y, 3)
        self.agent.forward(4, 4)
        self.assertEqual(self.agent.location.x, 1)
        self.assertEqual(self.agent.location.y, 3)
        self.agent.turnRight()
        self.agent.forward(4, 4)
        self.agent.forward(4, 4)
        self.assertEqual(self.agent.location.x, 3)
        self.assertEqual(self.agent.location.y, 3)
        self.agent.forward(4, 4)
        self.assertEqual(self.agent.location.x, 3)
        self.assertEqual(self.agent.location.y, 3)

    def test_status_indicators(self):
        self.assertEqual(self.agent.hasGold, False)
        self.assertEqual(self.agent.hasArrow, True)
        self.assertEqual(self.agent.isAlive, True)
