## Import modules 
import random
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import norm
## Do not need random and pygame twice
import random, pygame, sys
from pygame.locals import *

number_of_particles = 150
my_particles = []
background_colour = (255,255,255)
width, height = 1400, 600
sigma = 1
e = 1
dt = 0.1
v = 0
a = 0
r = 1
smallPSize = 15

def r(p1,p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    angle = 0.5 * math.pi - math.atan2(dy, dx)
    dist = np.hypot(dx, dy)
    return dist

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = np.hypot(dx, dy)
    if dist < (p1.size + p2.size):
        tangent = math.atan2(dy, dx)
        angle = 0.5 * np.pi + tangent

        angle1 = 2*tangent - p1.angle
        angle2 = 2*tangent - p2.angle
        speed1 = p2.speed
        speed2 = p1.speed
        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)

        overlap = 0.5*(p1.size + p2.size - dist+1)
        p1.x += np.sin(angle) * overlap
        p1.y -= np.cos(angle) * overlap
        p2.x -= np.sin(angle) * overlap
        p2.y += np.cos(angle) * overlap


## Check to see if initial position of small particles overlaps with big particles
def initializeParticles(macroP):

    
    for n in range(number_of_particles):
        x = random.randint(smallPSize, width-smallPSize)
        y = random.randint(smallPSize, height-smallPSize)

        dx = x - macroP.x
        dy = y - macroP.y

        dist = np.hypot(dx, dy)
        
        while dist < (smallPSize+ macroP.size):
            x = random.randint(smallPSize, width-smallPSize)
            y = random.randint(smallPSize, height-smallPSize)

            dx = x - macroP.x
            dy = y - macroP.y

            dist = np.hypot(dx, dy)

        coords = [x,y]           

        particle = Particle(coords, smallPSize)           
        particle.speed = random.random()
        # np.random.uniform(a,b) choose point between a and b from uniform distribution
        particle.angle = random.uniform(0, np.pi*2)

        my_particles.append(particle)
    

def drawNumSteps(n):
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Numbers of steps: '+str(n), True, (0,0,0))

class macroParticle():
    def __init__(self, coord, size, step):
        self.x = coord[0]
        self.y = coord[1]
        self.size = size
        self.colour = (255, 0, 0)
        self.thickness = 1
        self.speed = 0
        self.angle = 0
        self.step = step

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size)

    def displayGhost(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, 3)
        
    def move(self):
        self.x += self.step
        self.y -= 0

    def getPosition(self):
        return self.x, self.y

    def bounce(self):
        if self.x > width+self.size:
            self.x = -self.size
            self.angle = - self.angle

        elif self.x < -self.size:
            self.x = width+self.size
            self.angle = - self.angle

        if self.y > height+self.size:
            self.y = -self.size
            self.angle = np.pi - self.angle

        elif self.y < -self.size:
            self.y = height+self.size
            self.angle = np.pi - self.angle

    
class Particle():
    def __init__(self, coord, size,T):
        self.x = coord[0]
        self.y = coord[1]
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 1
        self.speed = 0
        self.angle = 0
        self.step = 5
        self.T = 10

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size)

    def move(self):
        angle = random.randint(0,360)
        self.x += norm.rvs(scale=self.T)*np.sin(self.angle)
        self.y -= norm.rvs(self.T)*np.cos(self.angle)
    def bounce(self):
        if self.x > width+self.size:
            self.x = -self.size
            self.angle = self.angle

        elif self.x < -self.size:
            self.x = width+self.size
            self.angle = self.angle

        if self.y > height+self.size:
            self.y = -self.size
            self.angle = self.angle

        elif self.y < -self.size:
            self.y = height+self.size
            self.angle = self.angle

def bestFit(x,y):
    Ex = sum(x)/len(x)
    Ey = sum(y)/len(y)
    
    xx = x**2
    
    Exx = sum(xx)/len(x)
    Exy = np.dot(x,y)/len(y)
    
    m = (Exy-Ex*Ey)/(Exx-Ex**2)
    b = (Exx*Ey-Ex*Exy)/(Exx-Ex**2)
    
    return m, b

