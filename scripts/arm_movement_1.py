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

                
def main():
    
    
    rospy.sleep(5)
    
    
#===============================================================================
#    sss.move("arm", "candle")
#    
#    
#    rospy.sleep(5)
#    sss.move("arm", "line/line_1")
#    
#    
#    rospy.sleep(5)
#    sss.move("arm", "out_of_view")
#    
#    
#    rospy.sleep(5)
#    sss.move("arm", "line/line_2")
#    
#    
#    rospy.sleep(5)
#    sss.move("arm", "line/line_3")
#    
#    
#    rospy.sleep(5)
#    sss.move("arm", "platform_centre")
#    
#    
#    rospy.sleep(5)
#    sss.move("arm", "platform_intermediate")
#    
#    
#    rospy.sleep(5)
#    sss.move("arm", "platform_left")
# 
#    rospy.sleep(5)
#    sss.move("arm", "platform_right")
# 
#    
#    rospy.sleep(5)
#    sss.move("arm", "pregrasp_laying")
# 
#    
#    rospy.sleep(5)
#    sss.move("arm", "pregrasp_standing")
# 
#    
#    rospy.sleep(5)
#    sss.move("arm", "tower_left")
# 
#    
#    rospy.sleep(5)
#    sss.move("arm", "tower_right")
# 
#    
#    rospy.sleep(5)
#    sss.move("arm", "zigzag/zigzag_1")
# 
#    
#    rospy.sleep(5)
#    #sss.move("arm", "zigzag/zigzag_2")
#===============================================================================

    
    rospy.sleep(5)
    sss.move("arm", "zigzag/zigzag_3")

    rospy.loginfo("Last one!")
    
    rospy.sleep(5)


    #rospy.loginfo('Arm at home base at S1')
    #
    #sss.move("base", "S2")
    #rospy.loginfo('Arm at home base at S2')
    #
    #sss.move("base", "S3")
    #rospy.loginfo('Arm at outofview base at S3')
    #
    #sss.move("base", "D1")
    #rospy.loginfo('Arm at home base at D1')
    #sss.move("arm", "grasp_laying_mex")
    #sss.move("base", "D2")
    #rospy.loginfo('Arm at home base at S1')
    #
    #sss.move("base", "S2")
    #rospy.loginfo('Arm at home base at S2')
    #sss.move("arm", "zigzag/zigzag1")
    #sss.move("base", "EXIT")
    #rospy.loginfo('Arm at zigzag1 base at EXIT')

    #rospy.spin()

if __name__ == '__main__':
    rospy.init_node('stretch_arm')
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        try:
            main()
            r.sleep()
        except rospy.ROSInterruptException:
            pass
   
    
#TODo:
#test arm configurations, make the change working! STA 1 etc still not working!!
# random base positions, perhaps by putting the predefined base positions in an array, and randomly select from that
# repeat experiment
