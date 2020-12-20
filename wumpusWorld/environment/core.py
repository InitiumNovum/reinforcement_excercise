import sys
from abc import ABCMeta, abstractmethod

class RewardTable:
    forward = -1
    turn = -1
    grab = -1
    shoot_with_arrow=-10
    shoot_without_arrow = -1
    climb_without_gold = -1
    climb_with_gold = 1000
    climb_in_wrong_location = -1
    died = -1000

#TODO may want to make this orientation class a child class from something more standard, such as the scipy.spatial.transform.Rotation class
class Orientation:
    """
    Specifies the orientation of the agent.
    I think I need to create an "Action class" which will act upon the "Orientation" class in order to change it's value.
    """

    def __init__(self, orientation='East'):
        self.orientations = ('North', 'East', 'South', 'West')
        #assert(set(self.orientation).issuperset({orientation}))
        self.orientation = orientation

    def turnLeft(self):
        idx = self.orientations.index(self.orientation)
        self.orientation = self.orientations[3] if idx-1 == -1 else self.orientations[idx-1]

    def turnRight(self):
        idx = self.orientations.index(self.orientation)
        self.orientation = self.orientations[0] if idx+1 == 4 else self.orientations[idx+1]

class IAction(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def __call__(environment, percept, agent):#(environment: Environment, percept: Percept, agent: Agent):
        """call interface"""

    def __str__(self):
        if type(self) == type(Forward()):
            this_type = "Forward"
        elif type(self) == type(TurnLeft()):
            this_type = "TurnLeft"
        elif type(self) == type(TurnRight()):
            this_type = "TurnRight"
        elif type(self) == type(Shoot()):
            this_type = "Shoot"
        elif type(self) == type(Grab()):
            this_type = "Grab"
        elif type(self) == type(Climb()):
            this_type = "Climb"
        else:
            this_type = ""
            raise Exception("No valid action type!")
        return this_type

class Forward(IAction):

    @staticmethod
    def __call__(environment, percept, agent):
        try:
            agent.forward(environment.gridWidth, environment.gridHeight)
        except:
            e = sys.exc_info()
            print(e)

        death = (environment.isWumpusAt(agent.location) and environment.wumpusAlive) or environment.isPitAt(agent.location)
        agent.isAlive = not death

        percept.stench = environment.isStench(agent.location)
        percept.breeze = environment.isBreeze(agent.location)
        percept.glitter = environment.isGlitter(agent.location)
        percept.bump = agent.hasBumped
        percept.scream = False
        percept.shoot_without_scream = False
        percept.isTerminated = not agent.isAlive
        environment.terminated = percept.isTerminated
        percept.reward = percept.reward + RewardTable.forward if agent.isAlive else percept.reward + RewardTable.forward + RewardTable.died

        return environment, percept, agent

class TurnLeft(IAction):
    def __init__(self):
        pass

    def __call__(self, environment, percept, agent):
        agent.turnLeft()
        agent.hasBumped = False
        percept.bump = agent.hasBumped
        percept.reward = percept.reward + RewardTable.turn

        return environment, percept, agent

class TurnRight(IAction):
    def __init__(self):
        pass

    def __call__(self, environment, percept, agent):
        agent.turnRight()
        agent.hasBumped = False
        percept.bump = agent.hasBumped
        percept.reward = percept.reward + RewardTable.turn
        return environment, percept, agent

class Shoot(IAction):
    def __init__(self):
        pass

    def __call__(self, environment, percept, agent):
        if agent.hasArrow:
            agent.hasBumped = False
            percept.bump = agent.hasBumped
            percept.scream = environment.killAttemptSuccessful(agent)
            environment.wumpusAlive = not percept.scream
            percept.shoot_without_scream = not percept.scream
            agent.hasArrow = False
            percept.reward = percept.reward + RewardTable.shoot_with_arrow
        else:
            agent.hasBumped = False
            percept.bump = agent.hasBumped
            percept.reward = percept.reward + RewardTable.shoot_without_arrow
        return environment, percept, agent

class Grab(IAction):
    def __init__(self):
        pass

    def __call__(self, environment, percept, agent):
        agent.hasBumped = False
        percept.bump = agent.hasBumped
        if not agent.hasGold: # enforces NOT DROPPING Gold
            agent.hasGold = environment.isGlitter(agent.location)
        percept.reward = percept.reward + RewardTable.grab
        return environment, percept, agent

class Climb(IAction):
    def __init__(self):
        pass

    def __call__(self, environment, percept, agent):
        agent.hasBumped = False
        percept.bump = agent.hasBumped
        inStartLocation = agent.location == Coords(0, 0)
        if not inStartLocation:
            percept.reward = percept.reward + RewardTable.climb_in_wrong_location
            percept.isTerminated = False
            environment.terminated = False
        elif agent.hasGold and inStartLocation:
            percept.reward = percept.reward + RewardTable.climb_with_gold
            percept.isTerminated = True
            environment.terminated = True
        elif environment.allowClimbWithoutGold and inStartLocation:
            percept.reward = percept.reward + RewardTable.climb_without_gold
            percept.isTerminated = True
            environment.terminated = True
        else:
            percept.isTerminated = False
            environment.terminated = False
            percept.reward = percept.reward + RewardTable.climb_in_wrong_location

        return environment, percept, agent

class Coords:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, coord):
        return coord.x == self.x and coord.y == self.y

