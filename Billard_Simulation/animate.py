# Nom du fichier : animate.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import EllipseCollection, LineCollection
import time

class Animate:
    def __init__(self, simul):
        self.simul = simul
        
        self.fig, self.ax = plt.subplots(figsize=(6, 10))
        
        
        self.circles = EllipseCollection(widths=2*simul.sigma, 
                                         heights=2*simul.sigma, 
                                         angles=0, units='x',
                                         offsets=simul.position, 
                                         transOffset=self.ax.transData)
        self.ax.add_collection(self.circles)

        
        self.segment = [[[0, 0], [0, simul.Ly], [simul.Lx, simul.Ly], [simul.Lx, 0], [0, 0]]]
        self.line = LineCollection(self.segment, colors="#027304")
        self.ax.add_collection(self.line)
        self.ax.set_xlim(left=-2, right=self.simul.Lx+2)
        self.ax.set_ylim(bottom=-2, top=self.simul.Ly+2)
        self.ax.set_aspect('equal', adjustable='box')
        
    def init(self):
        self.circles.set_offsets(self.simul.position)
        return self.circles,

   

    def anim_step(self, m):
        if m == 0:
            time.sleep(1)
        if m == self.nframes // 2:
            
            self.simul.reverse_velocities()

        dt= 0.05
        self.simul.md_step(dt)
        
        self.circles.set_offsets(self.simul.position)
        return self.circles,

    def go(self, nframes):
        self.nframes = nframes
        self._ani = animation.FuncAnimation(self.fig, func=self.anim_step, frames=nframes,
                                            repeat=False, interval=20, init_func=self.init, blit=True)
        plt.show()