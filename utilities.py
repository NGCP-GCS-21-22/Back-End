#import necessary libraries
#import pygame
#from pygame.locals import *
import os
#import setproctitle
import multiprocessing
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double
#from process import Process
from pygame.locals import *

class Controller():

    def run_controller(mode, controller_data):
        import pygame

        # Define some colors
        BLACK    = (   0,   0,   0)
        WHITE    = ( 255, 255, 255)

        # This is a simple class that will help us print to the screen
        # It has nothing to do with the joysticks, just outputing the
        # information.
        class TextPrint:
            def __init__(self):
                self.reset()
                self.font = pygame.font.Font(None, 20)

            def print(self, screen, textString):
                textBitmap = self.font.render(textString, True, BLACK)
                screen.blit(textBitmap, [self.x, self.y])
                self.y += self.line_height
                
            def reset(self):
                self.x = 10
                self.y = 10
                self.line_height = 15
                
            def indent(self):
                self.x += 10
                
            def unindent(self):
                self.x -= 10

        pygame.init() #initialize pygame
        size = [200, 150]
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Controller")

        clock = pygame.time.Clock()
        textPrint = TextPrint()

        #definition to instantiate variables in a json format
        data = {}
        data['Controls'] = []
        data['Controls'].append({
            'UP' : 0,
            'DOWN' : 0,
            'LEFT' : 0,
            'RIGHT' : 0,
            'X/ARROW_DOWN' : 0,
            'CIRCLE/ARROW_RIGHT' : 0,
            'SQUARE/ARROW_LEFT' : 0,
            'TRIANGLE/ARROW_UP' : 0,
            'L1/1' : 0,
            'R1/2' : 0,
            'L2/3' : 0,
            'R2/4' : 0,
            'L3/5' : 0,
            'R3/6' : 0,
            'SHARE/7' : 0,
            'PS/8' : 0,
            'OPTIONS/9' : 0,
            'UP/DOWN': 0,
            'LEFT/RIGHT': 0
        })

        global button_keys, analog_keys, joysticks #set global variables
        joysticks = []
        for i in range(pygame.joystick.get_count()):
            joysticks.append(pygame.joystick.Joystick(i))
        for joystick in joysticks:
            joystick.init()

        #Represents one click buttons
        button_keys = {"x": 0, "circle": 1, "square": 2, "triangle": 3, "share": 4, "PS": 5, "options": 6, "left_stick_click": 7, 
            "right_stick_click": 8, "L1": 9, "R1": 10, "up_arrow": 11, "down_arrow": 12, "left_arrow": 13, "right_arrow": 14, "touchpad": 15}
        #Represents analog keys joysticks, L2, R2, L3, R3
        analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }

        while True:
            screen.fill(WHITE)
            textPrint.reset()
            for event in pygame.event.get():
                #check for mode
                #if mode is keyboard
                if mode == True:
                    #handle keyboard press
                    if event.type == KEYDOWN:
                        if event.key == K_w:
                            data['Controls'][0]['UP'] = 1
                        if event.key == K_s:
                            data['Controls'][0]['DOWN'] = 1 
                        if event.key == K_a:
                            data['Controls'][0]['LEFT'] = 1 
                        if event.key == K_d:
                            data['Controls'][0]['RIGHT'] = 1 
                        if event.key == K_DOWN:
                            data['Controls'][0]['X/ARROW_DOWN'] = 1
                        if event.key == K_RIGHT:
                            data['Controls'][0]['CIRCLE/ARROW_RIGHT'] = 1 
                        if event.key == K_LEFT:
                            data['Controls'][0]['SQUARE/ARROW_LEFT'] = 1 
                        if event.key == K_UP:
                            data['Controls'][0]['TRIANGLE/ARROW_UP'] = 1 
                        if event.key == K_1:
                            data['Controls'][0]['L1/1'] = 1
                        if event.key == K_2:
                            data['Controls'][0]['R1/2'] = 1 
                        if event.key == K_3:
                            data['Controls'][0]['L2/3'] = 1 
                        if event.key == K_4:
                            data['Controls'][0]['R2/4'] = 1 
                        if event.key == K_5:
                            data['Controls'][0]['L3/5'] = 1 
                        if event.key == K_6:
                            data['Controls'][0]['R3/6'] = 1 
                        if event.key == K_7:
                            data['Controls'][0]['SHARE/7'] = 1
                        if event.key == K_8:
                            data['Controls'][0]['PS/8'] = 1 
                        if event.key == K_9:
                            data['Controls'][0]['OPTIONS/9'] = 1 
                        #to quit manual control
                        if event.key == K_q:
                            running = False
                            manual = False
                        #to switch to controller input
                        if event.key == K_c:
                            mode = False
                    #handle keyboard release set values equal to 0
                    elif event.type == KEYUP:
                        if event.key == K_w:
                            data['Controls'][0]['UP'] = 0    
                        if event.key == K_s:
                            data['Controls'][0]['DOWN'] = 0 
                        if event.key == K_a:
                            data['Controls'][0]['LEFT'] = 0 
                        if event.key == K_d:
                            data['Controls'][0]['RIGHT'] = 0
                        if event.key == K_DOWN:
                            data['Controls'][0]['X/ARROW_DOWN'] = 0
                        if event.key == K_RIGHT:
                            data['Controls'][0]['CIRCLE/ARROW_RIGHT'] = 0
                        if event.key == K_LEFT:
                            data['Controls'][0]['SQUARE/ARROW_LEFT'] = 0
                        if event.key == K_UP:
                            data['Controls'][0]['TRIANGLE/ARROW_UP'] = 0
                        if event.key == K_1:
                            data['Controls'][0]['L1/1'] = 0
                        if event.key == K_2:
                            data['Controls'][0]['R1/2'] = 0
                        if event.key == K_3:
                            data['Controls'][0]['L2/3'] = 0
                        if event.key == K_4:
                            data['Controls'][0]['R2/4'] = 0
                        if event.key == K_5:
                            data['Controls'][0]['L3/5'] = 0
                        if event.key == K_6:
                            data['Controls'][0]['R3/6'] = 0
                        if event.key == K_7:
                            data['Controls'][0]['SHARE/7'] = 0
                        if event.key == K_8:
                            data['Controls'][0]['PS/8'] = 0
                        if event.key == K_9:
                            data['Controls'][0]['OPTIONS/9'] = 0
    
                #else mode is controller
                else:
                    #handle controller press
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == button_keys['up_arrow']:
                            data['Controls'][0]['UP'] = 1
                        if event.button == button_keys['down_arrow']:
                            data['Controls'][0]['DOWN'] = 1
                        if event.button == button_keys['left_arrow']:
                            data['Controls'][0]['LEFT'] = 1
                        if event.button == button_keys['right_arrow']:
                            data['Controls'][0]['RIGHT'] = 1
                        if event.button == button_keys['x']:
                            data['Controls'][0]['X/ARROW_DOWN'] = 1
                        if event.button == button_keys['circle']:
                            data['Controls'][0]['CIRCLE/ARROW_RIGHT'] = 1
                        if event.button == button_keys['square']:
                            data['Controls'][0]['SQUARE/ARROW_LEFT'] = 1
                        if event.button == button_keys['triangle']:
                            data['Controls'][0]['TRIANGLE/ARROW_UP'] = 1
                        if event.button == button_keys['L1']:
                            data['Controls'][0]['L1/1'] = 1
                        if event.button == button_keys['R1']:
                            data['Controls'][0]['R1/2'] = 1
                        if event.button == button_keys['left_stick_click']:
                            data['Controls'][0]['L1/1'] = 1
                        if event.button == button_keys['right_stick_click']:
                            data['Controls'][0]['R1/2'] = 1
                        if event.button == button_keys['share']:
                            data['Controls'][0]['L1/1'] = 1
                        if event.button == button_keys['PS']:
                            data['Controls'][0]['R1/2'] = 1
                        if event.button == button_keys['options']:
                            data['Controls'][0]['OPTIONS/9'] = 1
                        #to quit manual control
                        if event.button == button_keys['PS']:
                            running = False
                        #to switch to keyboard control
                        if event.button == button_keys['up_arrow']:
                            mode = True
                    #handle controller release set values equal to 0
                    elif event.type == pygame.JOYBUTTONUP:
                        if event.button == button_keys['up_arrow']:
                            data['Controls'][0]['UP'] = 0
                        if event.button == button_keys['down_arrow']:
                            data['Controls'][0]['DOWN'] = 0
                        if event.button == button_keys['left_arrow']:
                            data['Controls'][0]['LEFT'] = 0
                        if event.button == button_keys['right_arrow']:
                            data['Controls'][0]['RIGHT'] = 0
                        if event.button == button_keys['x']:
                            data['Controls'][0]['X/ARROW_DOWN'] = 0
                        if event.button == button_keys['circle']:
                            data['Controls'][0]['CIRCLE/ARROW_RIGHT'] = 0
                        if event.button == button_keys['square']:
                            data['Controls'][0]['SQUARE/ARROW_LEFT'] = 0
                        if event.button == button_keys['triangle']:
                            data['Controls'][0]['TRIANGLE/ARROW_UP'] = 0
                        if event.button == button_keys['L1']:
                            data['Controls'][0]['L1/1'] = 0
                        if event.button == button_keys['R1']:
                            data['Controls'][0]['R1/2'] = 0
                        if event.button == button_keys['left_stick_click']:
                            data['Controls'][0]['L1/1'] = 0
                        if event.button == button_keys['right_stick_click']:
                            data['Controls'][0]['R1/2'] = 0
                        if event.button == button_keys['share']:
                            data['Controls'][0]['L1/1'] = 0
                        if event.button == button_keys['PS']:
                            data['Controls'][0]['R1/2'] = 0
                        if event.button == button_keys['options']:
                            data['Controls'][0]['OPTIONS/9'] = 0
                    #handle controller analog
                    if event.type == pygame.JOYAXISMOTION:
                        analog_keys[event.axis] = event.value
                        if abs(analog_keys[1]) > .1:
                            data['Controls'][0]['UP/DOWN'] = analog_keys[1]
                        else:
                            data['Controls'][0]['UP/DOWN'] = 0
                        if abs(analog_keys[0]) > .1:
                            data['Controls'][0]['LEFT/RIGHT'] = analog_keys[0]
                        else:
                            data['Controls'][0]['LEFT/RIGHT'] = 0
                        if abs(analog_keys[2]) > .1:
                            data['Controls'][0]['L2/3'] = analog_keys[2]
                        else:
                            data['Controls'][0]['L2/3'] = 0
                        if abs(analog_keys[3]) > .1:
                            data['Controls'][0]['R2/4'] = analog_keys[3]
                        else:
                            data['Controls'][0]['R2/4'] = 0
                        if analog_keys[4] > 0:
                            data['Controls'][0]['L3/5'] = analog_keys[4]
                        else:
                             data['Controls'][0]['L3/5'] = 0
                        if analog_keys[5] > 0:
                            data['Controls'][0]['R3/6'] = analog_keys[5]
                        else:
                            data['Controls'][0]['R3/6'] = 0

            #================= ERU Controls ===================#
            vertical = abs(int(data['Controls'][0]['UP/DOWN']*220))
            if data['Controls'][0]['UP/DOWN'] < 0:
                vertical_direction = 0
            else:
                vertical_direction = 1
            horizontal = int((data['Controls'][0]['LEFT/RIGHT'] + 1) * 90) + 32

            armOne = int(data['Controls'][0]['L2/3'])
            armTwo = int(-data['Controls'][0]['R2/4'])
            if data['Controls'][0]['L1/1'] == 1 and data['Controls'][0]['R1/2'] == 0:
                armThree = -1
            elif data['Controls'][0]['L1/1'] == 0 and data['Controls'][0]['R1/2'] == 1:
                armThree = 1
            else:
                armThree = 0
            
            if data['Controls'][0]['L3/5'] == 1 and data['Controls'][0]['R3/6'] == 0:
                armFour = -1
                armFour_direction = 0
            elif data['Controls'][0]['L3/5'] == 0 and data['Controls'][0]['R3/6'] == 1:
                armFour = 1
                armFour_direction = 1
            else:
                armFour = 0
                armFour_direction = 0

            controller_data[0] = vertical
            controller_data[1] = horizontal
            controller_data[2] = armOne
            controller_data[3] = armTwo
            controller_data[4] = armThree
            controller_data[5] = armFour
            controller_data[6] = vertical_direction
            controller_data[7] = armFour_direction

            textPrint.print(screen, "Vertical: " + str(vertical))
            textPrint.print(screen, "Vertical direction: " + str(vertical_direction))
            textPrint.print(screen, "Horizontal: " + str(horizontal))
            textPrint.print(screen, "ArmOne: " + str(armOne))
            textPrint.print(screen, "ArmTwo: " + str(armTwo))
            textPrint.print(screen, "ArmThree: " + str(armThree))
            textPrint.print(screen, "ArmFour: " + str(armFour))
            textPrint.print(screen, "ArmFour Direction: " + str(armFour))

            pygame.display.flip()
            clock.tick(20)

        pygame.quit()