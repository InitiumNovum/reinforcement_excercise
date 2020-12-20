
from wumpusWorld.environment.Agent import *
from wumpusWorld.environment.Environment import *
import random

class NaiveAgent:#(Agent):

    def __init__(self):
        self.rand_gen = [random.randint(0, 5) for i in range(1000)]

    @staticmethod
    def create_Agent():
        return Agent(location=Coords(0,0),
                       orientation='East',
                       hasGold=False,
                       hasArrow=True,
                       isAlive=True)

    #@staticmethod
    def nextAction(self, percept: Percept, agent: Agent) -> IAction:
        #action = self.rand_gen[-1]
        #del self.rand_gen[-1]
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
