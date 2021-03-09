#klasa odpowiedzialna za dane
class Global_Data():	
	
	def __init__(self, W,H,HA,WA,rho,c,t0,alfa,t_surroundings,tau,simulation_time):		
		self.width = W
		self.height = H
		self.height_amount =HA
		self.width_amount=WA
		self.elements_amount=(HA-1)*(WA-1)
		self.nodes_amount=WA*HA
		self.rho=rho
		self.c=c
		self.t0=t0
		self.alfa=alfa
		self.t_surroundings=t_surroundings
		self.tau=tau #krok czasowy
		self.simulation_time=simulation_time
#klasa odpowiedzialna za węzły
class Node():
	def __init__(self, X,Y,ID,t0):
		self.x=X
		self.y=Y
		self.id=ID
		self.t0=t0
		self.bc=0 #Boundary_Condition, czy wezel znajduje sie po zewnetrznej stronie siatki		
	def getX():
		return self.x
	def getY():
		return self.y
	def getID():
		return self.id		
#klasa odpowiedzialna za elementy
class Element():	
	def __init__(self, A,B,C,D,element_id): #A,B,C,D powinny być NODE'ami
		self.id_1=A
		self.id_2=B
		self.id_3=C
		self.id_4=D
		self.element_id=element_id
		self.id_list=[A.id,B.id,C.id,D.id]		
		self.H=[]
		self.C=[]
		self.P=[]
	def give_points(self):
		tab=[[self.id_1.x,self.id_2.x,self.id_3.x,self.id_4.x],[self.id_1.y,self.id_2.y,self.id_3.y,self.id_4.y]]
		#print("x:",tab[0])
		#print("y:",tab[1],"\n")
		return tab



	
#klasa odpowiedzialna za siatkę
class FEM_Grid():
	nodes=[] #węzły
	elements=[] #elementy