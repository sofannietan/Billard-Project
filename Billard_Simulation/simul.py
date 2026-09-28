import numpy as np
import math

class Simul:
    def __init__(self, simul_time, sigma, Lx, Ly, pos, vit):
        np.seterr(all='ignore')
        self.sigma = sigma
        self.Lx = Lx
        self.Ly = Ly
        self.simul_time = simul_time
        self.position = pos  
        if vit is None:
            self.velocity = np.zeros_like(self.position)
            self.velocity[15,:] = [0, 10] 
        else: 
            self.velocity=vit
        self.l, self.m = np.triu_indices(self.position.shape[0], k=1)

    def wall_time(self):
            times = []
            indices = []
            for i in range(self.position.shape[0]):
                xi, yi = self.position[i]
                vxi, vyi = self.velocity[i]
                #on distingue les différents cas
                if vxi > 0:
                    times.append((self.Lx - self.sigma - xi) / vxi)
                    indices.append((i, 0))
                elif vxi < 0:
                    times.append((xi - self.sigma) / -vxi)
                    indices.append((i, 0))
                else:
                    times.append(np.inf)
                    indices.append((i, 0))
                
                if vyi > 0:
                    times.append((self.Ly - self.sigma - yi) / vyi)
                    indices.append((i, 1))
                elif vyi < 0:
                    times.append((yi - self.sigma) / -vyi)
                    indices.append((i, 1))
                else:
                    times.append(np.inf)
                    indices.append((i, 1))

            min = np.argmin(times)
            return times[min], indices[min][0], indices[min][1] #on retourne le minimum du temps de collision murale, la partiule en question et la directon
        
    def pair_time(self):
        
        p1=-1
        p2=-1
        sigma=self.sigma
        dX=self.position[self.l]-self.position[self.m]
        dV=self.velocity[self.l]-self.velocity[self.m]
        A=np.sum(dV**2,axis=1)
        B=2*np.sum(dV*dX,axis=1)
        C=np.sum(dX**2,axis=1)-4*sigma**2
        Delta=B**2-4*A*C
        temps=np.where((B<0)&(C>0)&(Delta>0),(-B-np.sqrt(Delta))/(2*A),np.inf)
        t_min=np.min(temps)
        min=np.argmin(temps)
        p1,p2=self.l[min],self.m[min]
        return t_min, p1,p2 #on retourne le temps de collision entre particules minimal et la paire de particule concernée
    
    def update_velocity(self, particle1, particle2):
        #dans le cas d'une collision entre particules, la fonction permet de mettre à jour les vitesses après le choc
    
        ke_start = (self.velocity[particle1]**2).sum()/2. +(self.velocity[particle2]**2).sum()/2.
        dv = self.velocity[particle1]-self.velocity[particle2]
        r = (self.position[particle1]-self.position[particle2])/(2*self.sigma)
        self.velocity[particle1]-=r*np.dot(r, dv)
        self.velocity[particle2]+=r*np.dot(r, dv)
        ke_end = (self.velocity[particle1]**2).sum()/2. +(self.velocity[particle2]**2).sum()/2.
        assert math.isclose(ke_start,  ke_end)  
    
    
    
    def md_step(self, dt):
        ke_start = (self.velocity**2).sum()/2
        temps_restant = dt
        
        while temps_restant>0:
            w_time, particle, direction= self.wall_time()
            c_time,p1,p2= self.pair_time()
            temps_col=min(w_time, c_time) #la prochaine collision est le minimum entre le temps de la procahine collision murale et intra-particules
            if temps_col > temps_restant: #pas de collision sur le temps restant
                self.position += temps_restant*self.velocity
                break 
            else:
                self.position+= temps_col*self.velocity #on avance jusqua la prochaine collision
                temps_restant-= temps_col
                
                if w_time <= c_time: #la collision est murale
                    self.velocity[particle, direction] *= -1
                else:
                    self.update_velocity(p1, p2) #la collision est intra particule
        
        assert math.isclose(ke_start,  (self.velocity**2).sum()/2.)  
        return self.position
    
    def reverse_velocities(self): #permet lors du retournemnt temporel d'inverser les vitesses
        self.velocity*=-1 
        
   

            
        

        
        
        
        
    