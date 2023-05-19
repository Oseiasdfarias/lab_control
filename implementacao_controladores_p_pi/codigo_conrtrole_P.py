"""
Bancada Motor-Gerador
UFPA - Campus Tucuruí
Monitoria de Sistemas de Controle para Engenharia - PGRAD - MONITORIA 03/2020
Coodenador: Cleison Daniel Silva
Bolsista: Felipe Silveira Piano
Data: 27/09/2020
"""

# gerenciador de dispositivo - encontrar porta COM

# from pyserial import Serial
import numpy as np
import matplotlib.pyplot as plt            # noqa: F401
import time as t
from scipy.signal import square, sawtooth  # noqa: F401
import serial

##########################################
# Tensão de alimentação da bancada
amplitude_maxima = 15

numAmostras = 400
tempo = np.zeros(numAmostras)
y = np.zeros(numAmostras)

Ts = 0.02

fre = 0.5
Amplitude = 0.5
ponto_de_operacao = 7.5

nivel_dc_saida = 2.266

# a = 2*np.ones(int(numAmostras/2))
# b = 4*np.ones(int(numAmostras/2))
# u = np.concatenate([a,b]) #degrau

r = np.zeros(numAmostras)
u = np.zeros(numAmostras)

toc = np.zeros(numAmostras)
# #####################

for n in range(numAmostras):
    r[n] = Amplitude*square(2*np.pi*fre*n*Ts) + ponto_de_operacao
    # r[n] = Amplitude*sawtooth(2*np.pi*fre*n*Ts) + setpoint
    # r[n] = Amplitude*np.sin(2*np.pi*fre*n*Ts) + setpoint
    # r[n] = u[n]

# print('\nEstabelecendo conexão.')
# conexao = serial.Serial(port='COM5', baudrate=9600, timeout=0.005)

t.sleep(1)
print('\nIniciando coleta.')

print('\nEstabelecendo conexão.')
# conexao = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=0.005)
conexao = serial.Serial(port='COM8', baudrate=9600, timeout=0.005)

# #_____________ Loop principal de controle _____________##
nivel_dc_entrada = ponto_de_operacao

# Ganho do Controlador Proporcional
Kp = 2.296

for n in range(numAmostras):
    tic = t.time()
    if (conexao.inWaiting() > 0):
        y[n] = conexao.readline().decode()

    # remove o nivel_dc_saida
    sinal_medido = y[n] - nivel_dc_saida
    # calcula o erro
    e = r[n] - sinal_medido

    # primeiras 50 amostras
    if (n < 50):
        u[n] = nivel_dc_entrada
        r[n] = 0.0
    else:
        u[n] = (Kp*e) + nivel_dc_entrada

    if (u[n] > amplitude_maxima):
        sinal_PWM = 255
    else:
        sinal_PWM = ((u[n])*255)/amplitude_maxima
    # sinal_PWM deve ser um número inteiro entre 0 e 255
    conexao.write(str(round(sinal_PWM)).encode())
    t.sleep(Ts)

    if (n > 0):
        tempo[n] = tempo[n-1] + Ts
    toc[n] = t.time() - tic
