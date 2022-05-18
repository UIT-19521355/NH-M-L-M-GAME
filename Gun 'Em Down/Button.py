import pygame

class Button():
    '''This class later will be inheritaged by "PlayAgain"button, "ATKUP"button and so on ...'''
    def __init__(self, color, x,y,width,height, text=''):
        '''Fundamental infos'''
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        '''Call this method to draw the button on the screen'''
        if outline:
            pygame.draw.rect(win, (50, 50, 50), (self.x-5,self.y-5,self.width+10,self.height+10),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('roboto', 40)
            text = font.render(self.text, 1, (50,50,50))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        '''This function is used to check the position of the mouse, does it on the button or not'''
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True       
        return False
    def ChangeColor(self,color):
        '''This function is used to change color of button'''
        self.color=(255,255,255)
    