#!/usr/bin/env python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy
import math
import yaml
#from std_msgs.msg import String
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *


duration =4

class store_vel_init_y:
    def __init__(self):
        self.vel_init_y= 0
        print self.vel_init_y
        
    def write_file(self, vel_init_y):
        #amount = raw_input("How many objects would you like to spawn? ")
        self.vel_init_y=vel_init_y
        vel_init_file = open('../objects/vel_init_y.yaml', 'w')
        vel_init_details = self.vel_init_y
        yaml.dump(vel_init_details,vel_init_file)
        vel_init_file.close()

    def read_file(self):
        read_yaml_file = open('../objects/vel_init_y.yaml', 'r')
        pass_velocity_init = yaml.load(read_yaml_file)
        #rospy.loginfo("inthe file: %f", yaml.load(read_yaml_file))
        #print pass_velocity_init
        read_yaml_file.close()
        return pass_velocity_init
    
def callback(msg):
    rospy.loginfo("Received actual side velocity <</odom>> message! The value is %f" %msg.twist.twist.linear.y)
    svi = store_vel_init_y()
    svi.write_file(vel_init_y=0)
    if rospy.Time.now() == 0:
        vel_init_y = msg.twist.twist.linear.y
        print vel_init_y
        svi.write_file(vel_init_y)
    else:
        #how do i get the the vel_init?
        vel_init_y = svi.read_file()
        vel_last_y = msg.twist.twist.linear.x
        #print vel_last_y
        acceleration_y = (vel_last_y - vel_init_y)/duration
        talker(acceleration_y)
        svi.write_file(vel_last_y)
    
def talker(acc_y):
    rospy.loginfo("y_acceleration: %f"%acc_y)
    pub = rospy.Publisher('y_acceleration', Float64 )
    pub.publish(acc_y)
    
def listener():
    rospy.Subscriber("odom", Odometry, callback)
    
if __name__ == '__main__':
    rospy.init_node('y_acceleration', anonymous=True)
    
    while not rospy.is_shutdown():
        try:
            listener()
            rospy.sleep(duration)
        except rospy.ROSInterruptException:
            pass