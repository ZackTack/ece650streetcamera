# Zhehao Xu, 20762577, z352xu@uwaterloo.ca

import re


# Class of Point and Line objects
class Point(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


class Line(object):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __str__(self):
        return str(self.src) + '-->' + str(self.dst)

    def __repr__(self):
        return str(self.src) + '-->' + str(self.dst)

    def __hash__(self):
        return hash((self.src, self.dst))

    def __eq__(self, other):
        return (self.src, self.dst) == (other.src, other.dst)


# Function to find intersection
def intersect(l1, l2):
    x1, y1 = l1.src.x, l1.src.y
    x2, y2 = l1.dst.x, l1.dst.y
    x3, y3 = l2.src.x, l2.src.y
    x4, y4 = l2.dst.x, l2.dst.y

    xnum = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    xden = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if xden == 0:
        return -1
    xcoor = xnum / xden

    ynum = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    yden = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if yden == 0:
        return -1
    ycoor = ynum / yden

    if xcoor < max(min(x1,x2),min(x3,x4)):
        return -1
    elif xcoor > min(max(x1,x2),max(x3,x4)):
        return -1

    if ycoor < max(min(y1,y2),min(y3,y4)):
        return -1
    elif ycoor > min(max(y1,y2),max(y3,y4)):
        return -1

    return Point(xcoor, ycoor)


# Function to find x,y coordinates
def coordfind(input):
    coordinate = re.findall(r'[-]?\d+', input)
    xcoord = []
    ycoord = []
    for i in range(0, len(coordinate), 2):
        xcoord.append(int(coordinate[i]))
        ycoord.append(int(coordinate[i + 1]))
    return xcoord,ycoord


# Function to find points
def ptfind(xcoord, ycoord):
    pt = []
    if len(xcoord) == len(ycoord):
        for j in range(0, len(xcoord)):
            pt.append(Point(xcoord[j], ycoord[j]))
    else:
        print("Input coordinates do not match, Please check the input correctness! \n")
    return pt


# Function to find lines
def linefind(pt):
    line = []
    for k in range(0,len(pt)-1):
        line.append(Line(pt[k],pt[k+1]))
    return line


# Function to find vertices
def verticefind(totalline, interdic):
    totalpts = set()
    for i in range(0, len(totalline)):
        for j in range(0, len(totalline)):
            if j == i:
                continue
            else:
                for k in range(0, len(totalline[i])):
                    for h in range(0, len(totalline[j])):
                        if intersect(totalline[i][k], totalline[j][h]) != -1:
                            totalpts.add(totalline[i][k].src)
                            totalpts.add(totalline[i][k].dst)
                            totalpts.add(totalline[j][h].src)
                            totalpts.add(totalline[j][h].dst)
                            totalpts.add(intersect(totalline[i][k], totalline[j][h]))
                            if not interdic.has_key(intersect(totalline[i][k], totalline[j][h])):
                                interdic[intersect(totalline[i][k], totalline[j][h])] = set()
                            interdic[intersect(totalline[i][k], totalline[j][h])].add(totalline[i][k].src)
                            interdic[intersect(totalline[i][k], totalline[j][h])].add(totalline[i][k].dst)
                            interdic[intersect(totalline[i][k], totalline[j][h])].add(totalline[j][h].src)
                            interdic[intersect(totalline[i][k], totalline[j][h])].add(totalline[j][h].dst)
    return totalpts,interdic


# Function to generate the points from input command
def inputsetgen(coordinates):
    xcoord, ycoord = coordfind(coordinates)
    pt = ptfind(xcoord, ycoord)
    return pt


def inputlinesgen(database):
    inputlines = []
    element = database.keys()
    for i in range(0, len(element)):
        inputlines.extend(linefind(database[element[i]]))
    return inputlines


# Function to generate the new vertices from change or remove operation
def newverticesgen(vertices, totalpts):
    if len(vertices.values()) >= 1:
        removekeys = []
        removeitem = list(set(vertices.values()) - totalpts)
        newitem = list(totalpts - set(vertices.values()))
        currentkey = vertices.keys()
        for i in range(0, len(currentkey)):
            for j in range(0, len(removeitem)):
                if vertices[currentkey[i]] == removeitem[j]:
                    removekeys.append(currentkey[i])
        for k in range(0, len(removekeys)):
            vertices.pop(removekeys[k])
        if not vertices.keys():
            for x in range(0,len(newitem)):
                vertices[x+1] = newitem[x]
        else:
            for h in range(max(vertices.keys()), max(vertices.keys()) + len(newitem)):
                for g in range(0, len(newitem)):
                    vertices[h + 1] = newitem[g]
    return None


# Function to generate new vertices from add operation
def newverticeadd(vertices, totalpts):
    additem = list(totalpts - set(vertices.values()))
    if not vertices.keys():
        for x in range(0, len(additem)):
            vertices[x + 1] = additem[x]
    else:
        h = 0
        g = 1
        while h < len(additem):
            if vertices.has_key(g) is False:
                vertices[g] = additem[h]
                h = h + 1
            else:
                g = g + 1
    return None


def edgesgen(database,vertices, inputlines, interdic):
    inputpts = []
    for i in range(0,len(database.values())):
        for j in range(0,len(database.values()[i])):
            inputpts.append(database.values()[i][j])
    intersectpts = interdic.keys()
    if not vertices.keys():
        return None
    else:
        element = vertices.keys()
        edges = []
        for i in range(0,len(element)):
            for j in range(0,len(element)):
                if j == i:
                    continue
                else:
                    currentcheck = Line(vertices[element[i]],vertices[element[j]])
                    if currentcheck.dst in intersectpts and currentcheck.src in intersectpts:
                        edges.append("<%d,%d>" % (element[i], element[j]))
                    elif currentcheck.dst in intersectpts or currentcheck.src in intersectpts:
                        if currentcheck.dst in intersectpts:
                            if currentcheck.src in interdic[currentcheck.dst]:
                                edges.append("<%d,%d>" % (element[i],element[j]))
                        elif currentcheck.src in intersectpts:
                            if currentcheck.dst in interdic[currentcheck.src]:
                                edges.append("<%d,%d>" % (element[i], element[j]))
                checkpt = []
                for k in range(len(inputlines)):
                    checkpt.append(intersect(currentcheck,inputlines[k]))
                for g in range(len(checkpt)):
                    if checkpt[g] != -1:
                        if str(checkpt[g]) == str(currentcheck.src) or str(checkpt[g]) == str(currentcheck.dst):
                            continue
                        else:
                            if "<%d,%d>" % (element[i], element[j]) in edges:
                                edges.remove("<%d,%d>" % (element[i], element[j]))
                if "<%d,%d>" % (element[j], element[i]) in edges:
                    if "<%d,%d>" % (element[i], element[j]) in edges:
                        edges.remove("<%d,%d>" % (element[i], element[j]))
    edges = set(edges)
    return edges


# Function to print out all vertices
def verticesprint(vertices):
    print "V = { "
    for j in range(0, len(vertices.keys())):
        print " ", vertices.keys()[j], ":  ", vertices[vertices.keys()[j]]
    print "} "
    return None


# Function to print out all edges
def edgeprint(edges):
    if not edges:
        print "E = { "
    else:
        edges = list(edges)
        print "E = { "
        for i in range(0,len(edges)):
            if i == len(edges):
                print " %s" % edges[i]
            else:
                print " %s," % edges[i]
    print "} \n"
    return None


# Main function to calculate vertices and edges
def startcal(database, interdic):
    pt = []
    totalline = []
    for i in range(0,len(database.values())):
        pt.append(database.values()[i])
    for j in range(0,len(pt)):
        totalline.append(linefind(pt[j]))
    totalpts, interdic = verticefind(totalline,interdic)
    return totalpts,interdic


def main():
    database = {}
    coordinates = []
    stname = None
    vertices = {}
    edges = []
    interdic = {}
    while True:
        # Get the input command from the user
        action = raw_input("Please enter your command: \n")

        # Split the input string into variables
        commd = re.split(r'"*', action)
        op = commd[0]
        if len(commd) >= 2:
            stname = commd[1].strip()
        if len(commd) >=3:
            coordinates = commd[2]

        # Mode of operations
        if 'g' not in op:
            if 'r' not in op:
                if ' ' not in op:
                    print ("Error: Invalid input! Please have whitespace between operation command and street name! \n")
                elif re.search(r'[()]',coordinates) is None:
                    print ("Error: Invalid input! Please bracket coordinates! \n")
                elif coordinates.count('(') % coordinates.count(')') != 0:
                    print ("Error: Invalid input! Please make sure coordinates are bracketed properly! \n")
                elif coordinates.lstrip() == coordinates:
                    print ("Error: Invalid input! Please have whitespace between street name and coordinates! \n")
                else:
                    if 'a' in op:
                        database[stname] = inputsetgen(coordinates)
                        inputlines = inputlinesgen(database)
                        totalpts, interdic = startcal(database,interdic)
                        newverticeadd(vertices, totalpts)
                        edges = edgesgen(database, vertices, inputlines, interdic)
                        print("Add operation, street has been successfully added! \n")
                    elif 'c' in op:
                        if database.has_key(stname) is True:
                            database[stname] = inputsetgen(coordinates)
                            inputlines = inputlinesgen(database)
                            totalpts, interdic = startcal(database,interdic)
                            newverticesgen(vertices,totalpts)
                            edges = edgesgen(database,vertices,inputlines,interdic)
                            print("Change operation, street has been successfully updated! \n")
                        else:
                            print("Error: The input street to change does not exist, change denied! \n")
                    else:
                        print("Error: The input argument is not valid, Please enter the correct argument! \n")
            else:
                if database.has_key(stname) is True:
                    del database[stname]
                    inputlines = inputlinesgen(database)
                    totalpts, interdic = startcal(database,interdic)
                    newverticesgen(vertices, totalpts)
                    edges = edgesgen(database,vertices,inputlines, interdic)
                    print("Remove operation, street has been successfully removed! \n")
                else:
                    print("Error: The input street to remove does not exist, remove denied! \n")
        else:
            verticesprint(vertices)
            edgeprint(edges)


if __name__ == '__main__':
    main()
