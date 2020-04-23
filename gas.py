import csv


def gasPerMnemonic():
    GasCost = {}
    NormalOps = {}
    SpecialOps = {}

    with open("opcode-gas-costs.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == 'PUSH*':
                for i in range(1, 33):
                    GasCost[row[1][:-1] + str(i)] = row[2]
            elif row[1] == 'DUP*' or row[1] == 'SWAP*':
                for i in range(1, 17):
                    GasCost[row[1][:-1] + str(i)] = row[2]
            else:
                GasCost[row[1]] = row[2]

    for each in GasCost:
        try:
            NormalOps[each] = int(GasCost[each])
        except:
            SpecialOps[each] = GasCost[each]
    return NormalOps, SpecialOps


if __name__ == "__main__":
    print(gasPerMnemonic())
    print(len(gasPerMnemonic()[0])+len(gasPerMnemonic()[1]))
