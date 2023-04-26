import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import MultipleLocator


# Berechnung der Nachweisumfang
def nachweisumfang(d_v, geometry, diam, b1, b2):
    if geometry == 'kreis':
        u = math.pi * (diam + d_v)
    elif geometry == 'rechteck':
        u = min(2 * (b1 + b2) + math.pi * d_v, (12 + math.pi) * d_v)
    return u


# Berechnung der Stützstreifenbreite
def stuetzstreifenbreite(*momentennullpunkt):
    produkt = 1
    for i in momentennullpunkt:
        produkt = produkt * i
    return 1.5 * (produkt) ** (1/len(momentennullpunkt))    # Stuetzstreifenbreite b_s


# Biegewiderstand einer Stahlbetonplatte
def biegewiderstand(diam_s, s, d_s, f_sd, f_cd):
    a_s = (math.pi*diam_s ** 2)/ (4 * s / 1000)
    return a_s * f_sd * (d_s - (a_s * f_sd)/(2 * 1000 * f_cd))


# Verbundschubspannung [N/mm^2], SIA 262, Gl. (103)
def verbundschub(f_ctm, gamma_c):
    return 1.4 * f_ctm / gamma_c 


# Querkraft-Plattenrotationsbeziehung
def plattenrot(V_di, k, l_x, l_y, m_Rdx, m_Rdy, f_sd, E_s, d_sx, d_sy):
    V_flex = [(k * m_Rdx / 1e6), (k * m_Rdy / 1e6)]             # Querkraft wobei die Biegetragsicherheit der Platte erreicht wird [kN]
    r_s = [(0.22 * l_x), (0.22 * l_y)]                          # Momentennullpunktabstand in x- und y-Richtung
    return  [(1.5 * (r_s[0] / d_sx) * (f_sd / E_s) * (V_di / V_flex[0]) ** (3/2)),       # Plattenrotation psi [rad]
            (1.5 * (r_s[1] / d_sy) * (f_sd / E_s) * (V_di / V_flex[1]) ** (3/2))]


# Beiwert zur Berücksichtigung der Plattenrotation
def rotationsbeiwert(phi, d_sx, d_sy, k_g):
    return [(1/(0.45 + 0.18 * phi[0] * d_sx * k_g)),
           (1/(0.45 + 0.18 * phi[1] * d_sy * k_g))]         # Beiwert k_r gemäss SIA 262(2013), Gl. (58)


