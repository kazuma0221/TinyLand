# coding: UTF-8
from pygame._sdl2 import controller
from pygame.locals import *

class ControllerManager():
    def __init__(self):
        self.ctrl = None
        controller.init()
        if controller.get_count() > 0:
            self.ctrl = controller.Controller(0)
    
    def getLeftStick(self):
        if self.ctrl is None:
            return None
        return (self.ctrl.get_axis(CONTROLLER_AXIS_LEFTX), self.ctrl.get_axis(CONTROLLER_AXIS_LEFTY))

    def getRightStick(self):
        if self.ctrl is None:
            return None
        return (self.ctrl.get_axis(CONTROLLER_AXIS_RIGHTX), self.ctrl.get_axis(CONTROLLER_AXIS_RIGHTY))

    def getButtonA(self):
        if self.ctrl is None:
            return False
        return self.ctrl.get_button(CONTROLLER_BUTTON_A)

if __name__ == '__main__':
    import pygame
    pygame.init()
    print('---TEST STARTS---')
    CM = ControllerManager()

    while not CM.ctrl.get_button(CONTROLLER_BUTTON_Y):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        print(f'LEFT STICK: {CM.getLeftStick()}, RIGHT STICK: {CM.getRightStick()}')
        if CM.getButtonA():
            print('A is being pushed')
    print('---Y is pushed; TEST ENDS---')
