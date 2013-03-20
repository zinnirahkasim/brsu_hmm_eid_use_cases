#!/usr/bin/env python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy
import math
import yaml
#from std_msgs.msg import String
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *


class store_cmd_y:
    def __init__(self):
        self.vel_cmd_y= 0
        #print self.vel_init_y
        
    def write_file(self, vel_cmd_y):
        #amount = raw_input("How many objects would you like to spawn? ")
        self.vel_cmd_y=vel_cmd_y
        vel_cmd_file = open('/home/zinnirah/ros/workspace/thesis/kee_use_cases/objects/vel_cmd_y.yaml', 'w')
        vel_cmd_details = self.vel_cmd_y
        yaml.dump(vel_cmd_details,vel_cmd_file)
        vel_cmd_file.close()

    def read_file(self):
        read_yaml_file = open('/home/zinnirah/ros/workspace/thesis/kee_use_cases/objects/vel_cmd_y.yaml', 'r')
        pass_velocity_cmd = yaml.load(read_yaml_file)
        #rospy.loginfo("inthe file: %f", yaml.load(read_yaml_file))
        #print pass_velocity_init
        read_yaml_file.close()
        return pass_velocity_cmd

class store_act_y:
    def __init__(self):
        self.vel_act_y= 0
        #print self.vel_init_y
        
    def write_file(self, vel_act_y):
        #amount = raw_input("How many objects would you like to spawn? ")
        self.vel_act_y=vel_act_y
        vel_act_file = open('/home/zinnirah/ros/workspace/thesis/kee_use_cases/objects/vel_act_y.yaml', 'w')
        vel_act_details = self.vel_act_y
        yaml.dump(vel_act_details,vel_act_file)
        vel_act_file.close()

    def read_file(self):
        read_yaml_file = open('/home/zinnirah/ros/workspace/thesis/kee_use_cases/objects/vel_act_y.yaml', 'r')
        pass_velocity_act = yaml.load(read_yaml_file)
        #rospy.loginfo("inthe file: %f", yaml.load(read_yaml_file))
        #print pass_velocity_init
        read_yaml_file.close()
        return pass_velocity_act



def callback_1(msg):
    rospy.loginfo("Received forward velocity <</cmd_vel>> message! The value is %f" %msg.linear.y)
    vel_cmd_y = msg.linear.y
    scy = store_cmd_y()
    if vel_cmd_y is None:
        scy.write_file(vel_cmd_y=0)
    else:
        scy.write_file(vel_cmd_y)

def callback_2(msg):
    rospy.loginfo("Received actual y <</odom>> message! The value is %f"%msg.twist.twist.linear.y)
    vel_act_y = msg.twist.twist.linear.y
    say = store_act_y()
    if vel_act_y is None:
        scy.write_file(vel_act_y=0)
    else:
        say.write_file(vel_act_y)

def listener(): 
    rospy.Subscriber("cmd_vel", Twist, callback_1)
    rospy.Subscriber("odom", Odometry, callback_2)
    
def talker():
    scy = store_cmd_y()
    say = store_act_y()
    
    cmd = scy.read_file()
    act = say.read_file()
    
    if cmd is None:
        cmd = 0
    if act is None:
        act = 0
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
       