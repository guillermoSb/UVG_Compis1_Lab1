
from Automata import Automata

def test_postfix():
    # Arrange 
		infix = "a*|bc"
		# Act
		postfix = Automata._postfix_from_regex(infix)
		# Assert
		assert postfix == "a*bc.|"


