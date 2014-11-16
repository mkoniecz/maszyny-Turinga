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


def extend_tape_if_needed(position, tape):
    if position == -1:
        tape = [" "] + tape
        position += 1
    if len(tape) == position:
        tape.append(" ")
    return position, tape


def execute(machine, tape, verbose=True):
    tape = list(tape)
    iteration_limit = 100
    iteration = 0
    state = "start"
    position = 0
    while True:
        position, tape = extend_tape_if_needed(position, tape)
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
            return True
        if state == "no":
            return False
        if iteration > iteration_limit:
            if verbose:
                print "iteration limit reached"
            return None

        if direction == "<":
            position -= 1
        elif direction == ">":
            position += 1
        elif direction == "":
            pass
        else:
            raise ValueError


def get_alphabet(machine):
    alphabet = []
    for key in machine:
        symbol, _ = key
        if not symbol in alphabet:
            alphabet.append(symbol)
        new_symbol, _, _, = machine[key]
        if not new_symbol in alphabet:
            alphabet.append(new_symbol)
    return alphabet


def verify(machine, check_function, max_tape_len):
    alphabet = get_alphabet(machine)
    check_this_case(machine, check_function, "")
    verification_recurrency(machine, alphabet, max_tape_len, "", check_function, 0)


def check_this_case(machine, check_function, tape):
    tm_result = execute(machine, tape, verbose=False)
    check = check_function(tape)
    if (tm_result != check):
        print "for tape " + tape + " TM failed. Expected " + str(check) + ", TM returned " + str(tm_result)
    else:
        pass
        # print str(tm_result) + " " + str(check)
        #print "tape <" + tape + "> is OK"


def verification_recurrency(machine, alphabet, max_tape_len, tape_prefix, check_function, counter):
    if len(tape_prefix) == max_tape_len:
        return counter
    for letter in alphabet:
        if letter != " ":
            new_tape = list(tape_prefix)
            new_tape.append(letter)
            new_tape = "".join(new_tape)
            check_this_case(machine, check_function, new_tape)
            counter = verification_recurrency(machine, alphabet, max_tape_len, new_tape, check_function, counter)
    counter += 1
    if ((counter + 1) % 1000) == 0:
        pass
        # print str(counter/1000)+"k"
    return counter


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

