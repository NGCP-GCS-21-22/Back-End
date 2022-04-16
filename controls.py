#import necessary libraries
from utilities import *

#to make the json file look more manageable, do Shift+Alt+F

if __name__ == '__main__':
    #Initialize_Variables()
    pygame.init() #initialize pygame
    pygame.display.set_mode(((4,4)))
    mode = True
    manual = True
    running = True
    Initialize_Controller() #set controller buttons
    while running: #while loop to take inputs 
        Inputs(mode, manual, running) #call inputs method