from wumpusWorld.Bayes import *
from wumpusWorld.environment.core import *
from wumpusWorld.environment.Agent import *
from abc import ABCMeta, abstractmethod
import numpy as np
from wumpusWorld.environment.Percept import *

#TODO environment is a singleton, so perhaps enforce this constraint.
class Environment:
    """
    Environ
    """

    def __init__(self,
                 gridWidth: int,
                 gridHeight: int,
                 pitLocations: list,
                 wumpusLocation: Coords,
                 goldLocation: Coords,
                 wumpusAlive: bool = True,
                 terminated: bool = False,
                 allowClimbWithoutGold: bool=False):
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.allowClimbWithoutGold = allowClimbWithoutGold
        self.pitLocations = pitLocations
        self.terminated = terminated
        self.wumpusLocation = wumpusLocation
        self.wumpusAlive = wumpusAlive
        self.goldLocation = goldLocation

    def isPitAt(self, coords: Coords) -> bool:
        return coords in self.pitLocations

    def isWumpusAt(self, coords: Coords) -> bool:
        return self.wumpusLocation == coords

    def isGoldAt(self, coords: Coords) -> bool:
        return self.goldLocation == coords

    def killAttemptSuccessful(self, agent) -> bool:
        def wumpusInLineOfFire() -> bool:
            if agent.orientation == 'North':
                result = agent.location.x == self.wumpusLocation.x and agent.location.y < self.wumpusLocation.y
            elif agent.orientation == 'East':
                result = agent.location.x < self.wumpusLocation.x and agent.location.y == self.wumpusLocation.y
            elif agent.orientation == 'South':
                result = agent.location.x == self.wumpusLocation.x and agent.location.y > self.wumpusLocation.y
            elif agent.orientation == 'West':
                result = agent.location.x > self.wumpusLocation.x and agent.location.y == self.wumpusLocation.y
            else:
                raise Exception('orientation not within the set "North", "East", "South", "West"')

            return result

        return self.wumpusAlive and wumpusInLineOfFire()

    def adjacentCells(self, coords: Coords) -> list:
        """
        provides a list of cell coordinates that are adjacent to the specified cell.
        :param coords:
        :return:
        """
        adj = []
        adj += [Coords(coords.x - 1, coords.y)] if coords.x > 0 else []
        adj += [Coords(coords.x+1, coords.y)] if coords.x < self.gridWidth - 1 else []
        adj += [Coords(coords.x, coords.y-1)] if coords.y > 0 else []
        adj += [Coords(coords.x, coords.y+1)] if coords.y < self.gridHeight - 1 else []

#TODO turning the adjacent list into a numpy array might be even better for performance purposes
        return adj

    def isPitAdjacent(self, coords: Coords) -> bool:
        for pitLocation in self.pitLocations:
            if any(coords == cell for cell in self.adjacentCells(pitLocation)):
                return True
        return False

    def isWumpusAdjacent(self, coords: Coords) -> bool:
        return any(coords == cell for cell in self.adjacentCells(self.wumpusLocation))

    def isBreeze(self, location: Coords) -> bool:
        return self.isPitAdjacent(location)

    def isStench(self, location: Coords) -> bool:
        return self.isWumpusAdjacent(location) or self.isWumpusAt(location)

    def isGlitter(self, location: Coords) -> bool:
        return self.goldLocation == location

    def applyAction(self, action: IAction, percept: Percept, agent: Agent) -> (Agent, Percept):
        if self.terminated:
            percept.stench = False
            percept.breeze = False
            percept.glitter = False
            percept.bump = False
            percept.scream = False
            percept.shoot_without_scream = False
            percept.isTerminated = False
            percept.reward = 0
        else:
            self, percept, agent = action(self, percept, agent)
        return agent, percept

    @staticmethod
    def create_FourByFourRandomEnvironment(gridWidth: int = 4,
                                           gridHeight: int = 4,
                                           pitProb: Bayes.Probability=Bayes.Probability(0.2),
                                           allowClimbWithoutGold: bool=False):

        def genCoords(cell_num, gridWidth, gridHeight):
            return Coords(cell_num%gridWidth, cell_num//gridHeight)

        arr = np.arange(1, gridWidth*gridHeight)
        np.random.shuffle(arr)
        goldLocation = genCoords(arr[0], gridWidth, gridHeight)
        wumpusLocation = genCoords(arr[1], gridWidth, gridHeight)
        pitLocations = []
        for item in arr[2:]:
            if np.random.binomial(1, pitProb.x, 1) == 1:
                pitLocations.append(genCoords(item, gridWidth, gridHeight))

        return Environment(gridWidth,
                             gridHeight,
                             pitLocations,
                             wumpusLocation,
                             goldLocation,
                             wumpusAlive=True,
                             terminated=False,
                             allowClimbWithoutGold=allowClimbWithoutGold)