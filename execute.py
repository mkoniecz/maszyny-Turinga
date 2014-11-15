"""
executes specified Turing machine
"""

from collections import OrderedDict

"""
TM is represented by dictionary that expresses action table
(symbol, state) -> (new_symbol, new_state, direction)

Following states are special:
"yes" - accepting state
"no" - rejecting state
"start" - initial state

alphabet and set of states is implied by action table and supplied tape


tape is a String, with space as an empty symbol

initial tape is supplied as a String argument
initial head position is at start of String
"""


def pretty_print_machine(machine):
    for key in machine:
        print key, ' -> ', machine[key]


def execute(machine, tape, verbose=True):
    tape = list(tape)
    iteration_limit = 100
    iteration = 0
    state = "start"
    position = 0
    while True:
        if verbose:
            print "".join(tape)
            print " " * position + "^" + "   " + state + " -> ",
        symbol = tape[position]
        try:
            new_symbol, state, direction = machine[(symbol, state)]
            tape[position] = new_symbol
        except KeyError:
            state = "no"
        if verbose:
            print state

        if state == "yes":
            return
        if state == "no":
            return
        if iteration > iteration_limit:
            print "iteration limit reached"
            return

        if direction == "<":
            position -= 1
            if position == -1:
                tape = [" "] + tape
                position += 1
        elif direction == ">":
            position += 1
            if len(tape) == position:
                tape.append(" ")
        elif direction == "":
            pass
        else:
            raise ValueError


def example():
    # adding unary numbers separated by a blank
    unary = OrderedDict()
    unary[("1", "start")] = ("1", "start", ">")
    unary[(" ", "start")] = ("1", "break_found", ">")
    unary[("1", "break_found")] = ("1", "after_break", ">")
    unary[("1", "after_break")] = ("1", "after_break", ">")
    unary[(" ", "after_break")] = (" ", "end_found", "<")
    unary[("1", "end_found")] = ("1", "yes", "")
    unary_tape = "11 111"

    pretty_print_machine(unary)
    execute(unary, unary_tape)


