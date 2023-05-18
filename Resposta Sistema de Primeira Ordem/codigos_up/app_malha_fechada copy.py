"""
Bancada Motor-Gerador
UFPA - Campus Tucuruí
Monitoria de Sistemas de Controle para Engenharia - PGRAD - MONITORIA 03/2020
Coodenador: Cleison Daniel Silva
Bolsista: Felipe Silveira Piano
Data: 27/09/2020
"""

import serial
import numpy as np
import matplotlib.pyplot as plt
import time as t
from scipy.signal import square, sawtooth


##########################################

numAmostras = 300
tempo = np.zeros(numAmostras)
y = np.zeros(numAmostras)

Ts = 0.02

fre = 0.5
Amplitude = 0.5
setpoint = 6
# a = 2*np.ones(int(numAmostras/2))
# b = 4*np.ones(int(numAmostras/2))
# u = np.concatenate([a,b]) #degrau
r = np.zeros(numAmostras)
toc = np.zeros(numAmostras)
erro = np.zeros(numAmostras)
u = np.zeros(numAmostras)
######################
Kp = 2.5
# Ki = 1

for n in range(numAmostras):
    r[n] = Amplitude*square(2*np.pi*fre*n*Ts) + setpoint
    # r[n] = Amplitude*sawtooth(2*np.pi*fre*n*Ts) + setpoint
    # r[n] = Amplitude*np.sin(2*np.pi*fre*n*Ts) + setpoint
    # r[n] = u[n]

print('\nEstabelecendo conexão.')
conexao = serial.Serial(port='COM4', baudrate=9600, timeout=0.005)
t.sleep(1)
print('\nIniciando coleta.')

for n in range(numAmostras):
    tic = t.time()

    if (conexao.inWaiting() > 0):

        y[n] = conexao.readline().decode()

    erro[n] = r[n] - (y[n] - 4.56)
    #print(y[n])
    u[n] = (Kp*erro[n]) + 7  # u[n-1] + 2.5*erro[n] - 1.5*erro[n-1] + 5.5  # Controlador Proporcional Integral
    print(u[n])
    if (u[n] >= 7):
        sinal_enviado = 255

    else:
        sinal_enviado = (u[n]*255)/7

    conexao.write(str(round(sinal_enviado)).encode())

    t.sleep(Ts)

    if (n > 0):
        tempo[n] = tempo[n-1] + Ts
    toc[n] = t.time() - tic
conexao.write('0'.encode())
print('\nFim da coleta.')
conexao.close()
print('media=', np.mean(r))

print('\nPeríodo real:', np.mean(toc))
print('Nivel_DC:', np.mean(y[tempo > 2]))

plt.figure(figsize=(10, 10))
plt.subplot(211)
plt.plot(tempo, r + 4.56, '-b', tempo, y , '-ro', linewidth=1.2)
plt.xlabel('Tempo(s)')
plt.ylabel('Tensão (V)')
plt.grid()
plt.title('Onda Quadrada - Malha Aberta')
plt.legend(loc='lower right', labels=('Sinal de Entrada','Sinal de Saída'))

plt.subplot(212)
# plt.plot(tempo,r,'-b',tempo,y,'-r',linewidth=1.2)
plt.plot(tempo, u, '-ko', linewidth=1.2)
plt.xlabel('Tempo(s)')
plt.ylabel('Tensão (V)')
plt.grid()
# plt.title('Tensão de Saída - Malha Aberta')
plt.show()

dados = np.stack((tempo, r, y), axis=-1)

np.savetxt("malha_fechada_40pc_dados_motorgerador.csv", dados, delimiter=";")
# np.save(r"C:\Users\Windows 10\OneDrive\Área de Trabalho\Victor\ensaio_sen02", dados)
