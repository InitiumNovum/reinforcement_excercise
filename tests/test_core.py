from unittest import TestCase
from wumpusWorld.environment.core import *
from wumpusWorld.environment.Agent import *
from wumpusWorld.environment.Environment import *
from wumpusWorld.environment.Percept import *

class TestCoords(TestCase):
    def setUp(self) -> None:
        self.coord = Coords(4, 6)

    def test_x_get(self):
        self.assertEqual(self.coord.x, 4)

    def test_x_set(self):
        self.coord.x = 1
        self.assertEqual(self.coord.x, 1)

    def test_y_get(self):
        self.assertEqual(self.coord.y, 6)

    def test_y_set(self):
        self.coord.y = 9
        self.assertEqual(self.coord.y, 9)

    def test_equality(self):
        self.assertTrue(self.coord == Coords(4, 6))
        self.assertFalse(self.coord == Coords(4, 5))

class TestOrientation(TestCase):
    def setUp(self) -> None:
        self.orientation = Orientation()

    def test_orientation_get(self):
        self.assertEqual(self.orientation.orientation, 'East')

    def test_left_turn(self):
        self.orientation.turnLeft()
        self.assertEqual(self.orientation.orientation, 'North')
        self.orientation.turnLeft()
        self.assertEqual(self.orientation.orientation, 'West')
        self.orientation.turnLeft()
        self.assertEqual(self.orientation.orientation, 'South')
        self.orientation.turnLeft()
        self.assertEqual(self.orientation.orientation, 'East')

    def test_right_turn(self):
        self.orientation.turnRight()
        self.assertEqual(self.orientation.orientation, 'South')
        self.orientation.turnRight()
        self.assertEqual(self.orientation.orientation, 'West')
        self.orientation.turnRight()
        self.assertEqual(self.orientation.orientation, 'North')
        self.orientation.turnRight()
        self.assertEqual(self.orientation.orientation, 'East')

class TestForward(TestCase):
    def setUp(self) -> None:
        self.forward = Forward()
        self.agent = Agent()
        self.environment = Environment(gridWidth=4,
                               gridHeight=4,
                               #pitProb=0.1,
                               allowClimbWithoutGold=False,
                               pitLocations=[Coords(0, 2), Coords(1, 2)],
                               terminated=False,
                               wumpusLocation=Coords(2, 2),
                               wumpusAlive=True,
                               goldLocation=Coords(3, 3))
        self.percept = Percept(stench=False,
                               breeze=False,
                               glitter=False,
                               bump=False,
                               scream=False,
                               isTerminated=False,
                               reward=0)

#    def test_orientation_get(self):
#        self.assertEqual(self.orientation.orientation, 'East')
