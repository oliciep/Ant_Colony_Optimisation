import csv
contents = open("Uni50a.dat").read()
n = contents.split()[0]
F = []

def read_distance_matrix(fname):
    D = []
    contents = open("Uni50a.dat").read()
    with open(fname) as contents:
        matrices = contents.readlines()[2:]
        for line in matrices:
            D.append(line.split())
    return D

def read_flow_matrix(fname):
    F = []
    contents = open("Uni50a.dat").read()
    with open(fname) as contents:
        matrices = contents.readlines()[53:]
        for line in matrices:
            F.append(line.split())
    return F
