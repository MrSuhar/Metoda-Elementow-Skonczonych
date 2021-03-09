def tworz_H(dN_dX,dN_dY,dN_dE,dN_dN,dX_dN,dX_dE,dY_dE,dY_dN,det_J,H,ile_pc,wagi,k,ELEMENT):
	
	for i in range(ile_pc*ile_pc):
		for j in range(4):
			dN_dX[i][j] = (1 / det_J[i]) * (dN_dE[i][j] * dY_dN[i] - dN_dN[i][j] * dY_dE[i]); 
			dN_dY[i][j] = (1 / det_J[i]) * (-dX_dN[i] * dN_dE[i][j] + dX_dE[i] * dN_dN[i][j]); 

	for i in range(4):
			for j in range(4):
				H[i][j]=0

	for x in range(ile_pc*ile_pc):
		for i in range(4):
			for j in range(4):
				H[i][j]+=wagi[x]*det_J[x]*k*((dN_dX[x][i]*dN_dX[x][j])+(dN_dY[x][i]*dN_dY[x][j])) 
	
	#print("Macierz H dla elementu: ",ELEMENT.element_id)
	#for i in range(4):
		#print(H[i])

	#Pezypisanie macierzy do elementu
	ELEMENT.H=H	
	
    
    		
