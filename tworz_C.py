def tworz_C(N_ksztalty,det_J,Wagi,C,RHO,WSP_C, ile_pc,ELEMENT):
	for i in range(4):
		for j in range(4):
			C[i][j]=0

	for k in range(ile_pc*ile_pc):
		for i in range(4):
			for j in range(4):
				C[i][j]+=Wagi[k]*det_J[k]*RHO*WSP_C*N_ksztalty[k][i]*N_ksztalty[k][j]
	
	#print("Macierz C dla elementu: ",ELEMENT.element_id)
	#for i in range(4):
		#print(C[i])
		
	ELEMENT.C=C

