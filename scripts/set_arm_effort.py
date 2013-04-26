#!/usr/bin/env python
import roslib; roslib.load_manifest('brsu_hmm_eid_use_cases')
import roslib.message 
import rospy

#from brics_actuator.msg import JointTorques
from brsu_hmm_eid_messages.msg import obs_arm_JointTorques

if __name__ == '__main__':
    rospy.init_node('set_arm_effort', anonymous=True)
    
    while not rospy.is_shutdown():
        try:
            pub = rospy.Publisher('/arm_controller/torque_command', obs_arm_JointTorques)
            #msg2send = JointTorques()
            #msg2send.poisonStamp.description = ""
            #msg2send.poisonStamp.originator = ""
            #msg2send.poisonStamp.qos = 1 
            #msg2send.torques = [5,5,5,5,5]
            msg2send = obs_arm_JointTorques()
            msg2send.header.stamp.secs = rospy.Time.now().secs
            msg2send.torques = [5,5,5,5,5]
            pub.publish(msg2send)
            rospy.loginfo("publishing...")
            rospy.sleep(1)
        except rospy.ROSInterruptException:
            pass