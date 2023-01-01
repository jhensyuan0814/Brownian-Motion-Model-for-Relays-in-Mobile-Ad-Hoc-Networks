from random import random as r
from vpython import *
import math
import copy

class obj:
    pass

class Dust:
    def __init__(self,pos,vel,rad,mass):
        self.pos = pos
        self.vel = vel
        self.rad = rad
        self.mass = mass

class Particle:
    def __init__(self,pos,vel,rad,mass):
        self.pos = pos
        self.vel = vel
        self.rad = rad
        self.mass = mass
    

class many_molecules:
    def __init__(self,n_molecules, radius, mass):
        self.num = []
        self.num.append(Dust(vector(0, 0, 0),vector(0, 0, 0),0.05,1))
        for i in range(n_molecules):
            self.num.append(Particle(vector(r() - 0.5, r() - 0.5, r() - 0.5),vector(r() - 0.5, r() - 0.5, r() - 0.5),radius,mass))



# Stable (no oscillating velocity) because return to inside bounding box
# is guaranteed
def calc_wall_collision(particle):
    box_bounds = 0.5
    if abs(particle.pos.x) >= box_bounds:
        particle.vel.x *= -1
    if abs(particle.pos.y) >= box_bounds:
        particle.vel.y *= -1
    if abs(particle.pos.z) >= box_bounds:
        particle.vel.z *= -1
    
    
def calc_part_collision(p, molecules):
    for m in molecules:
        # Avoid collision with itself
      
        if p is m:
            continue

        # If collision detected, perform elastic momentum transfer
        # (Python simultaneous assignment ftw!)
        if mag(p.pos - m.pos) <= p.rad + m.rad:
            # If masses are equal, velocities are swapped
            if abs(p.mass - m.mass) < 1e-3:
                p.vel, m.vel = m.vel, p.vel
            else:
                p.vel, m.vel = \
                    (p.vel * (p.mass - m.mass) + 2 * m.mass * m.vel) / (p.mass + m.mass), \
                    (m.vel * (m.mass - p.mass) + 2 * p.mass * p.vel) / (p.mass + m.mass)
            # Process only one collision per frame
            break


def update_velocity(molecules, dt):
    for m in molecules:
        calc_wall_collision(m)
        
    calc_part_collision(molecules[0], molecules)
    

def update_position(molecules, dt):
    for m in molecules:
        m.pos += m.vel * dt
        


oscillation1 = graph(width = 450, align = 'right')
funct1 = gcurve(graph = oscillation1, color=color.blue, width=4)
oscillation2 = graph(width = 450,xtitle='t',ytitle='kinetic energy', align = 'right')
funct2 = gcurve(graph = oscillation2, color=color.red, width=4)

def main():

    # Generate list of 1 dust particle and 100 random small particles
    molecules = many_molecules(n_molecules=100, radius=0.01, mass=0.01).num
    
    t=0
    dt = 0.05

    while 1:
        rate(60)
        update_velocity(molecules, dt)
        update_position(molecules, dt)

        displacement = math.sqrt((molecules[0].pos.x)**2+(molecules[0].pos.y)**2+(molecules[0].pos.z)**2)
        kE = 0.5*1*(molecules[0].vel.x**2+molecules[0].vel.y**2+molecules[0].vel.z**2)
        funct1.plot(pos=(t, displacement))
        funct2.plot(pos=(t, kE))
        t+=dt
        
if __name__ == '__main__':
    main()
