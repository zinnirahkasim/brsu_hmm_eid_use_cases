#!/usr/bin/env python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy
import math
#from std_msgs.msg import String
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *


def callback(msg,i,N):
    rospy.loginfo("Received actual side velocity <</odom>> message! The value is %f" %msg.twist.twist.linear.y)
    if i == 0:
        vel_init = msg.twist.twist.linear.y
    if i == (N):
        vel_last = msg.twist.twist.linear.y
        acceleration = (vel_last - vel_init)/(N)
        talker(acc=acceleration)
    
def talker(acc):
    rospy.loginfo("y_acceleration: %f"%acc)
    pub = rospy.Publisher('y_acceleration', Float64 )
    pub.publish(difference)
    
def listener(i,N):
    rospy.Subscriber("odom", Odometry, callback(msg, i,N))
    
if __name__ == '__main__':
    rospy.init_node('y_acceleration', anonymous=True)
    
    while not rospy.is_shutdown():
        try:
            N=4
            for i in range(N):
                listener(i,N)
            talker()
        except rospy.ROSInterruptException:
            pass