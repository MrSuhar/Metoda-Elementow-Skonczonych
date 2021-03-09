import numpy as np 
from Net import *
from Jakobian import *
from elem4 import *
from tworz_h import *
from tworz_C import *
from tworz_HBC_i_P import *	

#MAIN() 

#Czytanie z pliku "dane.txt")
	#pomocnicze zmienne
width=0
height=0
height_nodes=0
width_nodes=0
k=0
ile_pc=0
t_sur=0
tau=0
simulation_time=0

#Czytanie z pliku
f=open("dane.txt","r")
f1=f.readlines()
y=0
for x in f1:
	if(y==1):
		width=float(x)
	if(y==3):
		height=float(x)
	if(y==5):
		height_nodes=int(x)
	if(y==7):
		width_nodes=int(x)
	if(y==9):
		k=float(x)
	if(y==11):
		ile_pc=int(x)
	if(y==13):
		rho=int(x)
	if(y==15):
		c=int(x)
	if(y==17):
		t0=float(x)		
	if(y==19):
		alfa=float(x)		
	#print(x)
	if(y==21):
		t_sur=float(x)
	if(y==23):
		tau=int(x)
	if(y==25):
	    simulation_time=int(x)		
	y+=1
f.close()

Data_1=Global_Data(width,height,height_nodes,width_nodes,rho,c,t0,alfa,t_sur,tau,simulation_time)
Net_1=FEM_Grid()

#TWORZENIE WEZLOW
	#zmienne pomocnicze 
x=0

y=0

for i in range(1,Data_1.nodes_amount+1):	
	
	if i%(Data_1.height_amount)!=0:		
		Net_1.nodes.append(Node(x,y,i,t0))
		y+=(Data_1.height/(Data_1.height_amount-1))
		
		#debug- wypisywanie wezlow elementu
		#print("id" ,Net_1.nodes[i-1].id)
		#print("x:",Net_1.nodes[i-1].x)		
		#print("y:",Net_1.nodes[i-1].y)				
	else:		
		Net_1.nodes.append(Node(x,y,i,t0))
		x+=(Data_1.width/(Data_1.width_amount-1))
		y=0
		
		#debug- wypisywanie wezlow elementu
		#print("id" ,Net_1.nodes[i-1].id)
		#print("x:",Net_1.nodes[i-1].x)		
		#print("y:",Net_1.nodes[i-1].y)

#Okreslenie czy wezel znajduje sie na zewnetrznej krawedzi siatki
for i in range(Data_1.nodes_amount):
	if Net_1.nodes[i].x==0 or Net_1.nodes[i].x==Data_1.width or Net_1.nodes[i].y==0 or Net_1.nodes[i].y==Data_1.height:
		Net_1.nodes[i].bc=1
	#print("Wezel nr: ",Net_1.nodes[i].id," bc: ",Net_1.nodes[i].bc)
		
#TWORZENIE ELEMENTÓW
	#zmienne pomocnicze
x=0

#print("Ilosc elementow",Data_1.elements_amount)

for i in range(1,Data_1.elements_amount+1):
#for i in range(Data_1.elements_amount+1):	
		#dodawanie wezlow do elementów
	#Net_1.elements.append(Element(Net_1.nodes[i-1+x],Net_1.nodes[i+4+x],Net_1.nodes[i+5+x],Net_1.nodes[i+x],i))
	#Net_1.elements.append(Element(Net_1.nodes[i-1+x],Net_1.nodes[i+3+x],Net_1.nodes[i+4+x],Net_1.nodes[i+x],i)) #zamaist 3 Data_1.height_nodes-1 , zamiast 4 Data_1.height_nodes
	Net_1.elements.append(Element(Net_1.nodes[i-1+x],Net_1.nodes[i+(Data_1.height_amount-1)+x],Net_1.nodes[i+Data_1.height_amount+x],Net_1.nodes[i+x],i))
		#debugowanie, wypisywanie wezlow elementu
	#print("element_id:",Net_1.elements[i-1].element_id,"...",Net_1.elements[i-1].id_1.id,Net_1.elements[i-1].id_2.id,Net_1.elements[i-1].id_3.id,Net_1.elements[i-1].id_4.id)
	
	if(i%(Data_1.height_amount-1)==0):
		x+=1


