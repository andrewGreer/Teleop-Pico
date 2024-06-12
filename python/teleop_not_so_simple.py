import pygame 
import lcm
import numpy as np
from lcmtypes import mbot_motor_command_t
from lcmtypes import mbot_encoder_t
import time
import sys
import os
from threading import Thread, Lock, current_thread
from mbot_params import *

cur_encoder_values = None
FWD_VEL = 0.8
REV_VEL = -0.9
RIGHT_VEL = -1.9
LEFT_VEL = 2.1
UP_COR = 0.41
REV_COR = 0.0
RIGHT_AUG = -4.0
LEFT_AUG = 4.0

def encoder_message_handler(channel, data):
    global cur_encoder_values
    cur_encoder_values = mbot_encoder_t.decode(data)

def handle_lcm(lcm_obj):
    try:
        while True:
            lcm_obj.handle()
    except KeyboardInterrupt:
        print("lcm exit!")
        sys.exit()

def transition(old : mbot_motor_command_t, new : mbot_motor_command_t) -> mbot_motor_command_t:
    d_trans = new.trans_v - old.trans_v
    d_ang = new.angular_v - old.angular_v

    if (d_trans > 0.1): d_trans = 0.1
    if (d_trans < -0.1): d_trans = -0.1
    if (d_ang > 2): d_ang = 2
    if (d_ang < -2): d_ang = -2

    smooth = mbot_motor_command_t()
    smooth.trans_v = old.trans_v + d_trans
    smooth.angular_v = old.angular_v + d_ang

    return smooth

