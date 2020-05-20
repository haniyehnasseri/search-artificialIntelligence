import numpy as np
import copy
from nodee import Node 
import math
import datetime
file1 = open('test1.txt', 'r')
Lines = file1.readlines() 
table = []

c = 0
for i in range(0,len(Lines) - 1):
	table.append(list(Lines[i]))
	table[i].pop()
	c += 1

table.append(list(Lines[c]))
Table = np.asarray(table)


tableLength = len(table)
tableWidth = len(table[0])

Patients = np.where(Table == 'P')
Patients = np.array(Patients)
Patients = Patients.tolist()

Ambulance = np.where(Table == 'A')
Ambulance = [Ambulance[0][0],Ambulance[1][0]]
hospitals = {}

for i in range(0,len(table)):
	for j in range(0,len(table[0])):
		if((table[i][j] != ' ') and (table[i][j] != '#') and (table[i][j] != 'P') and (table[i][j] != 'A')):
			hospitals[(i,j)] = int(table[i][j])

def findHueristic(row,col,newrow,newcol,_hospitals):
	_min1 = math.inf
	index1 = -1
	_min2 = math.inf
	index2 = -1
	for j in _hospitals:
		if((abs(row - j[0]) + abs(col - j[1]) < _min1)):
			_min1 = abs(row - j[0]) + abs(col - j[1])
			index1 = j
		if((abs(newrow - j[0]) + abs(newcol - j[1]) < _min2)):
			_min2 = abs(newrow - j[0]) + abs(newcol - j[1])
			index2 = j

	if(index1 == index2):
		if(_min2 < _min1):
			return -1
		else:
			return 1
	else:
		return -1





def findPatient(Patients,_hospitals,row,col,newrow,newcol,PatientsSize):
	NeighbourSign = -1
	Location = -1
	for i in range(0,PatientsSize):
		if((Patients[0][i] == newrow) and (Patients[1][i] == newcol)):
			NeighbourSign = i
		if((Patients[0][i] == row) and (Patients[1][i] == col)):
			Location = i

	if(Location == -1):
		return [-1]
	if((newcol < 0) or (newcol > tableWidth - 1)):
		return [-2]
	if((newrow < 0) or (newrow > tableLength - 1)):
		return [-2]
	if((table[newrow][newcol] == '#')):
		return [-2]
	if(NeighbourSign >= 0):
		return [-2]
	newPatients = copy.deepcopy(Patients)
	if (table[newrow][newcol].isnumeric()):
		if(_hospitals[(newrow,newcol)] > 0):
			newHospitals = copy.deepcopy(_hospitals)
			newHospitals[(newrow,newcol)] = _hospitals[(newrow,newcol)] - 1
			newPatients[0].pop(Location)
			newPatients[1].pop(Location)
			return [newPatients,newHospitals,-1]

	newPatients[0][Location] = newrow
	newPatients[1][Location] = newcol
	newHeuristic = findHueristic(row,col,newrow,newcol,_hospitals)
	return [newPatients,_hospitals,newHeuristic]



def doAction(action,curNode,PatientsSize):
	ambulanceLocation_row = curNode.getAmbulance()[0]
	ambulanceLocation_col = curNode.getAmbulance()[1]
	PatientsLocation = curNode.getPatients()
	Hospitals = curNode.getHospitals()
	curNodeHueristic = curNode.getHueristic()

	if(action == 'L'):
		if(ambulanceLocation_col == 0):
			return [-1,-1]
		if(table[ambulanceLocation_row][ambulanceLocation_col - 1] == '#'):
			return [-1,-1]

		newPatientsLocation = findPatient(PatientsLocation,Hospitals,ambulanceLocation_row,ambulanceLocation_col - 1,
			ambulanceLocation_row,ambulanceLocation_col - 2,PatientsSize)
		if(newPatientsLocation == [-1]):
			return [[ambulanceLocation_row,ambulanceLocation_col - 1],PatientsLocation,Hospitals,1,curNodeHueristic]
		if(newPatientsLocation == [-2]):
			return [-2]
		else:
			return [[ambulanceLocation_row,ambulanceLocation_col - 1],newPatientsLocation[0],newPatientsLocation[1],1,
			curNodeHueristic + newPatientsLocation[2]]

	if(action == 'R'):
		if(ambulanceLocation_col == tableWidth - 1):
			return [-1,-1]
		if(Table[ambulanceLocation_row][ambulanceLocation_col + 1] == '#'):
			return [-1,-1]
		newPatientsLocation = findPatient(PatientsLocation,Hospitals,ambulanceLocation_row,ambulanceLocation_col + 1,
			ambulanceLocation_row,ambulanceLocation_col + 2,PatientsSize)
		if(newPatientsLocation == [-1]):
			return [[ambulanceLocation_row,ambulanceLocation_col + 1],PatientsLocation,Hospitals,1,curNodeHueristic]
		if(newPatientsLocation == [-2]):
			return [-2]
		else:
			return [[ambulanceLocation_row,ambulanceLocation_col + 1],newPatientsLocation[0],newPatientsLocation[1],1,
			curNodeHueristic + newPatientsLocation[2]]


	if(action == 'D'):
		if(ambulanceLocation_row == tableLength - 1):
			return [-1,-1]
		if(Table[ambulanceLocation_row + 1][ambulanceLocation_col] == '#'):
			return [-1,-1]
		newPatientsLocation = findPatient(PatientsLocation,Hospitals,ambulanceLocation_row + 1,ambulanceLocation_col,
			ambulanceLocation_row + 2,ambulanceLocation_col,PatientsSize)
		if(newPatientsLocation == [-1]):
			return [[ambulanceLocation_row + 1,ambulanceLocation_col],PatientsLocation,Hospitals,1,curNodeHueristic]
		if(newPatientsLocation == [-2]):
			return [-2]
		else:
			return [[ambulanceLocation_row + 1,ambulanceLocation_col],newPatientsLocation[0],newPatientsLocation[1],1,
			curNodeHueristic + newPatientsLocation[2]]



	if(action == 'U'):

		if(ambulanceLocation_row == 0):
			return [-1,-1]
		if(Table[ambulanceLocation_row - 1][ambulanceLocation_col] == '#'):
			return [-1,-1]
		newPatientsLocation = findPatient(PatientsLocation,Hospitals,ambulanceLocation_row - 1,ambulanceLocation_col,
			ambulanceLocation_row - 2,ambulanceLocation_col,PatientsSize)
		if(newPatientsLocation == [-1]):
			return [[ambulanceLocation_row - 1,ambulanceLocation_col],PatientsLocation,Hospitals,1,curNodeHueristic]
		if(newPatientsLocation == [-2]):
			return [-2]
		else:
			return [[ambulanceLocation_row - 1,ambulanceLocation_col],newPatientsLocation[0],newPatientsLocation[1],1,
			curNodeHueristic + newPatientsLocation[2]]


