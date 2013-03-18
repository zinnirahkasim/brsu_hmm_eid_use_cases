#!/usr/bin/env python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy
import math
import yaml
#from std_msgs.msg import String
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *

class store_cmd_x:
    def __init__(self):
        self.vel_cmd_x= 0
        #print self.vel_init_x
        
    def write_file(self, vel_cmd_x):
        #amount = raw_input("How many objects would you like to spawn? ")
        self.vel_cmd_x=vel_cmd_x
        vel_cmd_file = open('../objects/vel_cmd_x.yaml', 'w')
        vel_cmd_details = self.vel_cmd_x
        yaml.dump(vel_cmd_details,vel_cmd_file)
        vel_cmd_file.close()

    def read_file(self):
        read_yaml_file = open('../objects/vel_cmd_x.yaml', 'r')
        pass_velocity_cmd = yaml.load(read_yaml_file)
        #rospy.loginfo("inthe file: %f", yaml.load(read_yaml_file))
        #print pass_velocity_init
        read_yaml_file.close()
        return pass_velocity_cmd

class store_act_x:
    def __init__(self):
        self.vel_act_x= 0
        #print self.vel_init_x
        
    def write_file(self, vel_act_x):
        #amount = raw_input("How many objects would you like to spawn? ")
        self.vel_act_x=vel_act_x
        vel_act_file = open('../objects/vel_act_x.yaml', 'w')
        vel_act_details = self.vel_act_x
        yaml.dump(vel_act_details,vel_act_file)
        vel_act_file.close()

    def read_file(self):
        read_yaml_file = open('../objects/vel_act_x.yaml', 'r')
        pass_velocity_act = yaml.load(read_yaml_file)
        #rospy.loginfo("inthe file: %f", yaml.load(read_yaml_file))
        #print pass_velocity_init
        read_yaml_file.close()
        return pass_velocity_act



def callback_1(msg):
    rospy.loginfo("Received forward velocity <</cmd_vel>> message! The value is %f" %msg.linear.x)
    vel_cmd_x = msg.linear.x
    scx = store_cmd_x()
    if vel_cmd_x is None:
        scx.write_file(vel_cmd_x=0)
    else:
        scx.write_file(vel_cmd_x)

def callback_2(msg):
    rospy.loginfo("Received actual x <</odom>> message! The value is %f"%msg.twist.twist.linear.x)
    vel_act_x = msg.twist.twist.linear.x
    sax = store_act_x()
    if vel_act_x is None:
        scx.write_file(vel_act_x=0)
    else:
        sax.write_file(vel_act_x)

def listener(): 
    rospy.Subscriber("cmd_vel", Twist, callback_1)
    rospy.Subscriber("odom", Odometry, callback_2)
    
def talker():
    scx = store_cmd_x()
    sax = store_act_x()
    
    cmd = scx.read_file()
    act = sax.read_file()
     
    #try:
    difference = cmd -act 
    rospy.loginfo("difference: %f"%difference)
    pub = rospy.Publisher('x_velocity_difference', Float64 )
    pub.publish(difference)
    #except rospy.ROSException:
    #    rospy.loginfo("cannot find difference")
   
    #rospy.sleep(0.5)


if __name__ == '__main__':
    rospy.init_node('x_velocity_difference', anonymous=True)
    
    while not rospy.is_shutdown():
        try:
            listener()
            talker()
        except rospy.ROSInterruptException:
            pass
    

