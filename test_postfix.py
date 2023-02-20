
from Automata import Automata

def test_postfix():
    # Arrange 
		infix = "4+18/(9−3)"
		# Act
		postfix = Automata._from_regex(infix)
		# Assert
		assert postfix == "4 18 9 3 − / +"