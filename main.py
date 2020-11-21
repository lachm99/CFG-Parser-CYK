"""This module is the entry point to your assignment. There is some scaffolding
to help you get started. It will call the appropriate method and load the input
data. You can edit or remove as much of this code as you wish to."""

from parser import Parser
from sys import stdin
from cfg import *

def membership(parser):
    """For each string, decide if it is in the language."""
    cfg = parser.parse_cfg()
    test_strings = parser.parse_test_strings()
    for in_string in test_strings:
        table = cfg.generateTable(in_string)
        print("1") if cfg.checkMembership(table) else print("0")
    print("end")

def rightmost_derivation(parser):
    """Print a rightmost derivation of the string."""
    cfg = parser.parse_cfg()
    test_string = parser.parse_test_string()
    table = cfg.generateTable(test_string)
    cfg.printRightmostDerivation(table)
    print("end")

def ambiguous(parser):
    """For each string, decide if it is ambiguous in this grammar."""
    cfg = parser.parse_cfg()
    test_strings = parser.parse_test_strings()
    for test_string in test_strings:
        table = cfg.generateTable(test_string)
        ambiguous = cfg.checkAmbiguity(table)
        print("1") if ambiguous else print("0")
    print("end")


if __name__ == '__main__':

    parser = Parser()
    command = parser.parse_command()

    if command == 'membership':
        membership(parser)
    elif command == 'rightmost-derivation':
        rightmost_derivation(parser)
    elif command == 'ambiguous':
        ambiguous(parser)
    else:
        print(f'Command {repr(command)} not recognised.')

