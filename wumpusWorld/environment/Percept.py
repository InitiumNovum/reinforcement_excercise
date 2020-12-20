from wumpusWorld.environment.core import *
import wumpusWorld.environment.Environment as env

# TODO precept is a singleton, so see if you can enforce this constraint.
class Percept:
    def __init__(self, stench: bool, breeze: bool,
                 glitter: bool, bump: bool, scream: bool,
                 isTerminated: bool, reward: float):
        self.stench = stench
        self.breeze = breeze
        self.glitter = glitter
        self.bump = bump
        self.scream = scream
        self.shoot_without_scream = False # both "scream" and "shoot_without_scream" represent a "hearing" percept
        self.isTerminated = isTerminated
        self.reward = reward

    @staticmethod
    def create_Percept(isStench: bool,
                       isBreeze: bool,
                       isGlitter: bool):
        percept = Percept(isStench,
                          isBreeze,
                          isGlitter,
                          False,
                          False,
                          False,
                          0)
        return percept


    def show(self) -> dict:
        return {'stench': self.stench, 'breeze': self.breeze, 'glitter': self.glitter,
                'bump': self.bump, 'scream': self.scream, 'shoot_without_scream': self.shoot_without_scream,
                'isTerminated': self.isTerminated, 'reward': self.reward}

    # TODO bump needs history of movement, so maybe introduce the logic here?
    @property
    def bump(self) -> bool:
        return self._bump

    @bump.setter
    def bump(self, bump: bool):
        self._bump = bump

