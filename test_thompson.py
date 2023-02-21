from Automata import Automata

def test_thompson_1():
    # Arrange 
		postfix = "a*"
		# Act
		states = Automata._states_from_postfix(postfix)
		# Assert
		assert len(states.keys()) == 4
		

