import random
import copy

m = 64 * 2
n = 128 * 2

time = 0

matrix = [None]*m
for i in range(m):
    matrix[i] = [None]*n



def init():
    global m
    global n
    global matrix
    
    
    for i in range(m):
        for j in range(n):
            if i == m-1 or i==0 or j==n-1 or j==0:
                matrix[i][j] = "BEDROCK"
            else:
                matrix[i][j] = "BLANK"

def evolve():
    old_matrix = copy.deepcopy(matrix)
    for i in range(m):
        for j in range(n):
            if old_matrix[i][j] == "SAND":
                matrix[i][j] = "BLANK"
                if i+1 < m:
                    matrix[i+1][j] = "SAND"
    pass
