#!/usr/bin/env python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy
import math
#from std_msgs.msg import String
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *


def callback_1(msg):
    rospy.loginfo("Received forward velocity <</cmd_vel>> message! The value is %f" %msg.linear.x)
    cmd_x_vel = msg.linear.x
    talker(cmd=cmd_x_vel)

def callback_2(msg):
    rospy.loginfo("Received actual <</odom>> message! The value is %f"%msg.twist.twist.linear.x)
    act_x_vel = msg.twist.twist.linear.x
    talker(act=act_x_vel)

def listener(): 
    rospy.Subscriber("cmd_vel", Twist, callback_1)
    rospy.Subscriber("odom", Odometry, callback_2)

def talker(cmd=2, act=2):
    difference = math.fabs(cmd - act) 
    rospy.loginfo("difference: %f"%difference)
    pub = rospy.Publisher('x_velocity_difference', Float64 )
    pub.publish(difference)
    #rospy.sleep(0.5)


if __name__ == '__main__':
    rospy.init_node('x_velocity_difference', anonymous=True)
    
    while not rospy.is_shutdown():
        try:
            listener()
            talker()
        except rospy.ROSInterruptException:
            pass
    

