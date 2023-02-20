

class Automata:
		
		
		

		@classmethod
		def _postfix_from_regex(cls, regex):
				# Define precedences for regex operators
				operators = {
					'*': 1,
					'+': 1,
					'.': 2,
					'|': 3
				}
				# Stack for tokens
				token_stack = []
				# Stack for operators
				operator_stack = []
				# Regex to list
				regex_list = list(regex)
				# Start the Shuntingh Yard Algorithm

				# Implementation of the Shunting Yard Algorithm (https://brilliant.org/wiki/shunting-yard-algorithm/
				for token in regex_list:
					is_operator = token in operators.keys()
					if not is_operator:
						token_stack.append(token)
					elif token in ['(', ')']:
						if token == '(':
							operator_stack.append(token)
						else:
							while len(operator_stack) > 0 and operators[operator_stack[-1]] != '(':
								token_stack.append(operator_stack.pop())
							operator_stack.pop()	
					else:
						precedence = operators[token]
						while len(operator_stack) > 0 and operators[operator_stack[-1]] < precedence and operators[operator_stack[-1]] != '(':
							token_stack.append(operator_stack.pop()) 
						operator_stack.append(token)
				while len(operator_stack) > 0:
					token_stack.append(operator_stack.pop())	
				return ''.join(token_stack)	# The output is a string in postfix notation
				

