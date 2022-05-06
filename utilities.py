#import necessary libraries
import pygame
from pygame.locals import *
import json, os

'''
#definition to instantiate variables in a json format
data = {}
data['Controls'] = []
data['Controls'].append({
    'UP/DOWN' : 0,
    'LEFT/RIGHT' : 0,
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
    'OPTIONS/9' : 0
})
'''

#definition to initialize the controller
def Initialize_Controller():
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

#defintion for inputs
def Inputs(mode, manual, running, data):
    global button_keys, analog_keys #set global variables
    for event in pygame.event.get():
        #check for mode
        #if mode is keyboard
        if mode == True:
            #handle keyboard press
            if event.type == KEYDOWN:
                if event.key == K_w:
                    data['Controls']['UP'] = 1
                if event.key == K_s:
                    data['Controls']['DOWN'] = 1 
                if event.key == K_a:
                    data['Controls']['LEFT'] = 1 
                if event.key == K_d:
                    data['Controls']['RIGHT'] = 1 
                if event.key == K_DOWN:
                    data['Controls']['X/ARROW_DOWN'] = 1
                if event.key == K_RIGHT:
                    data['Controls']['CIRCLE/ARROW_RIGHT'] = 1 
                if event.key == K_LEFT:
                    data['Controls']['SQUARE/ARROW_LEFT'] = 1 
                if event.key == K_UP:
                    data['Controls']['TRIANGLE/ARROW_UP'] = 1 
                if event.key == K_1:
                    data['Controls']['L1/1'] = 1
                if event.key == K_2:
                    data['Controls']['R1/2'] = 1 
                if event.key == K_3:
                    data['Controls']['L2/3'] = 1 
                if event.key == K_4:
                    data['Controls']['R2/4'] = 1 
                if event.key == K_5:
                    data['Controls']['L3/5'] = 1 
                if event.key == K_6:
                    data['Controls']['R3/6'] = 1 
                if event.key == K_7:
                    data['Controls']['SHARE/7'] = 1
                if event.key == K_8:
                    data['Controls']['PS/8'] = 1 
                if event.key == K_9:
                    data['Controls']['OPTIONS/9'] = 1 
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
                    data['Controls']['UP'] = 0    
                if event.key == K_s:
                    data['Controls']['DOWN'] = 0 
                if event.key == K_a:
                    data['Controls']['LEFT'] = 0 
                if event.key == K_d:
                    data['Controls']['RIGHT'] = 0
                if event.key == K_DOWN:
                    data['Controls']['X/ARROW_DOWN'] = 0
                if event.key == K_RIGHT:
                    data['Controls']['CIRCLE/ARROW_RIGHT'] = 0
                if event.key == K_LEFT:
                    data['Controls']['SQUARE/ARROW_LEFT'] = 0
                if event.key == K_UP:
                    data['Controls']['TRIANGLE/ARROW_UP'] = 0
                if event.key == K_1:
                    data['Controls']['L1/1'] = 0
                if event.key == K_2:
                    data['Controls']['R1/2'] = 0
                if event.key == K_3:
                    data['Controls']['L2/3'] = 0
                if event.key == K_4:
                    data['Controls']['R2/4'] = 0
                if event.key == K_5:
                    data['Controls']['L3/5'] = 0
                if event.key == K_6:
                    data['Controls']['R3/6'] = 0
                if event.key == K_7:
                    data['Controls']['SHARE/7'] = 0
                if event.key == K_8:
                    data['Controls']['PS/8'] = 0
                if event.key == K_9:
                    data['Controls']['OPTIONS/9'] = 0
    
        #else mode is controller
        else:
            #handle controller press
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == button_keys['up_arrow']:
                    data['Controls']['UP'] = 1
                if event.button == button_keys['down_arrow']:
                    data['Controls']['DOWN'] = 1
                if event.button == button_keys['left_arrow']:
                    data['Controls']['LEFT'] = 1
                if event.button == button_keys['right_arrow']:
                    data['Controls']['RIGHT'] = 1
                if event.button == button_keys['x']:
                    data['Controls']['X/ARROW_DOWN'] = 1
                if event.button == button_keys['circle']:
                    data['Controls']['CIRCLE/ARROW_RIGHT'] = 1
                if event.button == button_keys['square']:
                    data['Controls']['SQUARE/ARROW_LEFT'] = 1
                if event.button == button_keys['triangle']:
                    data['Controls']['TRIANGLE/ARROW_UP'] = 1
                if event.button == button_keys['L1']:
                    data['Controls']['L1/1'] = 1
                if event.button == button_keys['R1']:
                    data['Controls']['R1/2'] = 1
                if event.button == button_keys['left_stick_click']:
                    data['Controls']['L3/5'] = 1
                if event.button == button_keys['right_stick_click']:
                    data['Controls']['R3/6'] = 1
                if event.button == button_keys['share']: #to switch to keyboard control
                    mode = True
                    data['Controls']['SHARE/7'] = 1
                if event.button == button_keys['PS']:
                    data['Controls']['PS/8'] = 1
                if event.button == button_keys['options']:
                    data['Controls']['OPTIONS/9'] = 1
                #to quit manual control
                if event.button == button_keys['PS']:
                    running = False
            #handle controller release set values equal to 0
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == button_keys['up_arrow']:
                    data['Controls']['UP'] = 0
                if event.button == button_keys['down_arrow']:
                    data['Controls']['DOWN'] = 0
                if event.button == button_keys['left_arrow']:
                    data['Controls']['LEFT'] = 0
                if event.button == button_keys['right_arrow']:
                    data['Controls']['RIGHT'] = 0
                if event.button == button_keys['x']:
                    data['Controls']['X/ARROW_DOWN'] = 0
                if event.button == button_keys['circle']:
                    data['Controls']['CIRCLE/ARROW_RIGHT'] = 0
                if event.button == button_keys['square']:
                    data['Controls']['SQUARE/ARROW_LEFT'] = 0
                if event.button == button_keys['triangle']:
                    data['Controls']['TRIANGLE/ARROW_UP'] = 0
                if event.button == button_keys['L1']:
                    data['Controls']['L1/1'] = 0
                if event.button == button_keys['R1']:
                    data['Controls']['R1/2'] = 0
                if event.button == button_keys['left_stick_click']:
                    data['Controls']['L3/5'] = 0
                if event.button == button_keys['right_stick_click']:
                    data['Controls']['R3/6'] = 0
                if event.button == button_keys['share']:
                    data['Controls']['SHARE/7'] = 0
                if event.button == button_keys['PS']:
                    data['Controls']['PS/8'] = 0
                if event.button == button_keys['options']:
                    data['Controls']['OPTIONS/9'] = 0
            #handle controller analog
            if event.type == pygame.JOYAXISMOTION:
                analog_keys[event.axis] = event.value
                if abs(analog_keys[1]) > .4:
                    if analog_keys[1] < -.7 or analog_keys[1] > .7:
                        data['Controls']['UP/DOWN'] = analog_keys[1]
                    else:
                        data['Controls']['UP/DOWN'] = 0
                if abs(analog_keys[0]) > .4:
                    if analog_keys[0] < -.7 or analog_keys[1] > .7:
                        data['Controls']['LEFT/RIGHT'] = analog_keys[0]
                    else:
                        data['Controls']['LEFT/RIGHT'] = 0
                if analog_keys[2] > .1:
                    data['Controls']['L2/3'] = analog_keys[2]
                else:
                    data['Controls']['L2/3'] = 0
                if analog_keys[3] > .1:
                    data['Controls']['R2/4'] = analog_keys[3]
                else:
                    data['Controls']['R2/4'] = 0
        # close if not running
        if (running == False):
            pygame.display.quit()
            pygame.quit()
            exit()
        return data
'''
        #update json file
        with open("manualOverride.json", "w") as write_file:
            # formatted_data = json.dumps(data, indent=4)
            json.append(data, write_file)
'''
