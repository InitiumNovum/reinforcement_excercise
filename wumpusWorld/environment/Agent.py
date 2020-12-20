from wumpusWorld.environment.core import *
import copy

class Agent(Orientation):
    def __init__(self,
                 location = Coords(0, 0),
                 orientation = 'East',
                 hasGold = False,
                 hasArrow = True,
                 isAlive = True):

        self.location = location
        self.hasGold = hasGold
        self.hasArrow = hasArrow
        self.isAlive = isAlive
        self.hasBumped = False
        super(Agent, self).__init__(orientation)

    def forward(self, gridWidth: int, gridHeight: int):
        #self._orientation.
        temp = copy.copy(self.location)
        if self.orientation == 'North':
            self.location.y = min(gridHeight-1, self.location.y + 1)
        elif self.orientation == 'East':
            self.location.x = min(gridWidth-1, self.location.x + 1)
        elif self.orientation == 'South':
            self.location.y = max(0, self.location.y - 1)
        elif self.orientation == 'West':
            self.location.x = max(0, self.location.x - 1)
        else:
            raise Exception('orientation not within the set "North", "East", "South", "West"')

        self.hasBumped = temp == self.location

    def __str__(self):
        return "location - (%s, %s), orientation - %s, hasGold - %s, hasArrow - %s, isAlive - %s, hasBumped - %s" %(
            self.location.x, self.location.y, self.orientation, self.hasGold, self.hasArrow, self.isAlive, self.hasBumped
        )















