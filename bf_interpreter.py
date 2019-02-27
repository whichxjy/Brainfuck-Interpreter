import sys
import argparse
from array import array

def main():
    parser = argparse.ArgumentParser(description='Brainfuck interpreter')
    parser.add_argument('-f', '--file', type=str, help='Brainfuck program file')
    args = parser.parse_args()

    with open(args.file) as fp:
        keywords = {'>', '<', '+', '-', '.', ',', '[', ']'}
        program = array('u', (char for char in fp.read() if char in keywords))
        execute(program)

def execute(program):
    """Execute the program"""
    cells = [0]
    ptr = 0     # point to current cell
    pc = 0      # point to current command
    jump_map = get_jump_map(program)

    while pc < len(program):
        command = program[pc]
        if command == '>':
            ptr += 1
            if ptr == len(cells):
                cells.append(0)
        elif command == '<':
            ptr -= 1
        elif command == '+':
            cells[ptr] += 1
        elif command == '-':
            cells[ptr] -= 1
        elif command == '.':
            sys.stdout.write(chr(cells[ptr]))
            sys.stdout.flush()
        elif command == ',':
            cells[ptr] = ord(sys.stdin.read(1))
        elif command == '[':
            if cells[ptr] == 0:
                pc = jump_map[pc]
                continue
        elif command == ']':
            if cells[ptr] != 0:
                pc = jump_map[pc]
                continue
        pc += 1

def get_jump_map(program):
    """Return a jump map for brackets command('[' and ']')"""
    stack = []
    jump_map = {}
    pc = 0      # point to current command

    while pc < len(program):
        command = program[pc]
        if command == '[':
            stack.append(pc)
        elif command == ']':
            # Left bracket pointer
            left_bracket = stack.pop()
            # Right bracket pointer
            right_bracket = pc
            jump_map[left_bracket] = right_bracket + 1
            jump_map[right_bracket] = left_bracket + 1
        pc += 1

    return jump_map

if __name__ == "__main__":
    main()
