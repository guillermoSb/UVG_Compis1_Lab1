from Automata import Automata
import networkx as nx
import matplotlib.pyplot as plt


a = Automata._from_regex('a*')

G = nx.DiGraph()




for s in a._states.keys():
		for t in a._states[s].keys():
				e = []
				for d in a._states[s][t]:
					e.append((s, d))
					G.add_edges_from([(s,d)], label=t)

color_map = []

for node in G:
	if node == a._initial:
		color_map.append('red')
	elif node == a._final:
		color_map.append('yellow')
	else:
		color_map.append('blue')


pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels=True, node_color=color_map, edge_color='black', width=1, alpha=0.7)
nx.draw_networkx_edge_labels(G, pos)

plt.show()