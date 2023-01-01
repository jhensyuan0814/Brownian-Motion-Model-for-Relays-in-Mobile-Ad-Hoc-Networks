from random import random as r
from vpython import *
import math
import copy
import matplotlib.pyplot as plt





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
    

class many_molecules:   #all molecules in one sample
    def __init__(self,n_molecules, radius, mass):
        self.num = []
        self.num.append(Dust(vector(0, 0, 0),vector(0, 0, 0),0.05,1))
        for i in range(n_molecules):
            self.num.append(Particle(vector(r() - 0.5, r() - 0.5, r() - 0.5),vector(r() - 0.5, r() - 0.5, r() - 0.5),radius,mass))

class collection:   #collection of all samples
    def __init__(self,num):
        self.samples = []
        for i in range(num):
            self.samples.append(many_molecules(n_molecules=100, radius=0.01, mass=0.01).num)
        



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
        


oscillation1 = graph(width = 600,xtitle='t',ytitle='displacement', align = 'left')
funct1 = gcurve(graph = oscillation1, color=color.black, width=1)
funct2 = gcurve(graph = oscillation1, color=color.red, width=1)
funct3 = gcurve(graph = oscillation1, color=color.green, width=1)
funct4 = gcurve(graph = oscillation1, color=color.purple, width=1)
funct5 = gcurve(graph = oscillation1, color=color.blue, width=1)
funct6 = gcurve(graph = oscillation1, color=color.orange, width=1)


oscillation2 = graph(width = 600,xtitle='t',ytitle='average displacement', align = 'right')
avg_funct = gcurve(graph = oscillation2, color=color.red, width=4)



def main():
    number = 6    # number of samples
    # each sample contains a list of 1 dust particle and 100 random small particles

    prob_collection = []
    chance = 0

    t=0
    dt = 0.05

    all_samples = copy.deepcopy(collection(number).samples)

    while 1:
        rate(60)
        count = 0
        displacement_collection = []
       
        for molecules in all_samples:
            
            count+=1
            update_velocity(molecules, dt)
            update_position(molecules, dt)
            
            displacement = math.sqrt((molecules[0].pos.x)**2+(molecules[0].pos.y)**2+(molecules[0].pos.z)**2)
            displacement_collection.append(displacement)

            if count==1:
                funct1.plot( pos=(t, displacement))

            elif count==2:
                funct2.plot( pos=(t, displacement))

            elif count==3:
                funct3.plot( pos=(t, displacement))

            elif count==4:
                funct4.plot( pos=(t, displacement))

            elif count==5:
                funct5.plot( pos=(t, displacement))

            elif count==6:
                funct6.plot( pos=(t, displacement))

            
        
        avg_displacement = float(sum(displacement_collection)/number)
        prob_collection.append(round(avg_displacement, 1))
        avg_funct.plot( pos=(t, avg_displacement))
        
        chance +=1
        t+=dt

        if t>=150:
            break

    prob_dict = {}
    for sample in prob_collection:
        if sample not in prob_dict:
            prob_dict[sample]=1
        else:
            prob_dict[sample]+=1

    all_samples = sum(prob_dict.values())
    for sample in prob_dict:
        prob_dict[sample] = float(prob_dict[sample]/all_samples)

    D = {}
    for key in prob_dict:
        D[str(key)] = prob_dict[key]    

    plt.bar(range(len(D)), list(D.values()), align='center')
    plt.xticks(range(len(D)), list(D.keys()))

    plt.show()

if __name__ == '__main__':
    main()
