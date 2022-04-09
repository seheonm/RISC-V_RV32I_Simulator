# CS2303 Project 1- RISC-V RV32I_ Simulator
# By: Marina Seheon, Ahmad Shalaby, Toqa Bahaa

# Main is responsible for the program

import re
import sys

# Registers and Program Counter
dictRegisters = {'xpc': 0}
dictMemory = {}

# File being read in from file called program.txt
# TODO: Take the file name from the command line argument, instead of hard coded (at the end of all our coding)
f = open("program.txt", "r")
program = list(filter(None, f.read().splitlines()))
f.close()

programLine = program[dictRegisters['xpc']]

# TODO: Figure out halting instructions to put and replace the 'halt' in the while loop (at the end of all our coding)
while programLine.lower() != 'halt':
    incrementPC = True
    # Picks up new line, parses it and sorts into command and operands
    instruction = list(filter(None, re.split(',| ', programLine.strip())))
    # Functions
    if instruction[0].lower() == 'add':
        dictRegisters[instruction[1]] = dictRegisters[instruction[2]] + dictRegisters[instruction[3]]
    elif instruction[0].lower() == 'sub':
        dictRegisters[instruction[1]] = dictRegisters[instruction[2]] - dictRegisters[instruction[3]]
    elif instruction[0].lower() == 'lui':
        dictRegisters[instruction[1]] = int(instruction[2])
    elif instruction[0].lower() == 'or':
        dictRegisters[instruction[1]] = dictRegisters[instruction[2]] or dictRegisters[instruction[3]]
    elif instruction[0].lower() == 'and':
        dictRegisters[instruction[1]] = dictRegisters[instruction[2]] and dictRegisters[instruction[3]]
    elif instruction[0].lower() == 'lw':
        memoryAddressOffset = int(instruction[2].split('(')[0])
        memoryAddressRegister = instruction[2].split('(')[1].strip(')')
        wordArray = [
            dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset],
            dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset + 1],
            dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset + 2],
            dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset + 3]
        ]
        dictRegisters[instruction[1]] = int.from_bytes(wordArray, sys.byteorder, signed=True)
    elif instruction[0].lower() == 'lh':
        memoryAddressOffset = int(instruction[2].split('(')[0])
        memoryAddressRegister = instruction[2].split('(')[1].strip(')')
        wordArray = [
            dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset],
            dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset + 1]
        ]
        dictRegisters[instruction[1]] = int.from_bytes(wordArray, sys.byteorder, signed=True)
    elif instruction[0].lower() == 'lb':
        memoryAddressOffset = int(instruction[2].split('(')[0])
        memoryAddressRegister = instruction[2].split('(')[1].strip(')')
        dictRegisters[instruction[1]] = dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset]
    elif instruction[0].lower() == 'sw':
        memoryAddressOffset = int(instruction[2].split('(')[0])
        memoryAddressRegister = instruction[2].split('(')[1].strip(')')
        wordArray = list(dictRegisters[instruction[1]].to_bytes(4, sys.byteorder, signed=True))
        dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset] = wordArray[0]
        dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset + 1] = wordArray[1]
        dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset + 2] = wordArray[2]
        dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset + 3] = wordArray[3]
    elif instruction[0].lower() == 'sh':
        memoryAddressOffset = int(instruction[2].split('(')[0])
        memoryAddressRegister = instruction[2].split('(')[1].strip(')')
        wordArray = list(dictRegisters[instruction[1]].to_bytes(2, sys.byteorder, signed=True))
        dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset] = wordArray[0]
        dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset + 1] = wordArray[1]
    elif instruction[0].lower() == 'sb':
        memoryAddressOffset = int(instruction[2].split('(')[0])
        memoryAddressRegister = instruction[2].split('(')[1].strip(')')
        dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset] = dictRegisters[instruction[1]]

    # Debugging- part of Bonus 4
    elif instruction[0].lower() == 'printr':   # Print Register
        print(dictRegisters[instruction[1]])
    elif instruction[0].lower() == 'printw':   # Print Word from memory
        memoryAddressOffset = int(instruction[1].split('(')[0])
        memoryAddressRegister = instruction[1].split('(')[1].strip(')')
        wordArray = [
            dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset],
            dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset + 1],
            dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset + 2],
            dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset + 3]
        ]
        print(int.from_bytes(wordArray, sys.byteorder, signed=True))
    elif instruction[0].lower() == 'printh':   # Print Half-word from memory
        memoryAddressOffset = int(instruction[1].split('(')[0])
        memoryAddressRegister = instruction[1].split('(')[1].strip(')')
        wordArray = [
            dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset],
            dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset + 1]
        ]
        print(int.from_bytes(wordArray, sys.byteorder, signed=True))
    elif instruction[0].lower() == 'printb':   # Print Byte from memory
        memoryAddressOffset = int(instruction[1].split('(')[0])
        memoryAddressRegister = instruction[1].split('(')[1].strip(')')
        print(dictMemory[dictRegisters[memoryAddressRegister] + memoryAddressOffset])

    if incrementPC and dictRegisters['xpc'] < len(program) - 1:
        dictRegisters['xpc'] += 1
        programLine = program[dictRegisters['xpc']]

dictRegisters['xpc'] = 0


