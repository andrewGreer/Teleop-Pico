import lcm
import numpy as np
from lcmtypes import mbot_motor_command_t
from lcmtypes import mbot_encoder_t
import time
import sys
import os
from threading import Thread, Lock, current_thread

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

#   fwd 1 m
# 5890 L
# -5744 R
        
#   turn left 90
# -655 L
# -694 R

def main():
    print("creating LCM ...")
    lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")
    lcm_kill_thread = Thread(target = handle_lcm, args= (lc, ), daemon = True)
    lcm_kill_thread.start()
    subscription = lc.subscribe("MBOT_ENCODERS", encoder_message_handler)
    time.sleep(0.5)
    
    print('resetting encoders')
    cur_encoder_msg = mbot_encoder_t()
    lc.publish("RESET_ENCODERS", cur_encoder_msg.encode())
    
    time.sleep(0.5)
    print('I am driving straight and checking my encoders as I go')

    for j in range(4):
        while ((cur_encoder_values.leftticks < 5891) and (cur_encoder_values.rightticks > -5745)):
            print("Left ticks: " + str(cur_encoder_values.leftticks))
            print("Right ticks: " + str(cur_encoder_values.rightticks))
            print("Left delta: " + str(cur_encoder_values.left_delta))
            print("Right delta: " + str(cur_encoder_values.right_delta))

            cur_motor_command = mbot_motor_command_t()
            cur_motor_command.trans_v = 0.25
            cur_motor_command.angular_v = -0.395
            lc.publish("MBOT_MOTOR_COMMAND", cur_motor_command.encode())
            time.sleep(0.05) #sleep time between published messages is how long the motor command will be executed for

        time.sleep(0.5)
        print('resetting encoders')
        cur_encoder_msg = mbot_encoder_t()
        lc.publish("RESET_ENCODERS", cur_encoder_msg.encode())

        print("Left ticks: " + str(cur_encoder_values.leftticks))
        print("Left delta: " + str(cur_encoder_values.left_delta))
        print("Right ticks: " + str(cur_encoder_values.rightticks))
        print("Right delta: " + str(cur_encoder_values.right_delta))

        cur_motor_command = mbot_motor_command_t()
        cur_motor_command.trans_v = 0.0
        cur_motor_command.angular_v = 0.0
        lc.publish("MBOT_MOTOR_COMMAND", cur_motor_command.encode())
        print("I am stopping")
        print("Left ticks: " + str(cur_encoder_values.leftticks))
        print("Right ticks: " + str(cur_encoder_values.rightticks))
        print("Left delta: " + str(cur_encoder_values.left_delta))
        print("Right delta: " + str(cur_encoder_values.right_delta))
        time.sleep(0.5)

        print('I am turning and checking my encoders as I go')
        while ((cur_encoder_values.leftticks > -500) and (cur_encoder_values.rightticks > -906)):
            print("Left ticks: " + str(cur_encoder_values.leftticks))
            #print("Right ticks: " + str(cur_encoder_values.rightticks))
            print("Left delta: " + str(cur_encoder_values.left_delta))
            #print("Right delta: " + str(cur_encoder_values.right_delta))

            cur_motor_command = mbot_motor_command_t()
            cur_motor_command.trans_v = 0.0
            cur_motor_command.angular_v = 2.0
            lc.publish("MBOT_MOTOR_COMMAND", cur_motor_command.encode())
            time.sleep(0.05)
        
        time.sleep(0.5)
        print('resetting encoders')
        cur_encoder_msg = mbot_encoder_t()
        lc.publish("RESET_ENCODERS", cur_encoder_msg.encode())

        print("Left ticks: " + str(cur_encoder_values.leftticks))
        print("Left delta: " + str(cur_encoder_values.left_delta))
        print("Right ticks: " + str(cur_encoder_values.rightticks))
        print("Right delta: " + str(cur_encoder_values.right_delta))

        cur_motor_command = mbot_motor_command_t()
        cur_motor_command.trans_v = 0.0
        cur_motor_command.angular_v = 0.0
        lc.publish("MBOT_MOTOR_COMMAND", cur_motor_command.encode())
        print("I am stopping")
        print("Left ticks: " + str(cur_encoder_values.leftticks))
        print("Right ticks: " + str(cur_encoder_values.rightticks))
        print("Left delta: " + str(cur_encoder_values.left_delta))
        print("Right delta: " + str(cur_encoder_values.right_delta))
        time.sleep(0.5)

    cur_motor_command = mbot_motor_command_t()
    cur_motor_command.trans_v = 0.0
    cur_motor_command.angular_v = 0.0
    lc.publish("MBOT_MOTOR_COMMAND", cur_motor_command.encode())
    print("I am stopping")

if __name__== "__main__":
    main()
