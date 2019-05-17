import sys, pygame
import time
import math
import pyautogui
import keyboard
import random
from os import system

pygame.init()
size = width, height = 500, 500

mouse_delta = pyautogui.position();

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

running = True

START_TIME = time.time();

LOOP_SPEED = 50;

#colors

WHITE = (255, 255, 255)
PV_COLOR = (0, 200, 50)
CV_COLOR = (200, 50, 0)
LIGHT_BLUE = (0, 50, 200)

CONST_ERROR = 0;

#set point
screen_sp = height / 2
SP = 0

#control variable
CV = 0

#process variable 
PV = 0

#last error
LAST_ERROR = 0;

#last integral
LAST_INTEGRAL = 0;


pv_plot = []
cv_plot = []

P, I, D = 0, 0, 0


def calculate_output():
    global LAST_INTEGRAL, LAST_ERROR

    ERROR = SP - PV
    
    proportional = P * ERROR

    integral = LAST_INTEGRAL + (ERROR * LOOP_SPEED / 1000)

    derivative = (ERROR - LAST_ERROR) * (LOOP_SPEED / 1000)

    CV = proportional + I * integral + D * derivative
    
    print("P: ", proportional)
    print("I: ", integral * I)
    print("D: ", integral * D)
    print("")
    print("ERROR: ", ERROR)
    if CV > 0:
        set_output(CV)
    elif CV < 0:
        set_output(CV)
    else:
        set_output(0)

    pv_plot[-1] = (pv_plot[-1][0], PV)
    cv_plot[-1] = (cv_plot[-1][0], CV)

    LAST_INTEGRAL = integral
    LAST_ERROR = ERROR


def to_real(y):
    return float(y) / (height / 10)

def to_screen(y):
    mid_point = int(height / 2)
    return int(-y * (height / 10) + mid_point)

#def to_screen(*()):
#    return (point[0], to_screen(point[1]))

def init_plot(plot):
    for x in range(0, width - 50, 1):
        plot.append((x, 0))

def shift_plot(plot):
    for x in range(1, len(plot), 1):
        plot[x - 1] = (x - 1, plot[x][1])


def draw_grid():
    pygame.draw.line(screen, WHITE, [0, height / 2], [width, height / 2], 2)
    pygame.draw.line(screen, LIGHT_BLUE, [0, screen_sp], [width, screen_sp], 1)
    for y in range(0, int(height), int(height / 10)):
        pygame.draw.line(screen, (50, 50, 50), [0, y], [width, y], 1)    

def draw_graph(plot, color):
    for x in range(0, len(pv_plot) - 3, 2):
        
        p1 = (x, to_screen(plot[x][1]))
        p2 = (x + 1, to_screen(plot[x + 1][1]))
        p3 = (x + 2, to_screen(plot[x + 2][1]))
        

        pygame.draw.line(screen, color, p1, p2, 1)
        pygame.draw.line(screen, color, p2, p3, 1)

def graph_value(rx):
    mid_point = int(height / 2)
    return int(math.sin(rx) * 100.0 + mid_point)

def real_x(screen_x):
    mul = 5 
    return (float(screen_x / 100) + elapsed_time / 10) * mul

def handle_input():
    global screen_sp
    global delta_mouse
    if keyboard.is_pressed('w') and screen_sp <= height:
         screen_sp += delta_mouse[1]
        
    
    global SP

    screen_sp = (max(0, min(screen_sp, height)))

    SP = -(screen_sp - height / 2) / 50


def set_output(cv):
    global PV
    global CONST_ERROR
    PV += cv
   

init_plot(cv_plot);
init_plot(pv_plot);

last_pos = pyautogui.position() 

if __name__ == "__main__":
    err = float(sys.argv[1])
    P = float(sys.argv[2])
    I = float(sys.argv[3])
    D = float(sys.argv[4])
    CONST_ERROR = err

while running:

    mouse_pos = pyautogui.position() 

    delta_mouse = (mouse_pos[0] - last_pos[0], mouse_pos[1] - last_pos[1])

    last_pos = mouse_pos

    #elapsed_time = time.time() - START_TIME;
    PV += CONST_ERROR

    
    #set point calculated
    handle_input()


    shift_plot(cv_plot)
    shift_plot(pv_plot)

    #last index is free

    calculate_output()

    draw_grid()
    draw_graph(cv_plot, CV_COLOR)
    draw_graph(pv_plot, PV_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    screen.fill((0,0,0))
    pygame.time.wait(LOOP_SPEED)
    system('clear')


    
    




