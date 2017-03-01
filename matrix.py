#!/usr/bin/env python3

import line

width = 500
height = 500
#width = int(input("width of image: "))
#height = int(input("height of image: "))
colorDepth = 255
matrix = []
color = [0, 255, 0]

for i in range(width):
    matrix.append([])
    for j in range(height):
        matrix[i].append([0, 0, 0])

def printMatrix(matrix):
    printString = ''
    rows = len(matrix)
    columns = len(matrix[0])
    for row in range (0, rows):
        for column in range (0, columns):
            printString = printString + str(matrix[row][column]) + ' '
        printString = printString + '\n'
    print(printString)

def writePpmFile(matrix):
    file = open("edgeTest.ppm", "w")
    file.write("P3\n")
    file.write("{} {} {}\n".format(width, height, colorDepth))
    for i in range(height):
        for j in range(width):
            file.write("{} {} {}\n".format(matrix[j][i][0], matrix[j][i][1], matrix[j][i][2]))

def plot(matrix, x, y, color):
    matrix[x][y][0] = color[0]
    matrix[x][y][2] = color[2]
    matrix[x][y][1] = color[1]

def drawLine(matrix, a, b, color):
    #Swap points a and b if a is to the right of b.
    if(b[0] < a[0]):
        b[0] = b[0] + a[0]
        b[1] = b[1] + a[1]
        a[0] = b[0] - a[0]
        a[1] = b[1] - a[1]
        b[0] = b[0] - a[0]
        b[1] = b[1] - a[1]
        
    #Plot point b
    plot(matrix, b[0], b[1], color)

    x = a[0]
    y = a[1]
            
    B = -1 * (b[0] - a[0])
    
    if a[1] >= b[1]:
        #Octant I, II
        A = a[1] - b[1]
        if A >= (-1 * B):
            #Octant II
            d = A + (2 * B)
            while(y > b[1]):
                plot(matrix, x, y, color)
                if(d < 0):
                    x = x + 1
                    d = d + A
                y = y - 1
                d = d + B
        else:
            #Octant I
            d = (2 * A) + B
            while(x < b[0]):
                plot(matrix, x, y, color)
                if(d > 0):
                    y = y - 1
                    d = d + B
                x = x + 1
                d = d + A
    else:
        #Octant VII, VIII
        A = a[1] - b[1]
        if A >= B:
            #Octant VIII
            d = (2 * A) - B
            while(x < b[0]):
                plot(matrix, x, y, color)
                if(d < 0):
                    y = y + 1
                    d = d - B
                x = x + 1
                d = d + A
        else:
            #Octant VII
            d = A - (2 * B)
            while(y < b[1]):
                plot(matrix, x, y, color)
                if(d > 0):
                    x = x + 1
                    d = d + A
                y = y + 1
                d = d - B
    plot(matrix, b[0], b[1], color)

def randColor():
    randColor = [random.randrange(0,256), random.randrange(0,256), random.randrange(0,256)]
    return randColor
def drawRandLine():
    randColor = [random.randrange(0,256), random.randrange(0,256), random.randrange(0,256)]
    x = [random.randrange(0, len(matrix)), random.randrange(0, len(matrix[0]))]
    y = [random.randrange(0, len(matrix)), random.randrange(0, len(matrix[0]))]
    drawLine(matrix, x, y, randColor)
    
def scalarMultiplication(scalar, matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    for row in range(0, rows):
        for column in range(0, columns):
            matrix[row][column] = matrix[row][column] * scalar

# This function is specific to 4xN edge matrix multiplied BY a 4x4 matrix
def matrixMultiplication(matrix, edgeMatrix):
    if len(matrix[0]) != len(edgeMatrix):
        print('matrices cannot be multiplied.')
        return false
    retMatrix = []
    tempList = []
    for row in range( len(matrix) ):
        retMatrix.append([])
        for column in range( len(edgeMatrix[row]) ):
            for i in range( len(edgeMatrix) ):
                tempList.append(edgeMatrix[column][i])
            retMatrix[row].append(dotProduct(matrix[row], tempList))
            tempList = []
    for row in range( len(retMatrix) ):
        if( row >= len(edgeMatrix) ):
            edgeMatrix.append([])
        for column in range( len(retMatrix[row]) ):
            edgeMatrix[row][column] = retMatrix[row][column]
    return edgeMatrix
            
                                  
def dotProduct(list1, list2):
    dotProduct = 0
    if len(list1) != len(list2):
        print('lists of unequal lengths')
        return false
    for i in range(0, len(list1)):
        dotProduct = dotProduct + (list1[i] * list2[i])
    return dotProduct

def getIdentityMatrix(matrix):
    length = max(len(matrix), len(matrix[0]))
    retMatrix = []
    for r in range(0, length):
        retMatrix.append([])
        for c in range(0, length):
            if(r == c):
                retMatrix[r].append(1)
            else:
                retMatrix[r].append(0)
    return retMatrix

def addPoint(matrix, a):
    matrix[0].append(a[0])
    matrix[1].append(a[1])
    matrix[2].append(a[2])
    matrix[3].append(1)

def addEdge(matrix, a, b):
    addPoint(matrix, a)
    addPoint(matrix, b)

def drawEdges(edgeMatrix):
    for i in range(0, len(edgeMatrix[0]) - 1, 2):
        drawLine(matrix, [edgeMatrix[0][i], edgeMatrix[1][i]], [edgeMatrix[0][i+1], edgeMatrix[1][i+1]], [255, 0, 255])
    writePpmFile(matrix)

#Test Cases
edgeMatrix = []
for row in range(0,4):
    edgeMatrix.append([])
    for column in range(0,4):
        if(column == 4):
            edgeMatrix[row].append(1)
        else:
            edgeMatrix[row].append(row + column)

printMatrix(edgeMatrix)
print('multiplying previous matrix with scalar value \'3\'.')
scalarMultiplication(3, edgeMatrix)
printMatrix(edgeMatrix)
print('multiplying previous matrix with itself.')
matrixMultiplication(edgeMatrix, edgeMatrix)
printMatrix(edgeMatrix)
print('testing identity matrix of previous matrix.')
printMatrix(getIdentityMatrix(edgeMatrix))
print('testing addEdge function.')
a = [10, 20, 0]
b = [0, 599, 0]
addEdge(edgeMatrix, a, b)
printMatrix(edgeMatrix)
print('drawing the following matrix.')
edgeMatrix = []
for i in range(0, 4):
    edgeMatrix.append([])
addEdge(edgeMatrix, [40, 100, 0], [80, 100, 0])
addEdge(edgeMatrix, [80, 100, 0], [50, 200, 0])
addEdge(edgeMatrix, [50, 200, 0], [60, 0, 0])
addEdge(edgeMatrix, [60, 0, 0], [70, 200, 0])
addEdge(edgeMatrix, [70, 200, 0], [40, 100, 0])
addEdge(edgeMatrix, [0, 0, 0], [200, 200, 0])
printMatrix(edgeMatrix)
drawEdges(edgeMatrix)
scalarMultiplication(2, edgeMatrix)
drawEdges(edgeMatrix)

print('filename is edgeTest.ppm')
