import math
import numpy as np

def Jakobian(J,J_1,det_J,X,Y,dN_dN,dN_dE,dX_dE,dX_dN,dY_dN,dY_dE,ile_pc):
	if ile_pc>1: 
		for i in range(ile_pc*ile_pc):
			dX_dE[i]=0
			dX_dN[i]=0
			dY_dE[i]=0
			dY_dN[i]=0
		
		for i in range(ile_pc*ile_pc):
			for j in range(4):
				dX_dE[i] += (dN_dE[i][j] * X[j])
				dX_dN[i] += (dN_dN[i][j] * X[j])
				dY_dE[i] += (dN_dE[i][j] * Y[j])
				dY_dN[i] += (dN_dN[i][j] * Y[j])

		for i in range(ile_pc*ile_pc):
			J[i][0] = dX_dE[i]
			J[i][1] = dY_dE[i]
			J[i][2] = dX_dN[i]
			J[i][3] = dY_dN[i]
		
		for i in range(ile_pc*ile_pc):
			det_J[i] = (J[i][0]*J[i][3])-(J[i][1]*J[i][2])
			J_1[i][0] = (1/det_J[i])*J[i][3]
			J_1[i][1] = (1/det_J[i])*(J[i][1])
			J_1[i][2] = (1/det_J[i])*(J[i][2])
			J_1[i][3] = (1/det_J[i])*J[i][0]			

		

	