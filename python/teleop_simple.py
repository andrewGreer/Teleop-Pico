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
        if key_input[pygame.K_LEFT]:
            print('left')
            # cur_motor_command.trans_v = 0.0 # m/s
            cur_motor_command.angular_v = 2.0
            # print("Left ticks: " + str(LEFT_ENC_POL * cur_encoder_values.leftticks))
            # print("Right ticks: " + str(RIGHT_ENC_POL * cur_encoder_values.rightticks))
            # print("Left delta: " + str(LEFT_ENC_POL * cur_encoder_values.left_delta))
            # print("Right delta: " + str(RIGHT_ENC_POL * cur_encoder_values.right_delta))
        elif key_input[pygame.K_RIGHT]:
            print('right')
            # cur_motor_command.trans_v = 0.0 # m/s
            cur_motor_command.angular_v = -2.0
            # print("Left ticks: " + str(LEFT_ENC_POL * cur_encoder_values.leftticks))
            # print("Right ticks: " + str(RIGHT_ENC_POL * cur_encoder_values.rightticks))
            # print("Left delta: " + str(LEFT_ENC_POL * cur_encoder_values.left_delta))
            # print("Right delta: " + str(RIGHT_ENC_POL * cur_encoder_values.right_delta))
        if key_input[pygame.K_UP]:
            print('forward')
            cur_motor_command.trans_v = 0.25 # m/s
            cur_motor_command.angular_v = 0.1
            # print("Left ticks: " + str(LEFT_ENC_POL * cur_encoder_values.leftticks))
            # print("Right ticks: " + str(RIGHT_ENC_POL * cur_encoder_values.rightticks))
            # print("Left delta: " + str(LEFT_ENC_POL * cur_encoder_values.left_delta))
            # print("Right delta: " + str(RIGHT_ENC_POL * cur_encoder_values.right_delta))
        elif key_input[pygame.K_DOWN]:
            print('backward')
            cur_motor_command.trans_v = -0.25 # m/s
            cur_motor_command.angular_v = -0.1
            # print("Left ticks: " + str(LEFT_ENC_POL * cur_encoder_values.leftticks))
            # print("Right ticks: " + str(RIGHT_ENC_POL * cur_encoder_values.rightticks))
            # print("Left delta: " + str(LEFT_ENC_POL * cur_encoder_values.left_delta))
            # print("Right delta: " + str(RIGHT_ENC_POL * cur_encoder_values.right_delta))
        if (cur_motor_command.trans_v == 0.0 and cur_motor_command.angular_v == 0.0):
            print('stopped')
            # print("Left ticks: " + str(LEFT_ENC_POL * cur_encoder_values.leftticks))
            # print("Right ticks: " + str(RIGHT_ENC_POL * cur_encoder_values.rightticks))
            # print("Left delta: " + str(LEFT_ENC_POL * cur_encoder_values.left_delta))
            # print("Right delta: " + str(RIGHT_ENC_POL * cur_encoder_values.right_delta))
        lc.publish("MBOT_MOTOR_COMMAND", cur_motor_command.encode())
        time.sleep(0.05)

# 2.6 s to turn right
# 2.5 s to turn left
# 8.5 s on 1 m

if __name__== "__main__":
    main()

