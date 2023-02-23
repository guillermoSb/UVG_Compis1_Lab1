

class Automata:
		
		# Define precedences for regex operators
		operators = {
			'*': 1,
			'+': 1,
			'?': 1,
			'.': 2,
			'|': 3
		}

		
		
		@classmethod
		def _from_regex(self, regex):		
				"""Creates an Automata from a regex"""

				self._regex = regex.replace(' ', '')	# Remove spaces from the regex
				self._check_regex(regex)	# Check that the regex is valid
				self._postfix = self._postfix_from_regex(regex)	# Convert the regex to postfix
				return self._states_from_postfix(self._postfix)	# Create the states for the automaton

		def __init__(self, states, initial, final):
				"""Constructor for the Automata class"""				
				self._states = states
				self._initial = initial
				self._final = final
		
		@classmethod
		def _check_regex(cls, regex):
			"""Checks that the regex is valid, throws an error if invalid."""
			# Check that the regex has the same number of opening and closing parentheses
			if regex.count('(') != regex.count(')'):
				raise Exception("[REGEX ERROR] The regex has a different number of opening and closing parentheses.")
			
			# Check that there are no two operators in a row
			for i in range(0, len(regex)):

				if regex[i] in cls.operators.keys() and i < len(regex) - 1:
					if regex[i+1] in ['*', '?', '+']:
						raise Exception("[REGEX ERROR] There are two operators in a row.")			
			
			# The last character of the regex cannot be an | operator
			if regex[-1] in ['|']:
				raise Exception("[REGEX ERROR] The last character of the regex cannot be the | operator.")
			
			# The first character of the regex cannot be an | operator
			if regex[0] in cls.operators:
				raise Exception("[REGEX ERROR] The first character of the regex cannot be an operator.")

			# The first character of the regex cannot be an uniary operator
			if regex[0] in ['*', '?', '+']:
				raise Exception("[REGEX ERROR] The first character of the regex cannot be an uniary operator.")
				

		@classmethod
		def _states_from_postfix(cls, postfix):
			"""Creates the staes for the automata from a postfix expression"""
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
						# Create two new states
						start_state = state_counter
						end_state = state_counter + 1
						# Create the transitions between the new states
						new_states[start_state] = {'ε': (operand._initial, end_state)}
						new_states[end_state] = {}
						# Keep epsilon transitions from the previous final state
						if 'ε' in operand._states[operand._final].keys():
							prev_transitions = operand._states[operand._final]['ε']
						else:
							prev_transitions = tuple()
						
						new_transitions = prev_transitions + (operand._initial, end_state)
						# Add the new epsilon transition to the final state
						new_states[operand._final] = {
							**new_states[operand._final],
							**{'ε': new_transitions}
						}
						state_counter += 2
						operation_stack.append(Automata(new_states, start_state, end_state))
					elif token == "+":
						operand = operation_stack.pop()	
						new_states = {
									**operand._states, # Append the previous states
						}
						# Create the new states
						start_state = state_counter
						end_state = state_counter + 1
						# Cerate the epsilon transition between the start state and the initial state
						new_states[start_state] = {'ε': (operand._initial,)}
						new_states[end_state] = {}
						if 'ε' in operand._states[operand._final].keys():
							prev_transitions = operand._states[operand._final]['ε']
						else:
							prev_transitions = tuple()
						
						# Add an epsilon transition that goes from the initial state to the end state
						new_transitions = prev_transitions + (operand._initial, end_state)
						
						new_states[operand._final] = {
							**new_states[operand._final],
							**{'ε': new_transitions}
						}
						state_counter += 2

						operation_stack.append(Automata(new_states, start_state, end_state))
					elif token == ".":
						operand_2 = operation_stack.pop()
						operand_1 = operation_stack.pop()
						# Keep the operands states
						new_states = {
									**operand_1._states,
									**operand_2._states,
						}
						# End state of operand 1 connects to start state of operand 2
						new_states[operand_1._final] = {'ε': (operand_2._initial,)}

						operation_stack.append(Automata(new_states, operand_1._initial, operand_2._final))
					elif token == "?":
						operand_1 = operation_stack.pop()
						# Keep the operands states
						new_states = {
									**operand_1._states,
						}
						# Create the new states
						start_state = state_counter
						end_state = state_counter + 1
						# Create the epsilon transitions between the new states - the initial state can go to the end state
						new_states[start_state] = {'ε': (operand_1._initial, end_state)}
						new_states[end_state] = {}
						# Keep epsilon transitions from the previous final state
						if 'ε' in operand_1._states[operand_1._final].keys():
							prev_transitions_1 = operand_1._states[operand_1._final]['ε']
						else:
							prev_transitions_1 = tuple()
						new_states[operand_1._final] = {
							**new_states[operand_1._final],
							**{'ε': (end_state,) + prev_transitions_1}
						}
						state_counter += 2
						operation_stack.append(Automata(new_states, start_state, end_state))	
					elif token == "|":
						operand_2 = operation_stack.pop()
						operand_1 = operation_stack.pop()
						# Keep the operands states
						new_states = {
									**operand_1._states,
									**operand_2._states,
						}
						# Create the new states
						start_state = state_counter
						end_state = state_counter + 1
						# Create the epsilon transitions between the new states
						new_states[start_state] = {'ε': (operand_1._initial, operand_2._initial)}
						new_states[end_state] = {}
						# Keep epsilon transitions
						if 'ε' in operand_1._states[operand_1._final].keys():
							prev_transitions_1 = operand_1._states[operand_1._final]['ε']
						else:
							prev_transitions_1 = tuple()
						# Keep epsilon transitions
						if 'ε' in operand_2._states[operand_2._final].keys():
							prev_transitions_2 = operand_2._states[operand_2._final]['ε']
						else:
							prev_transitions_2 = tuple()
						# Add the new epsilon transitions
						new_states[operand_1._final] = {
							**new_states[operand_1._final],
							**{'ε': (end_state,) + prev_transitions_1}
						}
						new_states[operand_2._final] = {
							**new_states[operand_2._final],
							**{'ε': (end_state,) + prev_transitions_2}
						}
						state_counter += 2
						operation_stack.append(Automata(new_states, start_state, end_state))	
				else:
					# Append a base Automata to the operation stack, this state has two initial states with a connection between them
					operation_stack.append(Automata({state_counter: {token: (state_counter + 1,)}, state_counter + 1: {}}, state_counter, state_counter + 1))
					state_counter += 2
			
			return operation_stack[0]


		@classmethod
		def _postfix_from_regex(cls, regex):
				"""Converts a regex from postfix"""
				# Add the . to the regex to handle concatenation
				# TODO: Check how to handle concatenation without any special character
				i = 0
				while i < len(regex):
					if regex[i] not in ['|', '(', '.'] and i < len(regex) - 1:
						if regex[i + 1] not in cls.operators and regex[i + 1] != ')':
							regex = regex[:i + 1] + '.' + regex[i + 1:]
					i += 1
				
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
					if not is_operator and token not in ['(', ')']:
						token_stack.append(token)	# For simple tokens, just append them to the stack
					elif token in ['(', ')']:
						if token == '(':
							operator_stack.append(token)
						else:
							# Pop all operators until the matching parenthesis is found
							while len(operator_stack) > 0 and operator_stack[-1] != '(':
								token_stack.append(operator_stack.pop())
							operator_stack.pop()	
					else:
						precedence = cls.operators[token]	# The precedence helps to determine which order the operators are evaluated	
						while len(operator_stack) > 0:
							if operator_stack[-1] == "(":
								break	# Don't to anything if the last operator is a parenthesis
							if not cls.operators[operator_stack[-1]] < precedence:
								break	# Don't do anything if the last operator has a higher precedence
							token_stack.append(operator_stack.pop()) 	# Append the last operator to the token stack
						operator_stack.append(token)	# Append the current operator to the operator stack
				while len(operator_stack) > 0:
					token_stack.append(operator_stack.pop()) # Last part of the algorithm: append remaining operators to the token stack
				return ''.join(token_stack)	# The output is a string in postfix notation
				
