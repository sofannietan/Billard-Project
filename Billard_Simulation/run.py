import numpy as np
from simul2 import Simul     
from animate import Animate 
import matplotlib.pyplot as plt
import time

# fonction permettant de simuler la disposition des boules de billard
def billard_position(r, Lx, Ly):
    D = 2 * r
    e = 0.05 # écart epsilon entre les boules
    S = D + e
    dy = S * np.sqrt(3) / 2
    P = np.zeros((16, 2))
    x_milieu, y_milieu= Lx / 2, 3 * Ly / 4
    i = 0
    for j in range(5):
        y = y_milieu + j * dy
        row_start_x = x_milieu - (j* S) / 2
        for col in range(j+1):
            P[i, :] = [row_start_x + col * S, y]
            i += 1
    P[15, :] = [Lx / 2, Ly / 5] #Boule blanche
    return P #renvoie la liste des 16 positions des boules

def main(nframes, simul_time, v0, pos_init=None):
    Lx, Ly = 30, 60 
    sigma = 60/72
    if pos_init is None:
        pos_init = billard_position(sigma, Lx, Ly) 
    vitesse_initiale = np.zeros((16, 2))
    vitesse_initiale[15, 1] = v0 #vitesse initiale selon y pour la 16e buole
    simulation = Simul(simul_time, sigma, Lx, Ly, pos=pos_init, vit=vitesse_initiale)
    return simulation, pos_init 
#pour visualiser l'animation
def animate_simulation(nframes, simul_time, v0):
    simulation, _ = main(nframes, simul_time, v0, None)
    animate = Animate(simulation)
    animate.go(nframes=nframes)
animate_simulation(500, 10, 20)

#sans l'animation, pour pouvoir calculer rapidement l'erreur 
def sans_animation(nframes, simul_time, v0, pos_init):
    vitesse_initiale = np.zeros((16, 2))
    vitesse_initiale[15, 1] = v0
    sigma = 60/72
    Lx, Ly = 30, 60
    simulation = Simul(simul_time, sigma, Lx, Ly, pos=pos_init.copy(), vit=vitesse_initiale)
    dt= simul_time / nframes
    #sur la moitié des frames, on simule le trajet des boules
    for k in range(nframes // 2):
        simulation.md_step(dt)
    #puis à la moitié, on inverse toutes les vitesses pour le retournement temporel
    simulation.reverse_velocities()
    #on laisse avancer la simulation dans l'autre sens, on observe bien que les boules effectuent leur trajet en sens inverse
    for l in range(nframes // 2):
        simulation.md_step(dt)
        
    diff = simulation.position -pos_init
    #on définit comme métrique l'erreur qyadratique moyenne entre la position initiale des boules et la position finale après retournement temporel
    erreur = np.sqrt(np.mean(np.sum(diff**2, axis=1)))
    
    return erreur

sigma = 60/72   #rayon des boules
Lx, Ly = 30, 60 #largeur et longueur de la table
simul_times= np.linspace(5, 100, 300)#on fait varier le temps de simulation  (on a pris 300 points pour le graphe du compte rendu)
#simul_times= np.linspace(0.1, 10, 100) pour zoomer sur les premières collisions (figure 2)
evol_erreur= np.zeros((len(simul_times),5))
print("Début du calcul de l'erreur")
for k in range(5): #on va moyenner sur 5 simulations avec un bruit gaussen différent
    position_init = billard_position(sigma, Lx, Ly)+ np.random.normal(size=(16,2))*1e-2 #bruit gaussien
    for i, t in enumerate(simul_times):
        evol_erreur[i, k] = sans_animation(400, t, 15, position_init)
    print('Etape:', k+1, '/5')

plt.figure(figsize=(10, 6))
plt.plot(simul_times, np.mean(evol_erreur, axis=1), '+', color='blue', markersize=4)
plt.yscale("log")
plt.xlabel("Temps de simulation")
plt.ylabel("Erreur quadratique moyenne")
plt.title("Evolution de l'erreur quadratique moyenne lors d'un retournement temporel")
plt.grid(True, which="both", alpha=0.3)
plt.show()