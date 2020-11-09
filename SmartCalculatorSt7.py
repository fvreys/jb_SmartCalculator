""" Smart calculator - OOP version"""
from typing import Any
from collections import deque


# Static methods
def has_higher_precedence(op1: str, op2: str):
    """ precondition: op1 in valid_operators, without['(', ')']
    result: True if op1 has higher priority then op2 (not equal or lower) """
    if op1 in ["*", "/"]:
        if op2 in ["+", "-"]:
            return True
        else:
            return False
    else:
        return False


def has_lower_precedence(op1: str, op2: str):
    """ precondition: op1 in valid_operators, without ['(', ')']
    result: True if op1 has lower priority then op2 (not equal or lower) """
    if op1 in ["+", "-"]:
        if op2 in ["*", "/"]:
            return True
        else:
            return False
    else:
        return False


class Calculator:
    def __init__(self, commands, operators):
        self.memory = {}
        self.commands = commands    # ["/exit", "/help"]
        self.valid_operators = operators     # ["+", "-", "*", "/", "(", ")"]   Includes parentheses '(' and ')'

    # Command
    def check_command(self, instruction: str) -> bool:
        """ Check for command in input """
        if instruction == "/exit":
            print("Bye!")
            exit()
        elif instruction == "/help":
            print("The program calculates '+', '-', '*' and '/' operators. " 
                  "It must support unary and binary '-'. "
                  "It should also support parentheses.")
        elif instruction[0] == "/" and instruction not in self.commands:
            print("Unknown command")
        else:  # No command
            return False
        return True

    # Assignment
    def evaluate_assignment(self, input_string: str) -> None:
        """ Checks on assignment and update memory storage with new values
        Precondition: input_string contains minimal one '='
        """
        try:
            target, expression = input_string.replace(" ", "").split("=")
        except ValueError:
            # More then 1 '='
            print(f'Invalid assignment')
        else:
            if not target.isalpha():
                print(f'Invalid identifier')
            elif expression.isnumeric():
                self.memory[target] = int(expression)
            elif expression.isalpha():
                if expression in self.memory.keys():
                    self.memory[target] = self.memory[expression]
                else:
                    print(f'Unknown variable')
        return None

    # Only a variable
    def show_variable(self, entry: str) -> bool:
        """ If only one string, print value string """
        if entry.isalpha():
            if entry in self.memory.keys():
                print(self.memory[entry])
                return True
            else:
                print(f"Unknown variable")
                return True
        else:
            return False

    # Expression
    def validate_formula(self, elements: list) -> list:
        """ Replaces variables and validate operands  """
        simple_elements: list = []
        for text in elements:
            if text.isnumeric():
                simple_elements.append(text)
            elif text.isalpha():
                simple_elements.append(str(self.memory[text]))
            else:
                if text in self.valid_operators:
                    simple_elements.append(text)
                else:
                    # No valid formula_operand
                    print(f"Invalid expression")
                    simple_elements = []  # return value to make sure error is printed only once
                    break
        return simple_elements

    def parse_to_postfix(self, formula: list) -> list:
        """ returns: Change infix expression 'formula' into a postfix (or RPN) expression """
        my_stack: deque[Any] = deque()
        postfix: list = []
        for elem in formula:
            # elem is an operand (integer value or variable)
            if elem not in self.valid_operators:
                postfix.append(elem)
            # elem is an operator
            elif elem not in ["(", ")"]:
                if len(my_stack) == 0 or my_stack[-1] == "(":
                    my_stack.append(elem)
                elif has_higher_precedence(elem, my_stack[-1]):
                    my_stack.append(elem)
                else:
                    stack_elem = my_stack.pop()
                    postfix.append(stack_elem)
                    while len(my_stack) > 0 and not(has_lower_precedence(elem, my_stack[-1]) or my_stack[-1] == "("):
                        # ?? LOWER precedence == lower or EQUAL ?
                        stack_elem: object = my_stack.pop()
                        postfix.append(stack_elem)
                    my_stack.append(elem)
            # elem is ( or  )
            elif elem == "(":
                my_stack.append(elem)
            else:  # ")
                while len(my_stack) > 0 and not(my_stack[-1] == "("):
                    stack_elem: object = my_stack.pop()
                    postfix.append(stack_elem)
                if len(my_stack) > 0 and my_stack[-1] == "(":
                    my_stack.pop()   # Remove ( also from stack
                else:
                    print(f"Invalid expression")

        while len(my_stack) != 0:
            stack_elem = my_stack.pop()
            if stack_elem not in ["(", ")"]:
                postfix.append(stack_elem)
            else:
                print(f"Invalid expression")

        return postfix

    def calculate_postfix(self, postfix_result: list) -> None:
        my_stack2: deque[Any] = deque()

        for el in postfix_result:
            if el.isdecimal():
                my_stack2.append(el)
            elif el.isalpha():
                if el in self.memory.keys():
                    my_stack2.append(self.memory[el])
                else:  # Should be covered in show_variable
                    print(f"Unknown variable")
            elif el in self.valid_operators:
                nr1, nr2 = my_stack2.pop(), my_stack2.pop()
                result_operation: int = 0
                if el == "+":
                    result_operation = int(nr2) + int(nr1)
                elif el == "-":
                    result_operation = int(nr2) - int(nr1)
                elif el == "*":
                    result_operation = int(nr2) * int(nr1)
                elif el == "/":
                    try:
                        result_operation = int(nr2) // int(nr1)
                    except ZeroDivisionError:
                        print(f"Invalid expression")
                        return None

                my_stack2.append(result_operation)

        # Result is last element in stack
        if len(my_stack2) > 0:
            print(my_stack2.pop())  # Result should be integer

        return None

    def check_expression(self, input_string: str) -> None:
        """ Evaluate expression and provide result """
        # Expression can be split with and without spaces in expression, and remove duplicate '+' or '-'
        input_reduced: str = input_string.replace(" ", "")
        input_reduced = input_reduced.replace("+++", "+").replace("++", "+")
        input_reduced = input_reduced.replace("---", "-").replace("--", "+")
        if "**" in input_reduced or "//" in input_reduced:
            print(f"Invalid expression")
            return None
        input_spaces: str = ""
        for x in input_reduced:
            input_spaces += x if x not in self.valid_operators else f" {x} "
        infix_expression: list = input_spaces.split()

        # Infix to postfix
        postfix: list = self.parse_to_postfix(infix_expression)

        # Postfix to result
        self.calculate_postfix(postfix)

        return None


def smart_calculator():
    """ Main program """
    calc = Calculator(["/exit", "/help"], ["+", "-", "*", "/", "(", ")"])
    while True:
        entry: str = input()
        if len(entry) == 0:
            continue
        elif calc.check_command(entry):
            continue
        elif "=" in entry:
            calc.evaluate_assignment(entry)
        elif calc.show_variable(entry):   # variable to print
            continue
        else:
            calc.check_expression(entry)


smart_calculator()
