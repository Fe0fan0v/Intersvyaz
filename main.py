import csv
import sys
from time import time
import threading
from socket import gethostbyname

good = bad = unknown = 0
result = [['good knots', good], ['bad knots', bad], ['unknown knot', unknown]]


class IdThread(threading.Thread):
    def __init__(self, flow, file):
        super().__init__()
        self.flow = flow
        self.file = file

    def run(self):
        global result
        for knot in parse(self.file)[self.flow: self.flow + 1]:
            try:
                if gethostbyname(knot):
                    result[0][1] += 1
            except IOError:
                result[1][1] += 1
            except:
                result[2][1] += 1
        return result


def parse(filename):
    f = open(filename, 'r')
    knots = []
    for line in f:
        for knot in line.split():
            knots.append(knot)
    f.close()
    return knots


def main(inputfile, *args):
    global result
    lst = parse(inputfile)
    start = time()
    for wave in range(len(lst)):
        thread = IdThread(wave, inputfile)
        thread.start()
    if args:
        outfile = args[0]
        with open(outfile, "w") as file:
            writer = csv.writer(file)
            writer.writerows(result)
    else:
        pass
    finish = time()
    print(f'Time succeed: {finish - start}')


main('file.txt', 'file.csv')
# main(sys.argv[1], sys.argv[2])
