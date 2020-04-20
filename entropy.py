from gas import GasPerMnemonic
import os
import subprocess
import re

Mnemonics = []  # this list stores all mnemonics from all contracts
Total = 0  # nr of total mnemonics in selected contracts
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
    global Mnemonics, Entropy, Total
    Total = len(Mnemonics)
    for mnemonic in Mnemonics:
        if mnemonic not in Entropy:
            Entropy[mnemonic] = 1
        else:
            Entropy[mnemonic] += 1


def sort():
    global Entropy
    Entropy = {k: v for k, v in sorted(Entropy.items(), key=lambda item: item[1], reverse=True)}
    return Entropy


def getEntropy():
    collect()
    count()
    return sort()


def makeTable():
    Entropy = getEntropy()
    GasCost = GasPerMnemonic()
    result = '| Mnemonics| Occurences | Gas Cost | Gas Spent | \n  --- | --- | --- | --- \n'

    for key in Entropy:
        result += key + '|' + str(Entropy[key]) + '|'

        if key in GasCost[0]:
            result += str(GasCost[0][key]) + "|" + str(GasCost[0][key]*Entropy[key])
        elif key in GasCost[1]:
            result += str(GasCost[1][key]) + "|" + "N\A"
        result += '\n'

    return result


if __name__ == "__main__":
    print(makeTable())
