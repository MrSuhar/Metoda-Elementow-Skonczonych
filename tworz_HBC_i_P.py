import numpy as np
import math


def tworz_HBC_i_P(SZEROKOSC_ELEMENTU,WYSOKOSC_ELEMENTU, ALFA, ile_pc, HBC, ELEMENT, E, N, P,T_SURROUNDINGS,N_local):
    Wagi_podstawowe=np.zeros(shape=(ile_pc,1))

    if ile_pc==2:
        Wagi_podstawowe[0]=Wagi_podstawowe[1]=1
    if ile_pc==3:        
        Wagi_podstawowe[0]= 5.0 / 9.0
        Wagi_podstawowe[2]= 5.0 / 9.0
        Wagi_podstawowe[1]=8.0 / 9.0
    if ile_pc==4:
        Wagi_podstawowe[0] = Wagi_podstawowe[3] = (1.0 / 36.0) * (18.0 - math.sqrt(30.0))
        Wagi_podstawowe[1] = Wagi_podstawowe[2] = (1.0 / 36.0) * (18.0 + math.sqrt(30.0))


    for i in range(4):
        P[i] = 0
        for j in range(4):
            HBC[i][j] = 0

     # bok 4---1 (lewy)
    if ELEMENT.id_4.bc == 1 and ELEMENT.id_1.bc == 1:
        for i in range(ile_pc):
            N_local[i*ile_pc][0] = (1/2)*(1-N[i*ile_pc])  # N1
            N_local[i*ile_pc][3] = (1/2)*(1+N[i*ile_pc])  # N4

        print("N_local dla lewego boku, element:",ELEMENT.element_id)
        print(N_local[0],"\n",N_local[1],"\n",N_local[2],"\n",N_local[3])

        for q in range(ile_pc):
            for i in range(4):
                for j in range(4):
                    print("N_local [q*ile_pc][i]*N_local [q*ile_pc][j]:",N_local[q*ile_pc][i]*N_local[q*ile_pc][j])
                    #print("N_local [q*ile_pc][j]:",N_local[q*ile_pc][j])
                    #print(N_local[0],"\n",N_local[1],"\n",N_local[2],"\n",N_local[3])
                    HBC[i][j] += Wagi_podstawowe[q]*(WYSOKOSC_ELEMENTU/2)*ALFA*N_local[q*ile_pc][i]*N_local[q*ile_pc][j]

            # Wyliczenie P
        for q in range(ile_pc):
            for i in range(4):
                P[i] += Wagi_podstawowe[q]*(WYSOKOSC_ELEMENTU/2)*T_SURROUNDINGS*ALFA*N_local[q*ile_pc][i]

        for i in range(ile_pc):
            N_local[i*ile_pc][0] = 0
            N_local[i*ile_pc][3] = 0

     # bok 2---3 (prawy)
    if ELEMENT.id_2.bc == 1 and ELEMENT.id_3.bc == 1:
        for i in range(ile_pc):
            N_local[ile_pc-1+i*ile_pc][1]=(1/2)*(1-N[ile_pc-1+i*ile_pc]) #N2
            N_local[ile_pc-1+i*ile_pc][2]=(1/2)*(1+N[ile_pc-1+i*ile_pc]) #N3

        for q in range(ile_pc):    
            for i in range(4):
                for j in range(4):                        
                    HBC[i][j] += Wagi_podstawowe[q]*(WYSOKOSC_ELEMENTU/2)*ALFA*N_local[ile_pc-1+q*ile_pc][i]*N_local[ile_pc-1+q*ile_pc][j]

            # Wyliczenie P
        for q in range(ile_pc): 
            for i in range(4):
                P[i]+=Wagi_podstawowe[q]*(WYSOKOSC_ELEMENTU/2)*T_SURROUNDINGS*ALFA*N_local[ile_pc-1+q*ile_pc][i]

        for i in range(ile_pc):
            N_local[ile_pc-1+i*ile_pc][1]=0
            N_local[ile_pc-1+i*ile_pc][2]=0 

    # bok 1---2 (dolny)
    if ELEMENT.id_1.bc == 1 and ELEMENT.id_2.bc == 1:
        for i in range(ile_pc):
            N_local[i][0]=(1/2)*(1-E[i]) #N1
            N_local[i][1]=(1/2)*(1+E[i]) #N2

        for q in range(ile_pc):    
            for i in range(4):
                for j in range(4):                        
                    HBC[i][j] += Wagi_podstawowe[q]*(SZEROKOSC_ELEMENTU/2)*ALFA*N_local[q][i]*N_local[q][j]

            # Wyliczenie P
        for q in range(ile_pc): 
            for i in range(4):
                P[i]+=Wagi_podstawowe[q]*(SZEROKOSC_ELEMENTU/2)*T_SURROUNDINGS*ALFA*N_local[q][i]

        for i in range(ile_pc):
            N_local[i][0]=0
            N_local[i][1]=0

     # bok 3---4 (górny)
    if ELEMENT.id_3.bc == 1 and ELEMENT.id_4.bc == 1:
        for i in range(ile_pc):
            N_local[ile_pc*(ile_pc-1)+i][2]=(1/2)*(1-E[ile_pc*(ile_pc-1)+i]) #N1
            N_local[ile_pc*(ile_pc-1)+i][3]=(1/2)*(1+E[ile_pc*(ile_pc-1)+i]) #N2

        for q in range(ile_pc):    
            for i in range(4):
                for j in range(4):                        
                    HBC[i][j] += Wagi_podstawowe[q]*(SZEROKOSC_ELEMENTU/2)*ALFA*N_local[ile_pc*(ile_pc-1)+q][i]*N_local[ile_pc*(ile_pc-1)+q][j]

            # Wyliczenie P
        for q in range(ile_pc): 
            for i in range(4):
                P[i]+=Wagi_podstawowe[q]*(SZEROKOSC_ELEMENTU/2)*T_SURROUNDINGS*ALFA*N_local[ile_pc*(ile_pc-1)+q][i]

        for i in range(ile_pc):
            N_local[ile_pc*(ile_pc-1)+i][2]=0
            N_local[ile_pc*(ile_pc-1)+i][3]=0                                     

        

    #print("\nMacierz HBC dla elementu: ",ELEMENT.element_id)
    #for i in range(4):
        #print(HBC[i])

    for i in range(4):
        for j in range(4):
            ELEMENT.H[i][j]+=HBC[i][j]

    #print("\nWektor P dla elementu: ",ELEMENT.element_id)
    #print(P)
    ELEMENT.P=P        


