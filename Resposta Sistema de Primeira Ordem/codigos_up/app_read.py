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


dados = np.load(r"C:\Users\Windows 10\OneDrive\Área de Trabalho\Victor\ensaio_principal.npy")

tempo = dados[:,0]
r = dados[:,1]
y = dados[:,2]

##########################################



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
plt.plot(tempo,y,'-ro',linewidth=1.2)
plt.xlabel('Tempo(s)')
plt.ylabel('Tensão (V)')
plt.grid()
# plt.title('Tensão de Saída - Malha Aberta')
plt.show()


