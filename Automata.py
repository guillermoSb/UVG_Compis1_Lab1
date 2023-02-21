

class Automata:
		
		# Define precedences for regex operators
		operators = {
			'*': 1,
			'+': 1,
			'.': 2,
			'|': 3
		}

		
		
		def __init__(self, regex):
				self._regex = regex
				self._postfix = self._postfix_from_regex(regex)
				self._states = self._states_from_postfix(self._postfix)

		def __init__(self, states, initial, final):
				self._states = states
				self._initial = initial
				self._final = final
		

		@classmethod
		def _states_from_postfix(cls, postfix):
			state_counter = 0
			postfix_stack = list(postfix)
			operation_stack = []
			while len(postfix_stack) > 0:
				token = postfix_stack.pop(0)
				if token in cls.operators.keys():
					if token == "*":
						operand = operation_stack.pop()
						new_states = {
									**operand._states, # Append the previous states
						}
						start_state = state_counter
						end_state = state_counter + 1
						
						new_states[start_state] = {'E': (operand._initial, end_state)}
						new_states[end_state] = {}
						if 'E' in operand._states[operand._final].keys():
							prev_transitions = operand._states[operand._final]['E']
						else:
							prev_transitions = tuple()
						
						new_transitions = prev_transitions + (operand._initial, end_state)
						
						new_states[operand._final] = {'E': new_transitions}
						state_counter += 2

						operation_stack.append(Automata(new_states, start_state, end_state))
					elif token == ".":
						operand_2 = operation_stack.pop()
						operand_1 = operation_stack.pop()
						new_states = {
									**operand_1._states,
									**operand_2._states,
						}
						# End state of operand 1 connects to start state of operand 2
						new_states[operand_1._final] = {'E': (operand_2._initial,)}

						operation_stack.append(Automata(new_states, operand_1._initial, operand_2._final))
						
				else:
					# Append a base Automata to the operation stack
					operation_stack.append(Automata({state_counter: {token: (state_counter + 1,)}, state_counter + 1: {}}, state_counter, state_counter + 1))
					state_counter += 2
			
			return operation_stack[0]


		@classmethod
		def _postfix_from_regex(cls, regex):
				
				# Stack for tokens
				token_stack = []
				# Stack for operators
				operator_stack = []
				# Regex to list
				regex_list = list(regex)
				# Start the Shuntingh Yard Algorithm

				# Implementation of the Shunting Yard Algorithm (https://brilliant.org/wiki/shunting-yard-algorithm/
				for token in regex_list:
					is_operator = token in cls.operators.keys()
					if not is_operator:
						token_stack.append(token)
					elif token in ['(', ')']:
						if token == '(':
							operator_stack.append(token)
						else:
							while len(operator_stack) > 0 and cls.operators[operator_stack[-1]] != '(':
								token_stack.append(operator_stack.pop())
							operator_stack.pop()	
					else:
						precedence = cls.operators[token]
						while len(operator_stack) > 0 and cls.operators[operator_stack[-1]] < precedence and cls.operators[operator_stack[-1]] != '(':
							token_stack.append(operator_stack.pop()) 
						operator_stack.append(token)
				while len(operator_stack) > 0:
					token_stack.append(operator_stack.pop())	
				return ''.join(token_stack)	# The output is a string in postfix notation
				

