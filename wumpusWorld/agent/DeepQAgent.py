from wumpusWorld.agent.BayesianAgentEfficient import *
from wumpusWorld.environment.Agent import *
from wumpusWorld.environment.Percept import *
import random
import networkx as nx
import math
import numpy as np

class DeepQAgent(BayesianAgentEfficient):
    #TODO clean up methods and add nn-model from notebooks
    def __init__(self, gridWidth=4, gridHeight=4, dangerThreshold=0.45, allowClimbWithoutGold=True):
        BayesianAgentEfficient.__init__(self, gridWidth, gridHeight, dangerThreshold, allowClimbWithoutGold)
