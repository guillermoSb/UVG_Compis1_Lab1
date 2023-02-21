from Automata import Automata

def test_thompson_concat():
	 # Arrange 
		postfix = "ab."
		# Act
		states = Automata._states_from_postfix(postfix)._states
		# Assert
		print(states)
		assert states[0] == {'a': (1,)}
		assert states[1] == {'E': (2,)}
		assert states[2] == {'b': (3,)}
		assert states[3] == {}
		assert len(states.keys()) == 4

def test_thompson_union():
	 # Arrange 
		postfix = "ab|"
		# Act
		states = Automata._states_from_postfix(postfix)._states
		# Assert	
		assert len(states.keys()) == 6

def test_thompson_closure():
    # Arrange 
		postfix = "a*"
		# Act
		states = Automata._states_from_postfix(postfix)._states
		# Assert
		assert len(states.keys()) == 4
		
