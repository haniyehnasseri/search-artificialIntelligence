import numpy as np
import copy
from nodee import Node 
import datetime
file1 = open('test3.txt', 'r')
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
			return [newPatients,newHospitals]
	
	newPatients[0][Location] = newrow
	newPatients[1][Location] = newcol
	return [newPatients,_hospitals]



def doAction(action,curNode,PatientsSize):
	ambulanceLocation_row = curNode.getAmbulance()[0]
	ambulanceLocation_col = curNode.getAmbulance()[1]
	PatientsLocation = curNode.getPatients()
	Hospitals = curNode.getHospitals()
	
	if(action == 'L'):
		if(ambulanceLocation_col == 0):
			return [-1,-1]
		if(table[ambulanceLocation_row][ambulanceLocation_col - 1] == '#'):
			return [-1,-1]

		newPatientsLocation = findPatient(PatientsLocation,Hospitals,ambulanceLocation_row,ambulanceLocation_col - 1,
			ambulanceLocation_row,ambulanceLocation_col - 2,PatientsSize)
		if(newPatientsLocation == [-1]):
			return [[ambulanceLocation_row,ambulanceLocation_col - 1],PatientsLocation,Hospitals]
		if(newPatientsLocation == [-2]):
			return [-2]
		else:
			return [[ambulanceLocation_row,ambulanceLocation_col - 1],newPatientsLocation[0],newPatientsLocation[1]]

	if(action == 'R'):
		if(ambulanceLocation_col == tableWidth - 1):
			return [-1,-1]
		if(Table[ambulanceLocation_row][ambulanceLocation_col + 1] == '#'):
			return [-1,-1]
		newPatientsLocation = findPatient(PatientsLocation,Hospitals,ambulanceLocation_row,ambulanceLocation_col + 1,
			ambulanceLocation_row,ambulanceLocation_col + 2,PatientsSize)
		if(newPatientsLocation == [-1]):
			return [[ambulanceLocation_row,ambulanceLocation_col + 1],PatientsLocation,Hospitals]
		if(newPatientsLocation == [-2]):
			return [-2]
		else:
			return [[ambulanceLocation_row,ambulanceLocation_col + 1],newPatientsLocation[0],newPatientsLocation[1]]


	if(action == 'D'):
		if(ambulanceLocation_row == tableLength - 1):
			return [-1,-1]
		if(Table[ambulanceLocation_row + 1][ambulanceLocation_col] == '#'):
			return [-1,-1]
		newPatientsLocation = findPatient(PatientsLocation,Hospitals,ambulanceLocation_row + 1,ambulanceLocation_col,
			ambulanceLocation_row + 2,ambulanceLocation_col,PatientsSize)
		if(newPatientsLocation == [-1]):
			return [[ambulanceLocation_row + 1,ambulanceLocation_col],PatientsLocation,Hospitals]
		if(newPatientsLocation == [-2]):
			return [-2]
		else:
			return [[ambulanceLocation_row + 1,ambulanceLocation_col],newPatientsLocation[0],newPatientsLocation[1]]



	if(action == 'U'):

		if(ambulanceLocation_row == 0):
			return [-1,-1]
		if(Table[ambulanceLocation_row - 1][ambulanceLocation_col] == '#'):
			return [-1,-1]
		newPatientsLocation = findPatient(PatientsLocation,Hospitals,ambulanceLocation_row - 1,ambulanceLocation_col,
			ambulanceLocation_row - 2,ambulanceLocation_col,PatientsSize)
		if(newPatientsLocation == [-1]):
			return [[ambulanceLocation_row - 1,ambulanceLocation_col],PatientsLocation,Hospitals]
		if(newPatientsLocation == [-2]):
			return [-2]
		else:
			return [[ambulanceLocation_row - 1,ambulanceLocation_col],newPatientsLocation[0],newPatientsLocation[1]]



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