def main():
    print("creating LCM ...")
    lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")
    lcm_kill_thread = Thread(target = handle_lcm, args= (lc, ), daemon = True)
    lcm_kill_thread.start()
    pygame.init()
    pygame.display.set_caption("MBot TeleOp")
    screen = pygame.display.set_mode([100,100])
    subscription = lc.subscribe("MBOT_ENCODERS", encoder_message_handler)
    time.sleep(0.5)
    
    print('resetting encoders')
    cur_encoder_msg = mbot_encoder_t()
    lc.publish("RESET_ENCODERS", cur_encoder_msg.encode())
    
    prev_motor_command = mbot_motor_command_t()
    prev_motor_command.angular_v = 0.0
    prev_motor_command.trans_v = 0.0

    time.sleep(0.5)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        key_input = pygame.key.get_pressed() 
        cur_motor_command = mbot_motor_command_t()
        cur_motor_command.trans_v = 0.0
        cur_motor_command.angular_v = 0.0
        if key_input[pygame.K_q]:
            pygame.quit()
            sys.exit()
        elif key_input[pygame.K_LEFT] and key_input[pygame.K_UP]:
            print('left-up')
            cur_motor_command.trans_v = FWD_VEL # m/s
            cur_motor_command.angular_v = LEFT_VEL + LEFT_AUG + UP_COR

            cur_motor_command = transition(prev_motor_command, cur_motor_command)
            prev_motor_command = cur_motor_command
            if (cur_motor_command.trans_v == FWD_VEL and cur_motor_command.angular_v == LEFT_VEL + LEFT_AUG + UP_COR):
                print('===SETPOINT REACHED===')
        elif key_input[pygame.K_RIGHT] and key_input[pygame.K_UP]:
            print('right-up')
            cur_motor_command.trans_v = FWD_VEL # m/s
            cur_motor_command.angular_v = RIGHT_VEL + RIGHT_AUG + UP_COR
            
            cur_motor_command = transition(prev_motor_command, cur_motor_command)
            prev_motor_command = cur_motor_command
            if (cur_motor_command.trans_v == FWD_VEL and cur_motor_command.angular_v == RIGHT_VEL + RIGHT_AUG + UP_COR):
                print('===SETPOINT REACHED===')
        elif key_input[pygame.K_RIGHT] and key_input[pygame.K_DOWN]:
            print('right-down')
            cur_motor_command.trans_v = REV_VEL # m/s
            cur_motor_command.angular_v = LEFT_VEL + LEFT_AUG + REV_COR
            
            cur_motor_command = transition(prev_motor_command, cur_motor_command)
            prev_motor_command = cur_motor_command
            if (cur_motor_command.trans_v == REV_VEL and cur_motor_command.angular_v == LEFT_VEL + LEFT_AUG + REV_COR):
                print('===SETPOINT REACHED===')
        elif key_input[pygame.K_LEFT] and key_input[pygame.K_DOWN]:
            print('left-down')
            cur_motor_command.trans_v = REV_VEL # m/s
            cur_motor_command.angular_v = RIGHT_VEL + RIGHT_AUG + REV_COR
            
            cur_motor_command = transition(prev_motor_command, cur_motor_command)
            prev_motor_command = cur_motor_command
            if (cur_motor_command.trans_v == REV_VEL and cur_motor_command.angular_v == RIGHT_VEL + RIGHT_AUG + REV_COR):
                print('===SETPOINT REACHED===')
        elif key_input[pygame.K_LEFT]:
            print('left')
            cur_motor_command.trans_v = 0.0 # m/s
            cur_motor_command.angular_v = LEFT_VEL
            
            cur_motor_command = transition(prev_motor_command, cur_motor_command)
            prev_motor_command = cur_motor_command
            if (cur_motor_command.trans_v == 0.0 and cur_motor_command.angular_v == LEFT_VEL):
                print('===SETPOINT REACHED===')
        elif key_input[pygame.K_RIGHT]:
            print('right')
            cur_motor_command.trans_v = 0.0 # m/s
            cur_motor_command.angular_v = RIGHT_VEL
            
            cur_motor_command = transition(prev_motor_command, cur_motor_command)
            prev_motor_command = cur_motor_command
            if (cur_motor_command.trans_v == 0.0 and cur_motor_command.angular_v == RIGHT_VEL):
                print('===SETPOINT REACHED===')
        elif key_input[pygame.K_UP] and key_input[pygame.K_z]:
            print('forward')
            cur_motor_command.trans_v = FWD_VEL/3 # m/s
            cur_motor_command.angular_v = 0.0
            
            cur_motor_command = transition(prev_motor_command, cur_motor_command)
            prev_motor_command = cur_motor_command
            if (cur_motor_command.trans_v == FWD_VEL/3 and cur_motor_command.angular_v == 0.0):
                print('===SETPOINT REACHED===')
        elif key_input[pygame.K_DOWN] and key_input[pygame.K_z]:
            print('backward')
            cur_motor_command.trans_v = REV_VEL/3 # m/s
            cur_motor_command.angular_v = 0.0
            
            cur_motor_command = transition(prev_motor_command, cur_motor_command)
            prev_motor_command = cur_motor_command
            if (cur_motor_command.trans_v == REV_VEL/3 and cur_motor_command.angular_v == 0.0):
                print('===SETPOINT REACHED===')
        elif key_input[pygame.K_UP]:
            print('forward')
            cur_motor_command.trans_v = FWD_VEL # m/s
            cur_motor_command.angular_v = UP_COR
            
            cur_motor_command = transition(prev_motor_command, cur_motor_command)
            prev_motor_command = cur_motor_command
            if (cur_motor_command.trans_v == FWD_VEL and cur_motor_command.angular_v == UP_COR):
                print('===SETPOINT REACHED===')
        elif key_input[pygame.K_DOWN]:
            print('backward')
            cur_motor_command.trans_v = REV_VEL # m/s
            cur_motor_command.angular_v = REV_COR
            
            cur_motor_command = transition(prev_motor_command, cur_motor_command)
            prev_motor_command = cur_motor_command
            if (cur_motor_command.trans_v == REV_VEL and cur_motor_command.angular_v == REV_COR):
                print('===SETPOINT REACHED===')
        else:
            print('stopping')
            cur_motor_command.trans_v = 0.0 # m/s
            cur_motor_command.angular_v = 0.0
            
            cur_motor_command = transition(prev_motor_command, cur_motor_command)
            prev_motor_command = cur_motor_command
            if (cur_motor_command.trans_v == 0.0 and cur_motor_command.angular_v == 0.0):
                print('===SETPOINT REACHED===')
        if (cur_motor_command.trans_v == 0.0 and cur_motor_command.angular_v == 0.0):
            print('stopped')

        print("Set translational ", cur_motor_command.trans_v)
        print("Set angular ", cur_motor_command.angular_v)

        lc.publish("MBOT_MOTOR_COMMAND", cur_motor_command.encode())
        time.sleep(0.05)

# 2.6 s to turn right
# 2.5 s to turn left
# 8.5 s on 1 m

if __name__== "__main__":
    main()

