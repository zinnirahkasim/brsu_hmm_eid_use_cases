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

class store_acc_init_y:
    def __init__(self):
        self.acc_init_y= 0
        print self.acc_init_y
        
    def write_file(self, acc_init_y):
        #amount = raw_input("How many objects would you like to spawn? ")
        self.acc_init_y=acc_init_y
        acc_init_file = open('../objects/acc_init_y.yaml', 'w')
        acc_init_details = self.acc_init_y
        yaml.dump(acc_init_details,acc_init_file)
        acc_init_file.close()

    def read_file(self):
        read_yaml_file = open('../objects/acc_init_y.yaml', 'r')
        pass_acc_init = yaml.load(read_yaml_file)
        #rospy.loginfo("inthe file: %f", yaml.load(read_yaml_file))
        print pass_acc_init
        read_yaml_file.close()
        return pass_acc_init
    
def callback(msg):
    rospy.loginfo("Received actual forward acc <</odom>> message! The value is %f" %msg.data)
    svi = store_acc_init_y()
    svi.write_file(acc_init_y=0)
    if rospy.Time.now() == 0:
        acc_init_y = msg.data
        #print acc_init
        svi.write_file(acc_init_y)
    else:
        #how do i get the the vel_init?
        acc_init_y = svi.read_file()
        acc_last_y = msg.data
        print acc_last_y
        jerk_y = (acc_last_y - acc_init_y)/duration
        talker(jerk_y)
        svi.write_file(acc_last_y)
    

def talker(jerk_y):
    rospy.loginfo("y_jerk: %f"%jerk_y)
    pub = rospy.Publisher('y_jerk', Float64 )
    pub.publish(jerk_y)
    
def listener():
    rospy.Subscriber("y_acceleration", Float64, callback)
    
if __name__ == '__main__':
    rospy.init_node('y_jerk', anonymous=True)
    while not rospy.is_shutdown():
        try:
            listener()
            rospy.sleep(duration)
        except rospy.ROSInterruptException:
            pass
