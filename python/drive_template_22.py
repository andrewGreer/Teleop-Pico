# A minimal drive template
# works with the HelloRob (Alternative, second set of) instructions, and "mbot_467.uf2"  (EECS 467 FA23 semester version)

import lcm
from mbot_lcm_msgs import twist2D_t

_lcm = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")
vel = twist2D_t()
vel.vx = 0   # this is the forward speed. Suggest start with maybe 0.5m/s and make it faster/slower as you need.
vel.vy = 0   # this is the speed for going sideways. We don't really use this since our MBot can't go sideways.
vel.wz = 0   # this is the turning speed (rad/s)
_lcm.publish("MBOT_VEL_CMD", vel.encode())



# When you are done with the drive, you can reset the velocities to 0 and rerun "python3 drive_template_22.py" again. This will stop the bot.
