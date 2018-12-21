## Import modules 
import random
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import norm
## Do not need random and pygame twice
import random, pygame, sys
from pygame.locals import *

number_of_particles = 200
my_particles = []
background_colour = (255,255,255)
width, height = 1000, 600
sigma = 1
e = 1
dt = 0.1
v = 0
a = 0
r = 1
smallPSize = 10

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

def collideMass(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = np.hypot(dx, dy)
    if dist < (p1.size + p2.size):
        tangent = math.atan2(dy, dx)
        angle = 0.5 * np.pi + tangent

        angle1 = -2*tangent + p1.angle
        angle2 = -2*tangent + p2.angle
        speed1 = (p1.speed*(p1.mass-p2.mass)+2*p2.mass*p2.speed)/(p1.mass+p2.mass)
        speed2 = abs((p2.speed*(p2.mass-p1.mass))+2*p1.mass*p1.speed)/(p1.mass+p2.mass)
        (p1.angle, p1.step) = (angle1, speed1)
        (p2.angle, p2.step) = (angle2, speed2)

        
        overlap = 0.5*(p1.size + p2.size - dist+1)
        p1.x += np.sin(angle) * overlap
        p1.y -= np.cos(angle) * overlap
        p2.x -= np.sin(angle) * overlap
        p2.y += np.cos(angle) * overlap

## Check to see if initial position of small particles overlaps with big particles
def initializeParticles(macroP):

    random.seed(317)
    
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
    

def drawNumSteps(n,r):
    titleFont = pygame.font.Font('freesansbold.ttf', 20)
    stepsSurf = titleFont.render('Numbers of time steps: '+str(n), False, (0,0,0))
    stepsRect = stepsSurf.get_rect()
    stepsRect.topleft = (width - 400, 10)
    screen.blit(stepsSurf, stepsRect)

    stepsSurf = titleFont.render('Displacement from center: '+str(int(r))+ ' pixels', False, (0,0,0))
    stepsRect = stepsSurf.get_rect()
    stepsRect.topleft = (width - 400, 50)
    screen.blit(stepsSurf, stepsRect)
    
class slider():

    def __init__(self,coord, parameter):
        self.x = coord[0]
        self.y = coord[1]
        self.width = 100
        self.height = 10
        self.barColor = (0,0,0)
        self.circleColor = (200,200,0)
        self.centerX = self.x + self.width//2
        self.centerY = self.y + self.height//2
        self.radius = 12
        self.parameter = parameter

        self.value = (self.centerX - self.x)


    def drawSlider(self):

        titleFont = pygame.font.Font('freesansbold.ttf', 18)
        stepsSurf = titleFont.render(self.parameter, False, (0,0,0))
        stepsRect = stepsSurf.get_rect()
        stepsRect.topleft = (self.x,self.y - 25)
        screen.blit(stepsSurf, stepsRect)
        
        pygame.draw.rect(screen,self.barColor,[self.x,self.y,self.width,self.height])
        pygame.draw.circle(screen,self.circleColor,(self.centerX,self.centerY),self.radius)

        button = pygame.mouse.get_pressed()
        
        if button[0] != 0:
           pos = pygame.mouse.get_pos()
           x = pos[0]
           y = pos[1]
           
           if x > self.centerX and x < (self.width+self.x+self.radius) and y < self.y+2*self.radius and y > self.y-2*self.radius:
              self.centerX +=1
              if x >= (self.width+self.x):
                  self.centerX = (self.width+self.x)

           elif x < self.centerX and x > (self.x-self.radius) and y < self.y+2*self.radius and y > self.y-2*self.radius:
              self.centerX -=1
              if x <= self.width:
                  self.centerX = self.x

           self.value = (self.centerX - self.x)


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
        self.mass = 1

        self.path = [[self.x,self.y]]

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size)

    def displayGhost(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, 3)

    def drawPath(self):

        for i in range(len(self.path)-1):
            pygame.draw.line(screen, self.colour, self.path[i],self.path[i+1],3)
            
    def glide(self):
        self.x += self.step
        self.y -= 0

    def move(self):
        self.x += self.step*np.sin(self.angle)
        self.y -= self.step*np.cos(self.angle)
        
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
        self.size = smallPSize
        self.colour = (0, 0, 255)
        self.thickness = 1
        self.speed = 0
        self.angle = 0
        self.step = 5
        self.T = 5
        self.mass = 1

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

