#!/usr/bin/env python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy
import math
#from std_msgs.msg import String
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *


def callback(msg):
    rospy.loginfo("Received actual forward velocity <</odom>> message! The value is %f" %msg.twist.twist.linear.x)
    if rospy.Time.now() == 0:
        vel_init = msg.twist.twist.linear.x
        buffer_function(vel_init) #?
    else:
        #how do i get the the vel_init?
        vel_init = buffer_function()
        vel_last = msg.twist.twist.linear.x
        acceleration = (vel_last - vel_init)/4
        talker(acceleration)
        buffer_function(vel_last)
    
def buffer_function(*args):
    for each in args:
        return each
    

def talker(acc):
    rospy.loginfo("x_acceleration: %f"%acc)
    pub = rospy.Publisher('x_acceleration', Float64 )
    pub.publish(acc)
    
def listener():
    rospy.Subscriber("odom", Odometry, callback)
    
if __name__ == '__main__':
    rospy.init_node('x_acceleration', anonymous=True)
    
    duration = 4
    while not rospy.is_shutdown():
        try:
            listener()
            rospy.sleep(duration)
        except rospy.ROSInterruptException:
            pass