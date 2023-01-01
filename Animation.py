from random import random as r
from vpython import *
import math



class Particle(sphere):
    def __init__(self, pos, vel, col, rad, mass):
        super(self.__class__, self).__init__(
            pos=pos,
            radius=rad,
            color=col
        )
        self.vel = vel
        self.mass = mass


class Dust(sphere):
    def __init__(self, pos, vel, col, rad, mass):
        super(self.__class__, self).__init__(
            pos=pos,
            radius=rad,
            color=col,
            make_trail=True
        )
        self.vel = vel
        self.mass = mass


def make_molecules(n_molecules, radius, mass):
    molecules = [Dust(
        pos=vector(0, 0, 0),
        vel=vector(0, 0, 0),
        col=color.blue,
        rad=0.05,
        mass=1
    )]
    for i in range(n_molecules):
        molecules.append(Particle(
            pos=vector(r() - 0.5, r() - 0.5, r() - 0.5),
            vel=vector(r() - 0.5, r() - 0.5, r() - 0.5),
            col=color.red,
            rad=radius,
            mass=mass
            ))
    return molecules


# Stable (no oscillating velocity) because return to inside bounding box

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
       
        if mag(p.pos - m.pos) <= p.radius + m.radius:
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


oscillation1 = graph(width = 450,xtitle='t',ytitle='displacement', align = 'right')
funct1 = gcurve(graph = oscillation1, color=color.blue, width=4)
oscillation2 = graph(width = 450,xtitle='t',ytitle='kinetic energy', align = 'right')
funct2 = gcurve(graph = oscillation2, color=color.red, width=4)

def main():
    container = box(pos=vector(0, 0, 0),
                    size=vector(1, 1, 1),
                    color=color.white,
                    opacity=0.1)
    floor = box(pos = vec(0, -0.53, 0), length=1, height=0.005, width=1, color=color.orange)

    # Generate list of 1 dust particle and 100 random small particles
    molecules = make_molecules(n_molecules=100, radius=0.01, mass=0.01)

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
