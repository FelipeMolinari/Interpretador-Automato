import numpy as np
import math
import copy
from Automato import Automato

class FactoryAutomato:

    def __init__(self, tag):
        self.nome = ""
        self.definicao = ""
        self.tag = tag