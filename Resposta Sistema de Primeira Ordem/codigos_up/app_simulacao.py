"""
Bancada Motor-Gerador
UFPA - Campus Tucuruí
Monitoria de Sistemas de Controle para Engenharia - PGRAD - MONITORIA 03/2020
Coodenador: Cleison Daniel Silva
Bolsista: Felipe Silveira Piano
Data: 27/09/2020
"""


import numpy as np
import matplotlib.pyplot as plt
import control as ct


dados = np.load(r"C:\Users\Windows 10\OneDrive\Área de Trabalho\Victor\ensaio_principal.npy")

tempo = dados[:,0]
r = dados[:,1]
y = dados[:,2]

##########################################
u_barra = 6.5
y_barra = 1.89




########################

Km = 0.527
tau = 0.0374

Gs = ct.tf([Km],[tau, 1])

_, y_modelo = ct.forced_response(Gs, T = tempo, U = r- u_barra)
y_modelo = y_modelo + y_barra

plt.figure(figsize=(10,10))
plt.subplot(211)
plt.plot(tempo,r,'-b',linewidth=1.2)
plt.xlabel('Tempo(s)')
plt.ylabel('Tensão (V)')
plt.grid()
plt.title('Onda Quadrada - Malha Aberta')
plt.legend(loc='lower right', labels=('Sinal de Entrada','Sinal de Saída'))

plt.subplot(212)
#plt.plot(tempo,r,'-b',tempo,y,'-r',linewidth=1.2)
plt.plot(tempo,y,'-ro' ,tempo, y_modelo,'-ko',linewidth=1.2)
plt.xlabel('Tempo(s)')
plt.ylabel('Tensão (V)')
plt.grid()
# plt.title('Tensão de Saída - Malha Aberta')
plt.show()


