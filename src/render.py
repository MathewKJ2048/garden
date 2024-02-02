from cells import *

render = [None]*m
for i in range(m):
    render[i] = [None]*n

colors = {
    "TEST": (255,255,255),
    "BLANK": (0,0,0),
    "BEDROCK": (100,100,100),
    "SAND": (200,200,0)
}

def get_colors():
    for i in range(m):
        for j in range(n):
            render[i][j] = colors[matrix[i][j]]