E=np.zeros(shape=(ile_pc*ile_pc,1))
N=np.zeros(shape=(ile_pc*ile_pc,1))

Wagi=np.zeros(shape=(ile_pc*ile_pc,1))


J=np.zeros(shape=(ile_pc*ile_pc,4)) #Macierz Jakobianów
J_1=np.zeros(shape=(ile_pc*ile_pc,4)) #Odwrotność Jakobianów
det_J=np.zeros(shape=(ile_pc*ile_pc,1)) #wyznaczniki Jakobianów

dN_dX=np.zeros(shape=(ile_pc*ile_pc,4))
dN_dY=np.zeros(shape=(ile_pc*ile_pc,4))

dN_dE=np.zeros(shape=(ile_pc*ile_pc,4))
dN_dN=np.zeros(shape=(ile_pc*ile_pc,4))

dX_dE=np.zeros(shape=(ile_pc*ile_pc,1))
dX_dN=np.zeros(shape=(ile_pc*ile_pc,1))
dY_dE=np.zeros(shape=(ile_pc*ile_pc,1))
dY_dN=np.zeros(shape=(ile_pc*ile_pc,1))

#ZAWSZE 4x4
H=np.zeros(shape=(4,4))#4x4
suma_H=np.zeros(shape=(4,4))
N_ksztalty=np.zeros(shape=(ile_pc*ile_pc,4))
C=np.zeros(shape=(4,4))
suma_C=np.zeros(shape=(4,4))
HBC=np.zeros(shape=(4,4))

#Wyznaczenie wektora P
P=np.zeros(shape=(4,1))

#Tworzenie globalnych macierzy C i H, oraz wektora P
P_glob=np.zeros(shape=(Data_1.nodes_amount,1))
H_glob=np.zeros(shape=(Data_1.nodes_amount,Data_1.nodes_amount))
C_glob=np.zeros(shape=(Data_1.nodes_amount,Data_1.nodes_amount))


for i in range(Data_1.elements_amount):	
	elem4(E,N,ile_pc,dN_dE,dN_dN,N_ksztalty,Wagi)	
	tab=Net_1.elements[i].give_points()
	Jakobian(J,J_1,det_J,tab[0],tab[1],dN_dN,dN_dE,dX_dE,dX_dN,dY_dN,dY_dE,ile_pc)
	
	tworz_H(dN_dX,dN_dY,dN_dE,dN_dN,dX_dN,dX_dE,dY_dE,dY_dN,det_J,H,ile_pc,Wagi,k,Net_1.elements[i])
	tworz_C(N_ksztalty,det_J,Wagi,C,Data_1.rho,Data_1.c,ile_pc,Net_1.elements[i])
	SZEROKOSC_ELEMENTU=(Data_1.width/(Data_1.width_amount-1))	
	#print("SZEROKOSC ELEMENTU: ",SZEROKOSC_ELEMENTU)
	WYSOKOSC_ELEMENTU=(Data_1.height/(Data_1.height_amount-1)) 
	#print("WYSOKOSC ELEMENTU: ",WYSOKOSC_ELEMENTU)
	N_local = np.zeros(shape=(ile_pc*ile_pc, 4)) # funkcje kształtów dla poszczególnych boków
	tworz_HBC_i_P(SZEROKOSC_ELEMENTU,WYSOKOSC_ELEMENTU,Data_1.alfa,ile_pc,HBC,Net_1.elements[i],E,N,P,Data_1.t_surroundings,N_local)
	
	#suma_H=np.add(suma_H,H)	#H dla poszczególnych elementów są poprawne
	#suma_C=np.add(suma_C,C)

		
	#Tworzenie Globalnego C oraz H
	for j in range(4):
		for f in range(4):			
			H_glob[Net_1.elements[i].id_list[j]-1][Net_1.elements[i].id_list[f]-1]+=Net_1.elements[i].H[j][f]
			C_glob[Net_1.elements[i].id_list[j]-1][Net_1.elements[i].id_list[f]-1]+=Net_1.elements[i].C[j][f]

	#Tworzenie P globalnego
	for j in range(4):
		P_glob[Net_1.elements[i].id_list[j]-1]+=Net_1.elements[i].P[j]



		
