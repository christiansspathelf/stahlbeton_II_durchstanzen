## INPUT
# Platten- und Stützengeometrie
h = 350             # Plattenstärke [mm]
c_nom = 30          # Bewehrungsüberdeckung [mm]

l_x = 8909          # Spannweite in x-Richtung [mm]
l_y = 8909          # Spannweite in y-Richtung [mm]

b1 = 0            # Stützenbreite in y-Richtung [mm]
b2 = 0            # Stützenbreite in x-Richtung [mm]
diam = 400            # Stützendurchmesser [mm]
stuetzenform = 'kreis'

r_sx1 = 1960        # Abstand von Stützenachse zum Nullpunkt des Moments in x-Richtung [mm]
r_sx2 = 1960        # Abstand von Stützenachse zum Nullpunkt des Moments in x-Richtung [mm]
r_sy1 = 1960        # Abstand von Stützenachse zum Nullpunkt des Moments in y-Richtung [mm]
r_sy2 = 1960        # Abstand von Stützenachse zum Nullpunkt des Moments in y-Richtung [mm]

k_e = 1           # Beiwert zur Berücksichtigung von exzentrischen Lasteinleitungen
k = 8       # Stützenposition: 
            #Innenstütze 8; 
            # Randstütze, obere Bewehrung parallel zum Rand 4; 
            # Randstütze mit obere und untere Bewehrung senkrecht zum Rand 8, 
            # Eckstütze mit obere und untere Bewehrung 2

# Baustoffeigenschaften
f_ck = 49.4           # charakteristische Wert der Betondruckfestigkeit [N/mm^2]
f_cd = 49.4         # Bemessungswert der Betondruckfestigkeit [N/mm^2]
tau_cd = 2.1          # Schubspannungsgrenze des Beton [N/mm^2]
f_ctm = 2.6         # Mittelwert der Betonzugfestigkeit [Nmm^2]
D_max = 32          # Grösstkorn des Betons [mm]
gamma_c = 1.5       # Partialbeiwert des Betons [-]

f_sd = 500          # Bemessungswert der Betonstahlfliessgrenze [N/mm^2]
f_sk = 500          # charakteristische Wert der Betonstahlfliessgrenze [N/mm^2]
E_s = 205e3         # Elastizitätsmodul Betonstahl [N/mm^2]


# Bewehrungsparameter
diam_sx = 26        # Nom. Stabdurchmesser der Biegezugbewehrung in x-Richtung
s_x = 150           # Stabstand der Biegezugbewehrung in x-Richtung

diam_sy = 26        # Nom. Stabdurchmesser der Biegezugbewehrung in y-Richtung
s_y = 150           # Stabstand der Biegezugbewehrung in y-Richtung

d_sx = h - c_nom - 0.5*diam_sx              # Statische Höhe der Bewehrung in x-Richtung
d_sy = h - c_nom - diam_sx - 0.5*diam_sy    # Statische Höhe der Bewehrung in y-Richtung
d_v = int(0.5 * (d_sx + d_sy))              # Wirksame statische Hohe [mm]

diam_sw = 18        # Nominelle Durchmesser der Durchstanzbewehrung [mm]
beta = 90           # Orientation der Durchstanzbewehrung zur Mittelebene der Platte [°]            
