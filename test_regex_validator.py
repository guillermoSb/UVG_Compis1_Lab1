import pytest

from Automata import Automata

def test_regex_validator_parenthesis():
    # Arrange 
		infix = "(a*|bc"
		with pytest.raises(Exception): 
			Automata._check_regex(infix)


def test_regex_validator_operator_1():
    # Arrange 
		infix = "a++b"
		with pytest.raises(Exception): 
			Automata._check_regex(infix)


def test_regex_validator_operator_2():
    # Arrange 
		infix = "a+b|"
		with pytest.raises(Exception): 
			Automata._check_regex(infix)
		
			