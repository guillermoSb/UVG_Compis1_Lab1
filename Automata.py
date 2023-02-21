

class Automata:
		
		# Define precedences for regex operators
		operators = {
			'*': 1,
			'+': 1,
			'.': 2,
			'|': 3
		}

		
		@classmethod
		def _from_regex(self, regex):
				self._regex = regex
				self._check_regex(regex)
				self._postfix = self._postfix_from_regex(regex)
				return self._states_from_postfix(self._postfix)


		
		def __init__(self, states, initial, final):
				self._states = states
				self._initial = initial
				self._final = final
		
		@classmethod
		def _check_regex(cls, regex):
			# Check that the regex has the same number of opening and closing parentheses
			if regex.count('(') != regex.count(')'):
				raise Exception("[REGEX ERROR] The number of opening and closing parentheses is not the same.")
			
			# Check that there are no two operators in a row
			for i in range(0, len(regex)):

				if regex[i] in cls.operators.keys() and i < len(regex) - 1:
					if regex[i+1] in cls.operators.keys():
						raise Exception("[REGEX ERROR] There are two operators in a row.")			
			
			# The last character of the regex cannot be an operator
			if regex[-1] in ['|']:
				raise Exception("[REGEX ERROR] The last character of the regex cannot be the | operator.")
			

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
						
						new_states[start_state] = {'ε': (operand._initial, end_state)}
						new_states[end_state] = {}
						if 'ε' in operand._states[operand._final].keys():
							prev_transitions = operand._states[operand._final]['ε']
						else:
							prev_transitions = tuple()
						
						new_transitions = prev_transitions + (operand._initial, end_state)
						
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
						start_state = state_counter
						end_state = state_counter + 1
						
						new_states[start_state] = {'ε': (operand._initial)}
						new_states[end_state] = {}
						if 'ε' in operand._states[operand._final].keys():
							prev_transitions = operand._states[operand._final]['ε']
						else:
							prev_transitions = tuple()
						
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
						new_states = {
									**operand_1._states,
									**operand_2._states,
						}
						# End state of operand 1 connects to start state of operand 2
						new_states[operand_1._final] = {'ε': (operand_2._initial,)}

						operation_stack.append(Automata(new_states, operand_1._initial, operand_2._final))
					elif token == "|":
						operand_2 = operation_stack.pop()
						operand_1 = operation_stack.pop()
						new_states = {
									**operand_1._states,
									**operand_2._states,
						}
						start_state = state_counter
						end_state = state_counter + 1
						new_states[start_state] = {'ε': (operand_1._initial, operand_2._initial)}
						new_states[end_state] = {}

						if 'ε' in operand_1._states[operand_1._final].keys():
							prev_transitions_1 = operand_1._states[operand_1._final]['ε']
						else:
							prev_transitions_1 = tuple()

						if 'ε' in operand_2._states[operand_2._final].keys():
							prev_transitions_2 = operand_2._states[operand_2._final]['ε']
						else:
							prev_transitions_2 = tuple()

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
					# Append a base Automata to the operation stack
					operation_stack.append(Automata({state_counter: {token: (state_counter + 1,)}, state_counter + 1: {}}, state_counter, state_counter + 1))
					state_counter += 2
			
			return operation_stack[0]


		@classmethod
		def _postfix_from_regex(cls, regex):
				
				# Add the . to the regex
				for i in range(0, len(regex)):
					if regex[i] not in ['|', '(', '.'] and i < len(regex) - 1:
						if regex[i + 1] not in cls.operators and regex[i + 1] != ')':
							regex = regex[:i + 1] + '.' + regex[i + 1:]
				
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
						token_stack.append(token)
					elif token in ['(', ')']:
						if token == '(':
							operator_stack.append(token)
						else:
							while len(operator_stack) > 0 and operator_stack[-1] != '(':
								token_stack.append(operator_stack.pop())
							operator_stack.pop()	
					else:
						precedence = cls.operators[token]
				
						while len(operator_stack) > 0:
							if operator_stack[-1] == "(":
								break
							if not cls.operators[operator_stack[-1]] < precedence:
								break
							token_stack.append(operator_stack.pop()) 
						operator_stack.append(token)
				while len(operator_stack) > 0:
					token_stack.append(operator_stack.pop())	
				return ''.join(token_stack)	# The output is a string in postfix notation
				

