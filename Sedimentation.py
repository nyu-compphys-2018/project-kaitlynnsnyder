## Import modules 
import random
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import norm
## Do not need random and pygame twice
import random, pygame, sys
from pygame.locals import *
import time

number_of_particles = 500

numParticles = number_of_particles
my_particles = []
background_colour = (255,255,255)
width, height = 600, 600
sigma = 1
e = 1
dt = 0.1
v = 0
a = 0
r = 1
smallPSize = 6
smallPStep = 2

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

    random.seed(539)
    
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
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), int(self.size))

    def displayGhost(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), int(self.size), 3)
        
    def move(self):
        self.x += 0
        self.y += self.step

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
    def __init__(self, coord, size):
        self.x = coord[0]
        self.y = coord[1]
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 1
        self.speed = 0
        self.angle = 0
        self.step = smallPStep

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size)

    def move(self):
        self.x += self.step*np.sin(self.angle)
        self.y -= self.step*np.cos(self.angle)

    def brownian(self):
        self.x += norm.rvs(scale=self.step)
        self.y -= norm.rvs(scale=self.step)

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

def bestFit(x,y):
    Ex = sum(x)/len(x)
    Ey = sum(y)/len(y)
    
    xx = x**2
    
    Exx = sum(xx)/len(x)
    Exy = np.dot(x,y)/len(y)
    
    m = (Exy-Ex*Ey)/(Exx-Ex**2)
    b = (Exx*Ey-Ex*Exy)/(Exx-Ex**2)
    
    return m, b

def plotDisplacement(X):

    steps = np.arange(len(X))
    plt.figure()
    plt.plot(steps,X)
    plt.ylabel(r"$x$ displacement")
    plt.xlabel(r"Number of steps")
    plt.title("Horizantal displacement after " + str(NumSteps) + " steps in ballistic particles")
    plt.show()


def drawNumSteps(n):
    titleFont = pygame.font.Font('freesansbold.ttf', 20)
    stepsSurf = titleFont.render('Numbers of time steps: '+str(n), False, (0,0,0))
    stepsRect = stepsSurf.get_rect()
    stepsRect.topleft = (width - 300, 10)
    screen.blit(stepsSurf, stepsRect)


    
def runTimesSquare(MPRadius, MPX,MPY, NumSteps,speed):
        
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

    R1 = R/2
    R3 = int(1.5*R)

    macroP1 = macroParticle([3*R1,mPy],R1,speed)

    macroP2 = macroParticle([width//2-R,mPy],R,speed)
    
    macroP3 = macroParticle([width-R3-2*R1,mPy],R3,speed)
    
    pygame.init()

    ## Initialize positions for smaller particles
    initializeParticles(macroP3)
    
    ## Initial number of steps
    n = 0 


    while n<N:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        screen.fill(background_colour)
        macroP1.move()
        macroP2.move()
        macroP3.move()
        
        for i, particle in enumerate(my_particles):
            particle.move()
            particle.bounce()
            collide(particle, macroP1)
            collide(particle, macroP2)
            collide(particle, macroP3)
            
            for particle2 in my_particles[i+1:]:
                collide(particle, particle2)
            particle.display()

        macroP1.display()
        macroP2.display()
        macroP3.display()

        drawNumSteps(n)
        # Increase number of steps by one
        n+=1

        pygame.display.flip()
        
    pygame.quit()

def fitDrag():
    MPRadius = 150
    MPVelocity = 1
    NumSteps = 100
    mpVelocity = 5

    MPX = 2*MPRadius
    MPY = height//2

    steps = np.arange(NumSteps)

    speeds = np.arange(250)

    slopes = []

    for speed in speeds:
    
        X,gX=runTimesSquare(MPRadius,MPX,MPY, NumSteps,speed)

        m,b = bestFit(steps,X)

        print(m)

        slopes.append(m)

    

    plt.figure()
    plt.plot(np.arange(len(slopes)),slopes)
    plt.title("Speed vs. applied force on MP of radius " + str(MPRadius) + " in a sea of " + str(numParticles) +" particles with characteristic speed " + str(smallPStep))
    plt.xlabel("Step size of macro-particle (pixels)")
    plt.ylabel("Horizantal velocity of macro-particle (pixel per time step)")
    plt.show()

def scalingWNumParticles():

    global number_of_particles
    particles = np.arange(1,10)*50

    times = np.zeros(len(particles))

    i = 0

    MPRadius = 150
    MPVelocity = 3
    NumSteps = 100

    MPX = 2*MPRadius
    MPY = height//2

    for n in particles:

        number_of_particles = n

        start = time.time()
        runTimesSquare(MPRadius,MPX,MPY, NumSteps,MPVelocity)
        end = time.time()

        times[i] = end - start

        i += 1

    m1,  b1 = bestFit(np.log(particles),np.log(times))

    fit = m1*np.log(particles)+b1
                             
    plt.figure()
    plt.scatter(np.log(particles),np.log(times))
    plt.plot(np.log(particles),fit)
    plt.xlabel("Number of particles")
    plt.ylabel("Run time")
    plt.title("Run time scaling with number of particles")
    plt.show()

    print(m1)
            
def main():

    MPRadius = 50
    MPVelocity = 3
    NumSteps = 300

    MPX = 2*MPRadius
    MPY = 2*MPRadius


 #   scalingWNumParticles()
    runTimesSquare(MPRadius,MPX,MPY, NumSteps,MPVelocity)
    
    
if __name__=="__main__":
    main()
