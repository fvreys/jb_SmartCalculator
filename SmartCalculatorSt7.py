""" Smart calculator """
from typing import Any
from collections import deque

global memory   # All variables
global commands, valid_operators
commands = ["/exit", "/help"]
valid_operators = ["+", "-", "*", "/", "(", ")"]   # Includes parentheses '(' and ')'


# TO DO: 1/ Simplify check expression 2/ OOP
# Command
def check_command(instruction: str) -> bool:
    """ Check for command in input """
    if instruction == "/exit":
        print("Bye!")
        exit()
    elif instruction == "/help":
        print("The program calculates '+', '-', '*' and '/' operators. " 
              "It must support unary and binary '-'. "
              "It should also support parentheses.")
    elif instruction[0] == "/" and instruction not in commands:
        print("Unknown command")
    else:  # No command
        return False
    return True


# Assignment
def evaluate_assignment(input_string: str) -> None:
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
            memory[target] = int(expression)
        elif expression.isalpha():
            if expression in memory.keys():
                memory[target] = memory[expression]
            else:
                print(f'Unknown variable')
    return None


# Only a variable
def show_variable(entry: str) -> bool:
    """ If only one string, print value string """
    # print(entry)
    if entry.isalpha():
        if entry in memory.keys():
            print(memory[entry])
            return True
        else:
            print(f"Unknown variable")
            return True
    else:
        return False


# Expression
def validate_formula(elements: list) -> list:
    """ Replaces variables and validate operands  """
    simple_elements: list = []
    for text in elements:
        if text.isnumeric():
            simple_elements.append(text)
        elif text.isalpha():
            simple_elements.append(str(memory[text]))
        else:
            if text in valid_operators:
                simple_elements.append(text)
            else:
                # No valid formula_operand
                print(f"Invalid expression")
                simple_elements = []  # return value to make sure error is printed only once
                break
    return simple_elements


def has_higher_precedence(op1: str, op2: str):
    """ precondition: op1 in valid_operators, without['(', ')']
    result: True of op1 has higher priority then op2 (not equal or lower) """
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


def check_expression(input_string: str) -> None:
    """ Evaluate expression and provide result """
    # Expression can be split with and without spaces in expression
    # and remove duplicate '+' or '-'
    # TO DO: 1/ Make simpler 2/ split in different functions
    input_reduced: str = input_string.replace(" ", "")
    input_reduced = input_reduced.replace("+++", "+").replace("++", "+")
    input_reduced = input_reduced.replace("---", "-").replace("--", "+")
    if "**" in input_reduced or "//" in input_reduced:
        print(f"Invalid expression")
        return None
    input_spaces: str = ""
    for x in input_reduced:
        input_spaces += x if x not in valid_operators else f" {x} "
    formula: list = input_spaces.split()

    # Infix to postfix
    my_stack: deque[Any] = deque()
    postfix: list = []
    for elem in formula:
        # elem is an operand (integer value or variable)
        if elem not in valid_operators:
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

    # Postfix to result
    my_stack2: deque[Any] = deque()

    for elem2 in postfix:
        if elem2.isdecimal():
            my_stack2.append(elem2)
        elif elem2.isalpha():
            if elem2 in memory.keys():
                my_stack2.append(memory[elem2])
            else:  # Should be covered in show_variable
                print(f"Unknown variable")
        elif elem2 in valid_operators:
            nr1, nr2 = my_stack2.pop(), my_stack2.pop()
            result_operation: int = 0
            if elem2 == "+":
                result_operation = int(nr2) + int(nr1)
            elif elem2 == "-":
                result_operation = int(nr2) - int(nr1)
            elif elem2 == "*":
                result_operation = int(nr2) * int(nr1)
            elif elem2 == "/":
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


def smart_calculator():
    """ Main program """
    global memory
    memory = {}  # Initialize empty memory of variables

    while True:
        entry: str = input()
        if len(entry) == 0:
            continue
        elif check_command(entry):
            continue
        elif "=" in entry:
            evaluate_assignment(entry)
        elif show_variable(entry):   # variable to print
            continue
        else:
            check_expression(entry)


smart_calculator()
