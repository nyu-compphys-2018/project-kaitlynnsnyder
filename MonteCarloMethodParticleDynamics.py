

class Particle():

    def __init__(self,coord,size,temp):

        self.x = coord[0]
        self.y = coord[1]
        self.size = size
        self.colour = (255, 0, 0)
        self.thickness = 1
        self.speed = 0
        self.angle = 0
        self.step = temp

    def potential(self):

        uX = -self.x/((self.x-width//2)**2-(self.y-height//2))**(3/2)
        uX = -self.x/((self.x-width//2)**2-(self.y-height//2))**(3/2)

        return uX, uY
        

                
                
