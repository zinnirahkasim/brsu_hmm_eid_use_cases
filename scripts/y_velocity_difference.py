#!/usr/bin/env python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy
import math
#from std_msgs.msg import String
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *


def callback_1(msg):
    rospy.loginfo("Received side velocity command <</cmd_vel>> message! The value is %f" %msg.linear.y)
    cmd_y_vel = msg.linear.y
    talker(cmd=cmd_y_vel)

def callback_2(msg):
    rospy.loginfo("Received actual y <</odom>> message! The value is %f"%msg.twist.twist.linear.y)
    act_y_vel = msg.twist.twist.linear.y
    talker(act=act_y_vel)

def listener(): 
    rospy.Subscriber("cmd_vel", Twist, callback_1)
    rospy.Subscriber("odom", Odometry, callback_2)

def talker(cmd=0, act=0):
    difference = cmd - act 
    pub = rospy.Publisher('y_velocity_difference', Float64 )
    pub.publish(difference)
    #rospy.sleep(5.0)

if __name__ == '__main__':
    rospy.init_node('y_velocity_difference', anonymous=True)
    
    while not rospy.is_shutdown():
        try:
            listener()
            talker()
        except rospy.ROSInterruptException:
            pass
       