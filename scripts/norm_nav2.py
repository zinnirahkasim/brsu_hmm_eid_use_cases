#!/usr/bin/python
import roslib; roslib.load_manifest('brsu_hmm_eid_use_cases')
import rospy

import smach
import smach_ros
import arm_navigation_msgs.msg
from std_msgs.msg import Float64

import random 
import yaml

from simple_script_server import *
sss = simple_script_server()
# scenario specific states
#from fetch_and_carry_demo_states import *

class set_param_for_stretch_arm:
    def __init__(self, amount):
        self.amount=amount
        
        
    def write_yaml_files(self):
        #amount = raw_input("How many objects would you like to spawn? ")
        stretch_arm_yaml_file = open('/home/zinnirah/ros/workspace/thesis/brsu_hmm_eid_use_cases/objects/stretch_arm.yaml', 'w')
        for i in range(self.amount):
            self.arm_joint_1 = random.uniform(0.0100692, 5.84014)
            self.arm_joint_2 = random.uniform(0.0100692, 2.61799)
            self.arm_joint_3 = random.uniform(-5.02655, -0.015708)
            self.arm_joint_4 = random.uniform(0.0221239, 3.4292)
            self.arm_joint_5 = random.uniform(0.110619, 5.64159)
            
            arm_details = {'stretch_arm_'+str(i+1): [self.arm_joint_1,self.arm_joint_2,self.arm_joint_3,self.arm_joint_4,self.arm_joint_5]}
            yaml.dump(arm_details,stretch_arm_yaml_file)
        
        stretch_arm_yaml_file.close()

    def set_parameter(self):
        read_yaml_file = open('/home/zinnirah/ros/workspace/thesis/brsu_hmm_eid_use_cases/objects/stretch_arm.yaml', 'r')
        rospy.set_param("/script_server/stretch_arm/", yaml.load(read_yaml_file))
        print yaml.load(read_yaml_file)
        read_yaml_file.close()
        
                
def main():
    rospy.init_node('stretch_arm')
    
    #amount=input("Please enter the amount of arm configurations you like: ")
    #sp = set_param_for_stretch_arm(amount)
    #sp.write_yaml_files()
    #sp.set_parameter()
        
    #if rospy.has_param('/script_server/stretch_arm/'):
    #    print "yay!"
    #sss.move("base", "D1")
    sss.move("arm", "home")
    sss.move("base", "S1")
    rospy.loginfo('Arm at home base at S1')
    sss.move("arm", "candle")
    sss.move("base", "S2")
    rospy.loginfo('Arm at candle base at S2')
    sss.move("arm", "out_of_view")
    sss.move("base", "S3")
    rospy.loginfo('Arm at outofview base at S3')
    sss.move("arm", "platform_centre")
    sss.move("base", "D1")
    rospy.loginfo('Arm at platform_centre base at D1')
    sss.move("arm", "grasp_laying_mex")
    sss.move("base", "S1")
    rospy.loginfo('Arm at candle base at S1')
    sss.move("arm", "tower_right")
    sss.move("base", "S2")
    rospy.loginfo('Arm at tower_right base at S2')
    sss.move("arm", "zigzag/zigzag1")
    sss.move("base", "EXIT")
    rospy.loginfo('Arm at zigzag1 base at EXIT')

    rospy.spin()

if __name__ == '__main__':
    main()
    
#TODo:
#test arm configurations, make the change working! STA 1 etc still not working!!
# random base positions, perhaps by putting the predefined base positions in an array, and randomly select from that
# repeat experiment
