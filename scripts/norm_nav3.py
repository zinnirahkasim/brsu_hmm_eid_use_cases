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

def main():
    rospy.init_node('norm_nav3')
    

    #sss.move("arm", "home")

    
    sss.move("base", "S3")

    
    #rospy.loginfo('Arm at candle base at S2')
    #sss.move("arm", "tower_right")
    #sss.move("base", "S2")
    #rospy.loginfo('Arm at tower_right base at S2')
    # sss.move("arm", "zigzag/zigzag1")
    #sss.move("base", "EXIT")
    #rospy.loginfo('Arm at zigzag1 base at EXIT')

    

if __name__ == '__main__':
    while not rospy.is_shutdown():
        try:
            main()
            rospy.sleep(1)
        except rospy.ROSInterruptException:
            pass
    
#TODo:
#test arm configurations, make the change working! STA 1 etc still not working!!
# random base positions, perhaps by putting the predefined base positions in an array, and randomly select from that
# repeat experiment
