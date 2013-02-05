#!/usr/bin/python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy

import smach
import smach_ros
import arm_navigation_msgs.msg

from simple_script_server import *
sss = simple_script_server()
# scenario specific states
#from fetch_and_carry_demo_states import *

def main():
    rospy.init_node('stretch_arm')
    
    #sss.move("base", "D1")
    sss.move("arm", "pregrasp_laying")
    sss.move("base", "D1")
    sss.move("arm", "line/line_1")
    sss.move("base", "S1")
    sss.move("arm", "zigzag/zigzag_1")
    sss.move("base", "D1")
    sss.move("arm", "zigzag/zigzag_1")
    sss.move("base", "D2")
    sss.move("base", "S1")
    sss.move("base", "D2")
    sss.move("base", "S3")
    
    rospy.spin()
    # smach_thread.stop()
    smach_viewer.stop()

if __name__ == '__main__':
    main()