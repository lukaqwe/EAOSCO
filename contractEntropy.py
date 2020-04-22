# this file computes number of occurences per operation for each contract
import re
import os
import subprocess
import csv


# returns only the mnemonics from the list of opcodes
def clean(opcodesList):
    mnemonic = re.compile("[A-Z]+[0-9]{0,2}")
    result = []
    for opcode in opcodesList:
        if mnemonic.match(opcode):
            result.append(opcode)
    return result


def collect():
    ContractEntr = {}  # dict of format { contract -> { opcode -> occurences } }

    for filename in os.listdir("contracts"):
        Mnemonics = {}
        opcodes = subprocess.run(["evmasm", "-d", "-i", "contracts/" + filename],
                                 capture_output=True).stdout

        # returned value are in bytes format, string conversion necessary
        # first two chars and last one are redundant
        opcodes = [str(x)[2:-1] for x in opcodes.split()]

        # calculate each occurence per mnemonic
        for mnemonic in clean(opcodes):
            if mnemonic not in Mnemonics:
                Mnemonics[mnemonic] = 1
            else:
                Mnemonics[mnemonic] += 1

        # last 4 chars in the filename are redundant
        ContractEntr[filename[:-4]] = Mnemonics
    return ContractEntr


def makeCsv():
    ContractEntr = collect()
    Mnemonics = set()  # collecting all mnemonics for header
    with open("opcode-gas-costs.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == 'PUSH*':
                for i in range(1, 33):
                    Mnemonics.add(row[1][:-1] + str(i))
            elif row[1] == 'DUP*' or row[1] == 'SWAP*':
                for i in range(1, 17):
                    Mnemonics.add(row[1][:-1] + str(i))
            else:
                Mnemonics.add(row[1])
    Mnemonics = sorted(list(Mnemonics))

    with open("contract-entropy.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["ADDRESS"] + Mnemonics)  # header

        for contract in ContractEntr:
            row = [contract]
            for mnemonic in Mnemonics:
                if mnemonic in ContractEntr[contract]:
                    row.append(str(ContractEntr[contract][mnemonic]))
                else:
                    row.append('0')
            writer.writerow(row)


if __name__ == "__main__":
    makeCsv()