def getBestNode(Fifo):
	_min = math.inf
	for i in range(0,len(Fifo)):
		if(Fifo[i].getF() < _min):
			_min = Fifo[i].getF()
			index = i
	return index

def makeFrontier(table):
	Frontier = {}
	Explored = {}
	for i in range(0,len(table)):
		for j in range(0,len(table[0])):
			if(table[i][j] != '#'):
				Frontier[(i,j)] = []
				Explored[(i,j)] = []
	return[Frontier,Explored]


def GoalAchieved(f):
	return f[0] == []

def getInitialHueristic(hospitals):
	bestSum = 0
	hospitalsCopy = copy.deepcopy(hospitals)
	for i in range(0,len(Patients[0])):
		_min = math.inf
		for j in hospitalsCopy:
			if((abs(Patients[0][i] - j[0]) + abs(Patients[1][i] - j[1]) < _min)):
				_min = abs(Patients[0][i] - j[0]) + abs(Patients[1][i] - j[1])
		bestSum += _min
	return bestSum


def aStarSearch():
	#Repetitive = 1
	#nonRepetitive = 1
	Fifo = []
	Frontier,Explored = makeFrontier(table)
	actions = ['D','L','U','R']
	if(GoalAchieved(Patients)):
		return 1
	initialHueristic = getInitialHueristic(hospitals)
	firstNode = Node(Ambulance,Patients,hospitals)
	firstNode.setCost(0)
	firstNode.setHueristic(initialHueristic)
	firstNode.setF(initialHueristic)
	firstNode.setLevel(0)
	Fifo = [firstNode]
	Frontier[(Ambulance[0],Ambulance[1])].append([Ambulance,Patients,hospitals])
	while(True):
		if(Fifo == []):
			return 0
		bestNodeIndex = getBestNode(Fifo)
		curNode = Fifo.pop(bestNodeIndex)
		if(GoalAchieved(curNode.getPatients())):
			#print(nonRepetitive)
			#print(curNode.getLevel())
			return 1
		Explored[(curNode.getAmbulance()[0],curNode.getAmbulance()[1])].append(
			[curNode.getAmbulance(),curNode.getPatients(),curNode.getHospitals()])
		PatientsSize = len(curNode.getPatients()[0])
		for action in actions:
			decidedNodeList = doAction(action,curNode,PatientsSize)
			if(decidedNodeList == [-1,-1]):
				continue
			if(decidedNodeList == [-2]):
				continue
			if((decidedNodeList[0:3] in Explored[(decidedNodeList[0][0],decidedNodeList[0][1])])):
				#Repetitive += 1
				continue
			g =  curNode.getCost() + decidedNodeList[3]
			h = decidedNodeList[4]
			f = g + h
			if (decidedNodeList[0:3] not in Frontier[(decidedNodeList[0][0],decidedNodeList[0][1])]):
				#nonRepetitive += 1
				decidedNode = Node(decidedNodeList[0],decidedNodeList[1],decidedNodeList[2])
				decidedNode.setCost(g)
				decidedNode.setHueristic(h)
				decidedNode.setF(f)
				decidedNode.setLevel(curNode.getLevel() + 1)
				Frontier[(decidedNodeList[0][0],decidedNodeList[0][1])].append(decidedNodeList[0:3])
				Fifo.append(decidedNode)
			#Repetitive += 1

	return 0

###Astar Hueristic###
start = datetime.datetime.now()
Astar1Solution = aStarSearch()
#print(Astar1Solution)
finish = datetime.datetime.now()
print(finish - start)