def bfsSearch():
	#Repetitive = 1
	#nonRepetitive = 1
	Fifo = []
	Frontier,Explored = makeFrontier(table)
	actions = ['L','R','D','U']
	startNode = Node(Ambulance,Patients,hospitals)
	startNode.setLevel(0)
	Fifo = [startNode]
	if(GoalAchieved(Patients)):
		return 1
	Frontier[(Ambulance[0],Ambulance[1])].append([Ambulance,Patients,hospitals])
	while(True):
		if(Frontier == []):
			return 0
		curNode = Fifo.pop(0)
		Explored[(curNode.getAmbulance()[0],curNode.getAmbulance()[1])].append(
			[curNode.getAmbulance(),curNode.getPatients(),curNode.getHospitals()])
		PatientsSize = len(curNode.getPatients()[0])
		for action in actions:
			decidedNodeList = doAction(action,curNode,PatientsSize)
			if(decidedNodeList == [-1,-1]):
				continue
			if(decidedNodeList == [-2]):
				continue
			if(GoalAchieved(decidedNodeList[1])):
				#print(curNode.getLevel() + 1)
				#print(nonRepetitive + 1)
				#print(Repetitive + 1)
				return 1
			if((decidedNodeList not in Frontier[(decidedNodeList[0][0],decidedNodeList[0][1])])
			 and (decidedNodeList not in Explored[(decidedNodeList[0][0],decidedNodeList[0][1])])):
				#nonRepetitive += 1
				decidedNode = Node(decidedNodeList[0],decidedNodeList[1],decidedNodeList[2])
				decidedNode.setLevel(curNode.getLevel() + 1)
				Fifo.append(decidedNode)
				Frontier[(decidedNodeList[0][0],decidedNodeList[0][1])].append(decidedNodeList)
			#Repetitive += 1
	return 0



###BFS SEARCH###
for i in range(0,len(table)):
	for j in range(0,len(table[0])):
		if((table[i][j] != ' ') and (table[i][j] != '#') and (table[i][j] != 'P') and (table[i][j] != 'A')):
			hospitals[(i,j)] = int(table[i][j])


start = datetime.datetime.now()
bfsSolution = bfsSearch()#
finish = datetime.datetime.now()
print(finish - start)
#print(bfsSolution)






###IDS###
Views = makeFrontier(table)[0]
Depth = 0
actions = ['L','R','D','U']
def DLS(src,maxDepth,Views):
	if([src.getAmbulance(),src.getPatients(),src.getHospitals()] not in Views[(src.getAmbulance()[0],src.getAmbulance()[1])]):
		Views[(src.getAmbulance()[0],src.getAmbulance()[1])].append([src.getAmbulance(),src.getPatients(),src.getHospitals()])
	if(maxDepth > 1):
		srcChildren = src.getChildren()
		for child in srcChildren:
			if(DLS(child,maxDepth-1,Views)):
				return True
		return False

	if(maxDepth == 1):
  		srcPatients = src.getPatients()
  		PatientsSize = len(srcPatients[0])
  		for action in actions:
  			decidedNode = doAction(action,src,PatientsSize)
  			if(decidedNode == [-1,-1]):
  				continue
  			if(decidedNode == [-2]):
  				continue
  			if(decidedNode not in Views[(decidedNode[0][0],decidedNode[0][1])]):
  				newChild = Node(decidedNode[0],decidedNode[1],decidedNode[2])
  				src.addChild(newChild)
  				if(DLS(newChild,maxDepth - 1,Views)):
  					return True

  		return False
	if(maxDepth == 0):
  		if(GoalAchieved(src.getPatients())):
  			return True
  		return False
	return False
   
   
def IDDFS(Depth,Views):
	SrcNode = Node(Ambulance,Patients,hospitals)
	while(True):
		if(DLS(SrcNode,Depth,Views)):
			#print(Depth)
			return 1
		Depth += 1
	return 0

#start = datetime.datetime.now()
#IDSSolution = IDDFS(Depth,Views)
#finish = datetime.datetime.now()
#print(finish - start)
#print(IDSSolution)