#Sumy lokalnych macierzy H i C

#suma_H=np.divide(suma_H,9)
#print("Suma macierzy lokalnych H")
#for i in range(4):
	#print(suma_H[i])

#suma_C=np.divide(suma_C,9)
#print("\nSuma macierzy lokalnych C")
#for i in range(4):
	#print(suma_C[i])

#print("H globalne:")
#for i in range(Data_1.nodes_amount):
	#print(H_global[i])

#Wypisywanie macierzy/wektorów H,C,P
print("\n\nH Globalna (uwzglednia HBC)")
for i in range(Data_1.nodes_amount):#(20):
	print(H_glob[i])	

#print("\n\nC Globalna")
#for i in range(Data_1.nodes_amount):#(20):
	#print(C_glob[i])	

print("\n\nP globalne:\n",P_glob)


#SYMULACJA
#Kroki Czasowe
T0=[]
Pv=[]
current_time=0

while current_time<Data_1.simulation_time:
	#print("\nAKTUALNY CZAS SYMULACJI: ",current_time+Data_1.tau)
	
	#wyznaczenie [C]/dt
	C_div_dt=np.zeros(shape=(Data_1.nodes_amount,Data_1.nodes_amount))
	for i in range(Data_1.nodes_amount):
		for j in range(Data_1.nodes_amount):
			C_div_dt[i][j]=(C_glob[i][j]/Data_1.tau)

	#TWORZENIE P^

		#tworzenie wektoa {t0}	
	if	len(T0)==0:
		for i in range(Data_1.nodes_amount):
			T0.append(Net_1.nodes[i].t0)
	else:
		for i in range(Data_1.nodes_amount):
			T0[i]=Net_1.nodes[i].t0				

		#print("\nWektor {t0}")
		#print(T0)
		
		#[C]/dt*{t0}
	if len(Pv)==0:
		for i in range(Data_1.nodes_amount): 
		    tmp=0
		    for j in range(Data_1.nodes_amount):
		        tmp+=C_div_dt[i][j]*T0[j]
		    Pv.append(tmp)
	else:
		for i in range(Data_1.nodes_amount): 
		    tmp=0
		    for j in range(Data_1.nodes_amount):
		        tmp+=C_div_dt[i][j]*T0[j]
		    Pv[i]=tmp

			    
		#sumowanie z {P}
	for i in range(Data_1.nodes_amount):
	    Pv[i]+=P_glob[i]
	#print("\nWektor P^:")
	#print(Pv)    	

	
	#TWORZENIE H^
	Hv=np.zeros(shape=(Data_1.nodes_amount,Data_1.nodes_amount))
	for i in range(Data_1.nodes_amount):
		for j in range(Data_1.nodes_amount):
			Hv[i][j]+=(H_glob[i][j]+C_div_dt[i][j])
	
	#print("\nMacierz H^:")
	#for i in range(Data_1.nodes_amount):
		#print(Hv[i])

	#H^(-1)
	Hv=np.linalg.inv(Hv)
	
	#WYZNACZANIE {t} => {t}=H^(-1)*P^
	for i in range(Data_1.nodes_amount): #H^(-1)*P^
	    tmp=0
	    for j in range(Data_1.nodes_amount):
	        tmp+=Hv[i][j]*Pv[j]
	    T0[i]=tmp

	minimal_temp=T0[0]
	maximal_temp=T0[0]
	for i in range(Data_1.nodes_amount):
		if T0[i] <minimal_temp:
		    minimal_temp=T0[i]
		if T0[i] >maximal_temp:
		    maximal_temp=T0[i]    
	#print("Minimalna temp: ",minimal_temp)
	#print("Maksymalna temp: ",maximal_temp)

	print(current_time+Data_1.tau," ",minimal_temp," ",maximal_temp)	

	#Przypisanie nowych temperatur do elementów
	for i in range(Data_1.nodes_amount):
	    Net_1.nodes[i].t0=T0[i]

	current_time+=Data_1.tau
	   