# Plot-Funktion
def plot_durchstanzen(psi, V_di, k, m_Rdx, m_Rdy, V_Rdc, V_Rd_in, V_Rd_sup, V_Rds, idx_c, idx_in, idx_sup):
    # Ploteinstellungen
    fsize = 11      # Schriftgrösse Allgemein
    tsize = 9       # Schriftgrösse Legende
    tdir = 'in'
    major = 5.0     # Länge major ticks
    minor = 3.0     # Länge minor ticks
    lwidth = 0.5    # Rahmendicke
    lhandle = 2.0   # Länge handle in Legende
    
    # Font 
    plt.style.use('default')
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral'
    plt.rcParams['font.size'] = fsize
    plt.rcParams['legend.fontsize'] = tsize
    plt.rcParams['xtick.direction'] = tdir
    plt.rcParams['ytick.direction'] = tdir
    plt.rcParams['xtick.major.size'] = major
    plt.rcParams['xtick.minor.size'] = minor
    plt.rcParams['ytick.major.size'] = major
    plt.rcParams['ytick.minor.size'] = minor
    plt.rcParams['axes.linewidth'] = lwidth
    plt.rcParams['legend.handlelength'] = lhandle    
    
    
    # Plot initialisieren
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,6), sharex=True, sharey=True)

    # Plot für x-Richtung
    ax1.plot(psi[0], (np.clip(V_di , 0 , (k * m_Rdx / 1e6))), label='Querkraft-Plattenrotation', color='black')  # Begrenzung auf die plastische Biegewiderstand der Platte
    ax1.plot(psi[0], V_Rdc[0], label='Widerstand ohne Durchstanzbewehrung', color='green')
    ax1.plot(psi[0], V_Rd_in[0], label='Widerstand inneren Nachweisschnitt', color='blue')
    ax1.plot(psi[0], V_Rd_sup[0], label='Obere Schubspannungsgrenze des Betons', color='darkgreen')
    ax1.plot(psi[0], V_Rds[0], label='Widerstand Durchstanzbewehrung', color='darkblue')

    ax1.plot(psi[0][idx_c[0]], V_Rdc[0][idx_c[0]], 
            marker = 'o', markeredgecolor = 'black', markerfacecolor = 'white')
    ax1.plot(psi[0][idx_in[0]], V_Rd_in[0][idx_in[0]], 
            marker = 'o', markeredgecolor = 'black', markerfacecolor = 'white')
    ax1.plot(psi[0][idx_sup[0]], V_Rd_sup[0][idx_sup[0]], 
            marker = 'o', markeredgecolor = 'black', markerfacecolor = 'white')

    ax1.fill_between(psi[0], V_Rd_in[0], color = 'blue', alpha = 0.5)
    ax1.fill_between(psi[0], V_Rd_sup[0], color = 'green', alpha = 0.5)
    ax1.fill_between(psi[0], V_Rdc[0], color = 'lightgreen')
    
    ax1.annotate('$V_{Rd,c} = $%.1f'%(V_Rdc[0][idx_c[0]]),
                xy=(psi[0][idx_c[0]], V_Rdc[0][idx_c[0]]), 
                xytext=(4, 2), textcoords='offset points', ha = 'left', va='bottom')
    ax1.annotate('$V_{Rd,in} = $%.1f'%(V_Rd_in[0][idx_in[0]]),
                xy=(psi[0][idx_in[0]], V_Rd_in[0][idx_in[0]]), 
                xytext=(4, 2), textcoords='offset points', ha = 'left', va='bottom')
    ax1.annotate('$V_{Rd,sup} = $%.1f'%(V_Rd_sup[0][idx_sup[0]]),
                xy=(psi[0][idx_sup[0]], V_Rd_sup[0][idx_sup[0]]), 
                xytext=(4, 2), textcoords='offset points', ha = 'left', va='bottom')

    ax1.set_xlabel('$\psi_x$ [rad]')
    ax1.set_ylabel('$V_{Rd}$ [kN]')

    # Plot für y-Richtung
    ax2.plot(psi[1], (np.clip(V_di , 0 , (k * m_Rdy / 1e6))), label='Last-Plattenrotation', color='black')  # Begrenzung auf die plastische Biegewiderstand der Platte
    ax2.plot(psi[1], V_Rdc[1], label='Widerstand ohne Durchstanzbewehrung', color='green')
    ax2.plot(psi[1], V_Rd_in[1], label='Widerstand inneren Nachweisschnitt', color='blue')
    ax2.plot(psi[1], V_Rd_sup[1], label='Obere Schubspannungsgrenze des Betons', color='darkgreen')
    ax2.plot(psi[1], V_Rds[1], label='Widerstand Durchstanzbewehrung', color='darkblue')
    ax2.legend(frameon=False)

    ax2.plot(psi[1][idx_c[1]], V_Rdc[1][idx_c[1]], 
            marker = 'o', markeredgecolor = 'black', markerfacecolor = 'white')
    ax2.plot(psi[1][idx_in[1]], V_Rd_in[1][idx_in[1]], 
            marker = 'o', markeredgecolor = 'black', markerfacecolor = 'white')
    ax2.plot(psi[1][idx_sup[1]], V_Rd_sup[1][idx_sup[1]], 
            marker = 'o', markeredgecolor = 'black', markerfacecolor = 'white')

    ax2.fill_between(psi[1], V_Rd_in[1], color = 'blue', alpha = 0.5)
    ax2.fill_between(psi[1], V_Rd_sup[1], color = 'green', alpha = 0.5)
    ax2.fill_between(psi[1], V_Rdc[1], color = 'lightgreen')
    
    ax2.annotate('$V_{Rd,c} = $%.1f'%(V_Rdc[1][idx_c[1]]),
                xy=(psi[1][idx_c[1]], V_Rdc[1][idx_c[1]]), 
                xytext=(4, 2), textcoords='offset points', ha = 'left', va='bottom')
    ax2.annotate('$V_{Rd,in} = $%.1f'%(V_Rd_in[1][idx_in[1]]),
                xy=(psi[1][idx_in[1]], V_Rd_in[1][idx_in[1]]), 
                xytext=(4, 2), textcoords='offset points', ha = 'left', va='bottom')
    ax2.annotate('$V_{Rd,sup} = $%.1f'%(V_Rd_sup[1][idx_sup[1]]),
                xy=(psi[1][idx_sup[1]], V_Rd_sup[1][idx_sup[1]]), 
                xytext=(4, 2), textcoords='offset points', ha = 'left', va='bottom')

    ax2.set_xlabel(r'$\psi_y$ [rad]')
    ax2.set_ylabel(r'$V_{Rd}$ [kN]')
    
    plt.gca().xaxis.set_minor_locator(MultipleLocator(.5))
    plt.gca().yaxis.set_minor_locator(MultipleLocator(500))
    
    plt.savefig('durchstanzen.pdf')
    
    plt.show()

