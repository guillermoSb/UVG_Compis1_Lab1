from Automata import Automata
import networkx as nx
import matplotlib.pyplot as plt


a = Automata._from_regex('a+bc')
print(a._states)
