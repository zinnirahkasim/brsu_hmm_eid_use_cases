#!/usr/bin/env python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy
import math
import yaml
#from std_msgs.msg import String
from std_msgs.msg import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *

duration =8

class store_acc_init_x:
    def __init__(self):
        self.acc_init_x= 0
        #print self.acc_init_x
        
    def write_file(self, acc_init_x):
        #amount = raw_input("How many objects would you like to spawn? ")
        self.acc_init_x=acc_init_x
        acc_init_file = open('../objects/acc_init_x.yaml', 'w')
        acc_init_details = self.acc_init_x
        yaml.dump(acc_init_details,acc_init_file)
        acc_init_file.close()

    def read_file(self):
        read_yaml_file = open('../objects/acc_init_x.yaml', 'r')
        pass_acc_init = yaml.load(read_yaml_file)
        #rospy.loginfo("inthe file: %f", yaml.load(read_yaml_file))
        #print pass_acc_init
        read_yaml_file.close()
        return pass_acc_init
    
def callback(msg):
    rospy.loginfo("Received actual forward acc <</odom>> message! The value is %f" %msg.data)
    svi = store_acc_init_x()
    svi.write_file(acc_init_x=0)
    if rospy.Time.now() == 0:
        acc_init_x = msg.data
        #print acc_init
        svi.write_file(acc_init_x)
    else:
        #how do i get the the vel_init?
        acc_init_x = svi.read_file()
        acc_last_x = msg.data
        #print acc_last_x
        jerk_x = (acc_last_x - acc_init_x)/duration
        talker(jerk_x)
        svi.write_file(acc_last_x)
    

def talker(jerk_x):
    rospy.loginfo("x_jerk: %f"%jerk_x)
    pub = rospy.Publisher('x_jerk', Float64 )
    pub.publish(jerk_x)
    
def listener():
    rospy.Subscriber("x_acceleration", Float64, callback)
    
if __name__ == '__main__':
    rospy.init_node('x_jerk', anonymous=True)
    while not rospy.is_shutdown():
        try:
            listener()
            rospy.sleep(duration)
        except rospy.ROSInterruptException:
            pass
