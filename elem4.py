import math
import numpy as np
def elem4(E,N,ile_pc,dN_dE,dN_dN,N_ksztalty,Wagi):
	
	if(ile_pc==2):
		temp=1/math.sqrt(3)
		E[0] = -temp
		E[1] = temp
		E[2] = temp
		E[3] = -temp

		N[0] = -temp
		N[1] = -temp
		N[2] = temp
		N[3] = temp
		Wagi[0] = Wagi[1] = Wagi[2] = Wagi[3] = 1
		

	if(ile_pc==3):
		temp = math.sqrt(3/5)
		temp2 = 5.0 / 9.0
		temp3 = 8.0 / 9.0		

		E[0] = -temp
		E[3] = -temp
		E[6] = -temp

		E[1] = 0.0
		E[4] = 0.0
		E[7] = 0.0

		E[2] = temp
		E[5] = temp
		E[8] = temp

		N[0] = -temp		
		N[1] = -temp		
		N[2] = -temp
		
		N[3] = 0.0		
		N[4] = 0.0		
		N[5] = 0.0
		
		N[6] = temp		
		N[7] = temp		
		N[8] = temp

		Wagi[0] = temp2 * temp2
		Wagi[1] = temp2 * temp3
		Wagi[2] = temp2 * temp2
		Wagi[3] = temp2 * temp3
		Wagi[4] = temp3 * temp3
		Wagi[5] = temp2 * temp3
		Wagi[6] = temp2 * temp2
		Wagi[7] = temp2 * temp3
		Wagi[8] = temp2 * temp2

		

	if ile_pc==4:
		temp1= (1/35)*math.sqrt(525+70*math.sqrt(30))
		temp2 = (1.0 / 35.0) * math.sqrt(525.0 - 70.0 * math.sqrt(30.0))
		temp3 = (1.0 / 36.0) * (18.0 - math.sqrt(30.0))
		temp4 = (1.0 / 36.0) * (18.0 + math.sqrt(30.0))

		E[0] = E[4] = E[8] = E[12] = -temp1
		E[1] = E[5] = E[9] = E[13] = -temp2
		E[2] = E[6] = E[10] = E[14] = temp2
		E[3] = E[7] = E[11] = E[15] = temp1

		N[0] = N[1] = N[2] = N[3] = -temp1
		N[4] = N[5] = N[6] = N[7] = -temp2
		N[8] = N[9] = N[10] = N[11] = temp2
		N[12] = N[13] = N[14] = N[15] = temp1

		Wagi[0] = temp3 * temp3
		Wagi[1] = temp3 * temp4
		Wagi[2] = temp3 * temp4
		Wagi[3] = temp3 * temp3
		Wagi[4] = temp4 * temp3
		Wagi[5] = temp4 * temp4
		Wagi[6] = temp4 * temp4
		Wagi[7] = temp4 * temp3
		Wagi[8] = temp4 * temp3
		Wagi[9] = temp4 * temp4
		Wagi[10] = temp4 * temp4
		Wagi[11] = temp4 * temp3
		Wagi[12] = temp3 * temp3
		Wagi[13] = temp3 * temp4
		Wagi[14] = temp3 * temp4
		Wagi[15] = temp3 * temp3	


	#Wypełnianie tablic dN_dN , dN_dE,N_ksztalty
	for i in range(ile_pc*ile_pc):
		dN_dE[i][0] = -0.25 * (1 - N[i])
		dN_dE[i][1] = 0.25 * (1 - N[i])
		dN_dE[i][2] = 0.25 * (1 + N[i])
		dN_dE[i][3] = -0.25 * (1 + N[i])

		dN_dN[i][0] = -0.25 * (1 - E[i])
		dN_dN[i][1] = -0.25 * (1 + E[i])
		dN_dN[i][2] = 0.25 * (1 + E[i])
		dN_dN[i][3] = 0.25 * (1 - E[i])

		N_ksztalty[i][0] = (1.0 / 4.0) * (1 - E[i]) * (1 - N[i])
		N_ksztalty[i][1] = (1.0 / 4.0) * (1 + E[i]) * (1 - N[i])
		N_ksztalty[i][2] = (1.0 / 4.0) * (1 + E[i]) * (1 + N[i])
		N_ksztalty[i][3] = (1.0 / 4.0) * (1 - E[i]) * (1 + N[i])


