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

class store_vel_init_x:
    def __init__(self):
        self.vel_init_x= 0
        #print self.vel_init_x
        
    def write_file(self, vel_init_x):
        #amount = raw_input("How many objects would you like to spawn? ")
        self.vel_init_x=vel_init_x
        vel_init_file = open('../objects/vel_init_x.yaml', 'w')
        vel_init_details = self.vel_init_x
        yaml.dump(vel_init_details,vel_init_file)
        vel_init_file.close()

    def read_file(self):
        read_yaml_file = open('../objects/vel_init_x.yaml', 'r')
        pass_velocity_init = yaml.load(read_yaml_file)
        #rospy.loginfo("inthe file: %f", yaml.load(read_yaml_file))
        print pass_velocity_init
        read_yaml_file.close()
        return pass_velocity_init
    
def callback(msg):
    rospy.loginfo("Received actual forward velocity <</odom>> message! The value is %f" %msg.twist.twist.linear.x)
    svi = store_vel_init_x()
    svi.write_file(vel_init_x=0)
    if rospy.Time.now() == 0:
        vel_init = msg.twist.twist.linear.x
        #print vel_init
        svi.write_file(vel_init_x)
    else:
        #how do i get the the vel_init?
        vel_init_x = svi.read_file()
        vel_last_x = msg.twist.twist.linear.x
        #print vel_last_x
        acceleration_x = (vel_last_x - vel_init_x)/duration
        talker(acceleration_x)
        svi.write_file(vel_last_x)
    

def talker(acc_x):
    rospy.loginfo("x_acceleration: %f"%acc_x)
    pub = rospy.Publisher('x_acceleration', Float64 )
    pub.publish(acc_x)
    
def listener():
    rospy.Subscriber("odom", Odometry, callback)
    
if __name__ == '__main__':
    rospy.init_node('x_acceleration', anonymous=True)
    while not rospy.is_shutdown():
        try:
            listener()
            rospy.sleep(duration)
        except rospy.ROSInterruptException:
            pass
