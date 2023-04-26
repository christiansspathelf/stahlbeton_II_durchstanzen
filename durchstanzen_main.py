import numpy as np
import math

from funktionen_durchstanzen import *
import input_durchstanzen


# Last-Plattenrotation-Charakteristik (Näherung)
steps = 200
V_di = np.linspace(10,8000,steps)    # Querkraftbeanspruchung [kN]


# Beiwert zur Berücksichigung der Rissverzahnungseffekt anhand des Grösskorns
k_g = 48 / (16 + input_durchstanzen.D_max)


# Bestimmung der Stützstreifenbreite
b_s = stuetzstreifenbreite(input_durchstanzen.r_sx1, input_durchstanzen.r_sx2, input_durchstanzen.r_sy1, input_durchstanzen.r_sy2)
print('b_s = ', b_s)


# Ermittlung der Plattenbiegetragsicherheit
m_Rdx = biegewiderstand(input_durchstanzen.diam_sx, input_durchstanzen.s_x, input_durchstanzen.d_sx, input_durchstanzen.f_sd, input_durchstanzen.f_cd)
print('m_Rdx = ', m_Rdx) 
m_Rdy = biegewiderstand(input_durchstanzen.diam_sy, input_durchstanzen.s_y, input_durchstanzen.d_sy, input_durchstanzen.f_sd, input_durchstanzen.f_cd)
print('m_Rdy = ', m_Rdy) 


# Mindestdurchstanzbewehrung
V_Rdsmin = 0.5 * V_di
A_swmin = (1000 * V_Rdsmin) / (input_durchstanzen.f_sd * input_durchstanzen.k_e * np.sin(input_durchstanzen.beta))
rho_sw_min = 0.005 * ((input_durchstanzen.f_ck / 30) ** (0.5)) * (500 / input_durchstanzen.f_sk)

psi = plattenrot(V_di, input_durchstanzen.k, input_durchstanzen.l_x, input_durchstanzen.l_y, m_Rdx, m_Rdy, input_durchstanzen.f_sd, input_durchstanzen.E_s, input_durchstanzen.d_sx, input_durchstanzen.d_sy)
print('psi[0] =', psi[0])
print('psi[1] =', psi[1])


# Umfang des Nachweisschnitts [mm]
u = nachweisumfang(input_durchstanzen.d_v, input_durchstanzen.stuetzenform, input_durchstanzen.diam, input_durchstanzen.b1, input_durchstanzen.b2)
print('Umfang =', u)


## Durchstanzwiderstand ohne Querkraftbewehrung (LoA III)
k_r =  rotationsbeiwert(psi, input_durchstanzen.d_sx, input_durchstanzen.d_sy, k_g)
print('k_r = ', k_r)

V_Rdc = [(k_r[0] * input_durchstanzen.tau_cd * input_durchstanzen.d_v * u * input_durchstanzen.k_e)/1000,     
         (k_r[1] * input_durchstanzen.tau_cd * input_durchstanzen.d_v * u * input_durchstanzen.k_e)/1000 ]    # SIA 262(2013), Gl. (57)
print('V_Rdc = ', V_Rdc)


# Durchstanzwiderstand ohne Durchstanzbewehrung
idx_c = [(np.argwhere(np.diff(np.sign(V_di - V_Rdc[0]))).flatten()) , 
         (np.argwhere(np.diff(np.sign(V_di - V_Rdc[1]))).flatten())]


## Durchstanzwiderstand mit Querkraftbewehrung
A_sw = 5200
f_bd = verbundschub(input_durchstanzen.f_ctm, input_durchstanzen.gamma_c)

sigma_sd = [((1/6) * (input_durchstanzen.E_s * psi[0]) * (1 + (f_bd / input_durchstanzen.f_sd)*(input_durchstanzen.d_sx / input_durchstanzen.diam_sw))), 
            ((1/6) * (input_durchstanzen.E_s * psi[1]) * (1 + (f_bd / input_durchstanzen.f_sd)*(input_durchstanzen.d_sy / input_durchstanzen.diam_sw)))]


# Bewehrungsspannung auf Fliessgrenze begrenzen
sigma_sd = [np.clip(sigma_sd[0] , 0 , input_durchstanzen.f_sd),
            np.clip(sigma_sd[1] , 0 , input_durchstanzen.f_sd)]
print('sig_sd[0] = ', sigma_sd[0])
print('sig_sd[1] = ', sigma_sd[1])


V_Rds = [(A_sw * sigma_sd[0] * input_durchstanzen.k_e * np.sin(math.radians(input_durchstanzen.beta)) / 1000),
         (A_sw * sigma_sd[1] * input_durchstanzen.k_e * np.sin(math.radians(input_durchstanzen.beta)) / 1000)]


# Durchstanzwiderstand des inneren Nachweisschnitts
V_Rd_in = np.add(V_Rdc,V_Rds)
idx_in = [(np.argwhere(np.diff(np.sign(V_di - V_Rd_in[0]))).flatten()),
          (np.argwhere(np.diff(np.sign(V_di - V_Rd_in[1]))).flatten())]
print('idx_in = ', idx_in[0])


# Obere Schubspannungsgrenze des Durchstanzwiderstands
V_Rd_sup = [((2 * k_r[0] * input_durchstanzen.tau_cd * input_durchstanzen.d_v * u * input_durchstanzen.k_e)/1000),
            ((2 * k_r[0] * input_durchstanzen.tau_cd * input_durchstanzen.d_v * u * input_durchstanzen.k_e)/1000)]
print('k_r = ', k_r)
print('V_Rd,sup = ', V_Rd_sup)


# Begrenzung
V_Rd_sup = np.clip(V_Rd_sup , 0 ,(3.5 * input_durchstanzen.tau_cd * input_durchstanzen.d_v * u * input_durchstanzen.k_e)/1000)
idx_sup = [(np.argwhere(np.diff(np.sign(V_di - V_Rd_sup[0]))).flatten()),
           (np.argwhere(np.diff(np.sign(V_di - V_Rd_sup[1]))).flatten())]


# Plot
plot_durchstanzen(psi, V_di, input_durchstanzen.k, m_Rdx, m_Rdy, V_Rdc, V_Rd_in, V_Rd_sup, V_Rds, idx_c, idx_in, idx_sup)



