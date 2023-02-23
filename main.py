from Automata import Automata
from graphviz import Digraph


a = Automata._from_regex('a')

# create a new directed graph
dot = Digraph(graph_attr={'rankdir': 'LR'})

print(a._states)

# add nodes to the graph
for state in a._states.keys():
    if state == a._final:          
          dot.node('{}'.format(state), shape="doublecircle")
    elif  state == a._initial:          
          dot.node('{}'.format(state), shape="triangle")
    else:
          dot.node('{}'.format(state),)

for state in a._states.keys():
    for transition in a._states[state]:
            
            for to in a._states[state][transition]:
                    dot.edge('{}'.format(state), '{}'.format(to), label=transition)


print(a._final)
dot.render('automaton.gv', view=True)
