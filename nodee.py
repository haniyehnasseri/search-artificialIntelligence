class Node :
    Ambulance = []
    Patients = []
    Hospitals = {}

    def __init__ (self ,Ambulance,Patients,Hospitals):
        #self.nodeList = listt
        self.Ambulance = Ambulance
        self.Patients = Patients 
        self.Hospitals = Hospitals
        self.Children = []
        self.Cost = 0
        self.Hueristic = 0
        self.F = 0
        self.Level = 0

    def setLevel (self,Level):
        self.Level = Level
            
    def getLevel (self):
        return self.Level

    def setAmbulance (self,Ambulance):
        self.Ambulance = Ambulance
            
    def getAmbulance (self):
        return self.Ambulance 

    def setCost (self,Cost):
        self.Cost = Cost
            
    def getCost (self):
        return self.Cost

    def setHueristic (self,Hueristic):
        self.Hueristic = Hueristic
            
    def getHueristic (self):
        return self.Hueristic

    def setF (self,F):
        self.F = F
            
    def getF (self):
        return self.F

    def setPatients (self,Patients):
        self.Patients = Patients
            
    def getPatients (self):
        return self.Patients

    def setHospitals (self,Hospitals):
        self.Hospitals = Hospitals
            
    def getHospitals (self):
        return self.Hospitals  

    def addChild (self,Child):
        self.Children.append(Child) 


    def getChildren (self):
        return self.Children






    