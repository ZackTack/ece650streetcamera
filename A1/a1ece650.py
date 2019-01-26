# Zhehao Xu, 20762577, z352xu@uwaterloo.ca

import re
import sys


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

    if Point(x1, y1) == Point(x3, y3) and Point(x2, y2) == Point(x4, y4):
        return 1
    elif x1 == x3 == x2 == x4:
        if max(y1,y2) < max(y3,y4) and min(y1,y2) > min(y3,y4):
            return 1  # return Point(x1,y1) Point(x2,y2)
        elif max(y1,y2) > max(y3,y4) and min(y1,y2) < min(y3,y4):
            return 2  # return Point(x3,y3) Point(x4,y4)
    elif y1 == y3 == y2 == y4:
        if max(x1,x2) < max(x3,x4) and min(x1,x2) > min(x3,x4):
            return 1  # return Point(x1,y1) Point(x2,y2)
        elif max(x1,x2) > max(x3,x4) and min(x1,x2) < min(x3,x4):
            return 2  # return Point(x3,y3) Point(x4,y4)

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
    interdic.clear()
    totalpts = set()
    for i in range(0, len(totalline)):
        for j in range(0, len(totalline)):
            if j <= i:
                continue
            else:
                for k in range(0, len(totalline[i])):
                    for h in range(0, len(totalline[j])):
                        if str(intersect(totalline[i][k], totalline[j][h])) == '1':
                            print totalline[i][k]
                            totalpts.add(totalline[i][k].src)
                            totalpts.add(totalline[i][k].dst)
                            totalpts.add(totalline[j][h].src)
                            totalpts.add(totalline[j][h].dst)
                            if not interdic.has_key(totalline[i][k].src):
                                interdic[totalline[i][k].src] = set()
                            interdic[totalline[i][k].src].add(totalline[i][k].dst)
                            interdic[totalline[i][k].src].add(totalline[j][h].src)
                            if not interdic.has_key(totalline[i][k].dst):
                                interdic[totalline[i][k].dst] = set()
                            interdic[totalline[i][k].dst].add(totalline[i][k].src)
                            interdic[totalline[i][k].dst].add(totalline[j][h].dst)
                        elif str(intersect(totalline[i][k], totalline[j][h])) == '2':
                            totalpts.add(totalline[i][k].src)
                            totalpts.add(totalline[i][k].dst)
                            totalpts.add(totalline[j][h].src)
                            totalpts.add(totalline[j][h].dst)
                            if not interdic.has_key(totalline[j][h].src):
                                interdic[totalline[j][h].src] = set()
                            interdic[totalline[j][h].src].add(totalline[j][h].dst)
                            interdic[totalline[j][h].src].add(totalline[i][k].src)
                            if not interdic.has_key(totalline[i][k].dst):
                                interdic[totalline[j][h].dst] = set()
                            interdic[totalline[j][h].dst].add(totalline[j][h].src)
                            interdic[totalline[j][h].dst].add(totalline[i][k].dst)
                        elif intersect(totalline[i][k], totalline[j][h]) != -1:
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
    if vertices.keys():
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
            for x in range(0, len(newitem)):
                vertices[x + 1] = newitem[x]
        else:
            h = 0
            g = 1
            while h < len(newitem):
                if vertices.has_key(g) is False:
                    vertices[g] = newitem[h]
                    h = h + 1
                else:
                    g = g + 1
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
    for i in range(len(intersectpts)):
        ptlist = list(interdic[intersectpts[i]])
        for j in range(len(ptlist)):
            for k in range(len(inputlines)):
                for g in range(len(intersectpts)):
                    if intersectpts[i] in interdic[intersectpts[i]]:
                        interdic[intersectpts[i]].remove(intersectpts[i])
                    if str(intersect(Line(intersectpts[i],ptlist[j]),inputlines[k])) == str(intersectpts[g]) and str(intersect(Line(intersectpts[i],ptlist[j]),inputlines[k])) != str(intersectpts[i]):
                        interdic[intersectpts[i]].add(intersect(Line(intersectpts[i],ptlist[j]),inputlines[k]))
                        if ptlist[j] in interdic[intersectpts[i]]:
                            interdic[intersectpts[i]].remove(ptlist[j])
    edges = []
    element = vertices.keys()
    for i in range(len(intersectpts)):
        realptlist = list(interdic[intersectpts[i]])
        for j in range(len(realptlist)):
            for g in range(len(element)):
                for h in range(len(element)):
                    if vertices[element[g]] == intersectpts[i] and vertices[element[h]] == realptlist[j]:
                        edges.append("<%d,%d>" % (element[g], element[h]))
                    if "<%d,%d>" % (element[h], element[g]) in edges:
                        if "<%d,%d>" % (element[g], element[h]) in edges:
                            edges.remove("<%d,%d>" % (element[g], element[h]))
    edges = set(edges)
    return edges


# Function to print out all vertices
def verticesprint(vertices):
    print "V = { "
    for j in range(len(vertices.keys())):
        value = vertices[vertices.keys()[j]]
        value.x = round(value.x,2)
        value.y = round(value.y,2)
        print " ", vertices.keys()[j], ":  ", value
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
    # Command Instructions
    print "User Manual:"
    print "In order to input correctly, please follow the format : [operation mode \"street name\" coordinates]"
    print "For example: \n a \"Queen Street\" (2,-1) (2,2) (5,5) (5,6) (3,8) \n c \"Queen Street\" (2,1) (2,2) \n r \"Queen Street\" \n g"
    print "Types of operation modes: \n a: add a new street \n c: change the coordinates of an existing street from database \n r: remove an existing street from database \n g: generate the graph from database"
    print "Type \"exit\" to end the program \n"
    database = {}
    coordinates = []
    stname = None
    vertices = {}
    edges = []
    interdic = {}
    while True:
        # Get the input command from the user
        print "Please enter your command: "
        action = sys.stdin.readline()

        # Split the input string into variables
        if action == '':
            print "Program terminated! \n"
            sys.exit(0)
        elif action.strip() == '':
            print "Error: Empty input! \n"
            continue
        elif not action.count('"') and len(action.split()) > 1:
            print "Error: Invalid input format! \n"
            continue
        else:
            commd = re.split(r'"*', action)
            op = commd[0]
            if len(commd) >= 2:
                stname = commd[1].lower()
            if len(commd) >=3:
                coordinates = commd[2]

        # Mode of operations
        if 'g' not in op and 'a' not in op and 'c' not in op and 'r' not in op:
            print "Error: Invalid operation mode! Operation mode does not exist! \n"
        else:
            if 'g' not in op:
                if 'r' not in op:
                    if ' ' not in op:
                        print ("Error: Invalid input! Please have whitespace between operation mode and street name! \n")
                    elif re.search(r'[()]',coordinates) is None:
                        print ("Error: Invalid input! Please enter non-empty and bracketed coordinates! \n")
                    elif coordinates.count('(') != coordinates.count(')'):
                        print ("Error: Invalid input! Please make sure coordinates are bracketed properly! \n")
                    elif coordinates.lstrip() == coordinates:
                        print ("Error: Invalid input! Please have whitespace between street name and coordinates! \n")
                    else:
                        if 'a' in op:
                            if not database.has_key(stname):
                                database[stname] = inputsetgen(coordinates)
                                inputlines = inputlinesgen(database)
                                totalpts, interdic = startcal(database,interdic)
                                newverticeadd(vertices, totalpts)
                                edges = edgesgen(database, vertices, inputlines, interdic)
                                print("Add operation, street has been successfully added! \n")
                            else:
                                print("Error: The street currently exists! \n")
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