def runTimesSquare(MPRadius,speed):
        
    global screen, my_particles

    my_particles = []
    
    screen = pygame.display.set_mode((width, height))

    ## Set starting parameters for MacroParticle
    # Radius
    R = MPRadius
    # X position
    mPx = width//2
    # Y position
    mPy = height//2

    s1 = slider([50,50],"Velocity")

    s2 = slider([50,100],"Size")
    
    macroP = macroParticle([mPx,mPy],R,speed)
    pygame.init()

    ## Initialize positions for smaller particles
    initializeParticles(macroP)    

    n = 0

    running = True

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(background_colour)
        
        for i, particle in enumerate(my_particles):
            particle.move()
            particle.bounce()
            collide(particle, macroP)

            particle.step = s1.value//10
            particle.size = int(s2.value/5)
            
            for particle2 in my_particles[i+1:]:
                collide(particle, particle2)
            particle.display()

    ## Get new macro-particle coordinates
        x,y = macroP.getPosition()

        macroP.path.append([int(x),int(y)])
        r = np.sqrt((x-mPx)**2+(y-mPy)**2)

        macroP.drawPath()
        macroP.bounce()
        macroP.display()
        drawNumSteps(n,r)
        s1.drawSlider()
        s2.drawSlider()
        pygame.display.flip()
        
        n += 1
        
    pygame.quit()

    
def runBrownian(MPRadius,speed):
        
    global screen, my_particles

    my_particles = []
    
    screen = pygame.display.set_mode((width, height))

    ## Set starting parameters for MacroParticle
    # Radius
    R = MPRadius
    # X position
    mPx = width//2
    # Y position
    mPy = height//2

    s1 = slider([50,50],"Velocity")

    s2 = slider([50,100],"Size")
    
    macroP = macroParticle([mPx,mPy],R,speed)
    pygame.init()

    ## Initialize positions for smaller particles
    initializeParticles(macroP)    

    n = 0

    running = True

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(background_colour)
        
        for i, particle in enumerate(my_particles):
            particle.brownian()
            particle.bounce()
            collide(particle, macroP)

            particle.step = s1.value//10
            particle.size = int(s2.value/5)
            
            for particle2 in my_particles[i+1:]:
                collide(particle, particle2)
            particle.display()

    ## Get new macro-particle coordinates
        x,y = macroP.getPosition()

        macroP.path.append([int(x),int(y)])
        r = np.sqrt((x-mPx)**2+(y-mPy)**2)

        macroP.drawPath()
        macroP.bounce()
        macroP.display()
        drawNumSteps(n,r)
        s1.drawSlider()
        s2.drawSlider()
        pygame.display.flip()
        
        n += 1
        
    pygame.quit()

def showStartScreen():
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    FPSCLOCK=pygame.time.Clock()
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Particle Collider!', True, (200,0,0))

    surface  = pygame.Surface((100,500))
    surface.set_colorkey((0,0,0))

    ellipse = pygame.draw.ellipse(surface, (255,0,0), (0,0,100,500))

    degrees1 = 0
    degrees2 = 0

    run = True

    while True:
        screen.fill((255,255,255))
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (width / 2, height / 2)
        screen.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(surface, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (width / 2, height / 2)
        screen.blit(rotatedSurf2, (10,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        pygame.display.update()
        FPSCLOCK.tick(12)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame

def runElastic(MPRadius,speed):
        
    global screen, my_particles

    my_particles = []
    
    screen = pygame.display.set_mode((width, height))

    ## Set starting parameters for MacroParticle
    # Radius
    R = MPRadius
    # X position
    mPx = width//2
    # Y position
    mPy = height//2

    s1 = slider([50,50],"Velocity")

    s2 = slider([50,100],"Size")
    
    macroP = macroParticle([mPx,mPy],R,speed)
    pygame.init()

    ## Initialize positions for smaller particles
    initializeParticles(macroP)    

    n = 0

    running = True

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(background_colour)
        
        for i, particle in enumerate(my_particles):
            particle.move()
            particle.bounce()
            collideMass(particle, macroP)

            particle.step = s1.value//10
            particle.size = int(s2.value/5)+2
            
            for particle2 in my_particles[i+1:]:
                collideMass(particle, particle2)
            particle.display()

    ## Get new macro-particle coordinates
        x,y = macroP.getPosition()

        macroP.path.append([int(x),int(y)])
        r = np.sqrt((x-mPx)**2+(y-mPy)**2)

        macroP.drawPath()
        macroP.bounce()
        macroP.move()
        macroP.display()
        drawNumSteps(n,r)
        s1.drawSlider()
        s2.drawSlider()
        pygame.display.flip()
        
        n += 1
        
    pygame.quit()

def main():

    MPRadius = 25
    MPVelocity = 1
    NumSteps = 300
    mpVelocity = 5

    MPX = 2*MPRadius
    MPY = height//2

    steps = np.arange(NumSteps)

    speed = 0

 #   showStartScreen()
    runElastic(MPRadius,speed)
    
if __name__=="__main__":
    main()
