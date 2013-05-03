#!/usr/bin/python
import roslib; roslib.load_manifest('brsu_hmm_eid_use_cases')
import rospy

import smach
import smach_ros
import arm_navigation_msgs.msg


import random 
import yaml


from simple_script_server import *
sss = simple_script_server()
# scenario specific states
#from fetch_and_carry_demo_states import *

        
                
def main():
    rospy.init_node('stretch_arm2')
    
    rospy.sleep(6)
    sss.move("arm", "pregrasp_laying")
    rospy.sleep(6)
    sss.move("base", "S1")
    sss.move("base", "S2")
    sss.move("base", "S3")
    sss.move("base", "D1")
    sss.move("base", "S1")
    sss.move("base", "D2")
    sss.move("base", "S2")
    sss.move("base", "D1")
    sss.move("base", "S1")
    sss.move("base", "S2")
    sss.move("base", "D2")
    sss.move("base", "EXIT")
    rospy.spin()

if __name__ == '__main__':
    main()
    
#TODo:
#test arm configurations, make the change working! STA 1 etc still not working!!
# random base positions, perhaps by putting the predefined base positions in an array, and randomly select from that
# repeat experiment