def runAnimation(MPRadius, MPX,MPY, NumSteps,speed):
        
    global screen, my_particles

    my_particles = []
    
    screen = pygame.display.set_mode((width, height))

    ## Set starting parameters for MacroParticle
    # Radius
    R = MPRadius
    # X position
    mPx = MPX

    # Y position
    mPy = MPY

    #Number of time steps
    N = NumSteps

    # Vectors for positions of interacting particle
    X = np.zeros(N)
    Y = np.zeros(N)
    distance = np.zeros(N)

    # Vectors for positions of ghost particle
    ghostX = np.zeros(N)
    ghostY = np.zeros(N)
    ghostDistance = np.zeros(N)
    
    macroP = macroParticle([mPx,mPy],R,speed)
    ghostMacroP = macroParticle([mPx,mPy],R,speed)
    pygame.init()

    ## Initialize positions for smaller particles
    initializeParticles(macroP)
    
    ## Initial number of steps
    n = 0 

    ## Initial displacements
    x0 = mPx
    y0 = mPy
    r0 = np.sqrt((mPx)**2+(mPy**2))

    while n<N:
        
        x,y = macroP.getPosition()
        gX,gY = ghostMacroP.getPosition()
        X[n] = x - x0
        Y[n] = y - y0
        distance[n] = np.sqrt(x**2+y**2)-r0
        
        ghostX[n] = gX - x0
        ghostY[n] = gY - y0
        ghostDistance[n] = np.sqrt(gX**2+gY**2)-r0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(background_colour)

        for i, particle in enumerate(my_particles):
            particle.move()
            particle.bounce()
            collide(particle, macroP)
            
            for particle2 in my_particles[i+1:]:
                collide(particle, particle2)
            particle.display()
        macroP.move()
        ghostMacroP.move()
        macroP.display()
        ghostMacroP.displayGhost()
        pygame.display.flip()
        drawNumSteps(n)
        # Increase number of steps by one
        n+=1
        
    pygame.quit()
    return X,ghostX

def plotData(MPRadius, MPVelocity, NumSteps, mpVelocity):

    for i in range(1,10):
        ## Set starting parameters for MacroParticle
        # Radius
        R = MPRadius
        # X position
        mPx = 2*R
        # Y position
        mPy = height//2
        
        #Number of time steps
        N = NumSteps

        MPV = i

        macroP = macroParticle([mPx,mPy],R,MPV)
        ghostMacroP = macroParticle([mPx,mPy],R,MPV)
        
        pygame.init()

        ## Initialize positions for smaller particles
        initializeParticles(macroP)
        
        ## Initial number of steps
        n = 0 

        ## Initial displacements
        x0 = mPx
        y0 = mPy
        r0 = np.sqrt((mPx)**2+(mPy**2))
        
        # Vectors for positions of interacting particle
        X = np.zeros(N)
        Y = np.zeros(N)
        distance = np.zeros(N)

        # Vectors for positions of ghost particle
        ghostX = np.zeros(N)
        ghostY = np.zeros(N)
        ghostDistance = np.zeros(N)

        while n<N:
        
            x,y = macroP.getPosition()
            gX,gY = ghostMacroP.getPosition()
            X[n] = x - x0
            Y[n] = y - y0
            distance[n] = np.sqrt(x**2+y**2)-r0
            
            ghostX[n] = gX - x0
            ghostY[n] = gY - y0
            ghostDistance[n] = np.sqrt(gX**2+gY**2)-r0
            macroP.move()
            ghostMacroP.move()

            for i, particle in enumerate(my_particles):
                particle.move()
                particle.bounce()
                collideMP(particle, macroP)
                
                for particle2 in my_particles[i+1:]:
                    collide(particle, particle2)

            macroP.bounce()
            # Increase number of steps by one
            n+=1

        steps = np.arange(N)
        plt.figure()
        plt.plot(steps,X,'r')
        plt.plot(steps,ghostX,'b')
        plt.ylabel(r"$x$ displacement")
        plt.xlabel(r"Number of steps")
        plt.title("Horizantal displacement after " + str(N) + " steps")
        plt.show()
        
            
def main():

    MPRadius = 100
    MPVelocity = 1
    NumSteps = 300
    mpVelocity = 10

    MPX = 2*MPRadius
    MPY = height//2

    plt.figure()

    steps = np.arange(NumSteps)

# Modulate speeeds 
    speeds = np.arange(14)
    slopes = np.zeros(14)
    i=0
    for speed in speeds:
        x,gX = runAnimation(MPRadius,MPX,MPY, NumSteps,speed)
        plt.plot(steps,x)
        m, b = bestFit(steps,x)
        slopes[i] = m
        i+=1
        
    plt.show()

    plt.figure()
    plt.ylabel(r"$Measured velocity (v)$")
    plt.xlabel(r"Characteristic velocity (v)")
    plt.title("Macroparticle velocity as a function of characteristic momentum")
    plt.scatter(speeds,slopes)
    plt.show()
    plt.savefig('Brownian-momentum-Dependence.png')

# Modulate radius
    radii = np.arange(1,15)*15
    slopes = np.zeros(14)
    i=0
    for radius in radii:
        x,gX = runAnimation(radius,MPX,MPY, NumSteps,mpVelocity)
        plt.plot(steps,x)
        m, b = bestFit(steps,x)
        slopes[i] = m
        i+=1
        
    plt.show()

    plt.figure()
    plt.scatter(radii,slopes)
    plt.ylabel(r"$Velocity (v)$")
    plt.xlabel(r"Macro-Particle Radius")
    plt.title("Macro-Particle velocity as a function of radius")
    plt.show()
    plt.savefig('Brownian-Radius-Dependence.png')
    
    
if __name__=="__main__":
    main()
