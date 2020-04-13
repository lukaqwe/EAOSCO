import os
import subprocess
import re

Mnemonics = []  # this list stores all mnemonics from all contracts
Entropy = {}  # dictionary containing nr of occurences per mnemonic


# returns only the mnemonics from the list of opcodes
def clean(opcodesList):
    mnemonic = re.compile("[A-Z]+[0-9]{0,2}")
    result = []
    for opcode in opcodesList:
        if mnemonic.match(opcode):
            result.append(opcode)
    return result


def collect():
    global Mnemonics
    for filename in os.listdir("contracts"):
        opcodes = subprocess.run(["evmasm", "-d", "-i", "contracts/" + filename],
                                 capture_output=True).stdout

        # returned value are in bytes format, string conversion necessary
        # first two chars and last one are redundant
        opcodes = [str(x)[2:-1] for x in opcodes.split()]

        # collect all mnemonics into a list
        for mnemonic in clean(opcodes):
            Mnemonics.append(mnemonic)


def count():
    global Mnemonics, Entropy
    for mnemonic in Mnemonics:
        if mnemonic not in Entropy:
            Entropy[mnemonic] = 1
        else:
            Entropy[mnemonic] += 1


if __name__ == "__main__":
    collect()
    count()
    print(Entropy)
