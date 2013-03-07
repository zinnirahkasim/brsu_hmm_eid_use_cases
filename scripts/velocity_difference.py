#!/usr/bin/env python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy
import math
#from std_msgs.msg import String
from std_msgs.msg import *
from nav_msgs.msg import Odometry


def callback_1(msg):
    rospy.loginfo("Received <<resultant_cmd_base_velocity>> message!")

def callback_2(msg):
    rospy.loginfo("Received <<resultant_actual_base_velocity>> message!")


#def talker(resultant):
#    pub = rospy.Publisher('resultant_actual_base_velocity', Float64 )
    #rospy.init_node('talker')
#    while not rospy.is_shutdown():
#        pub.publish(Float64(resultant))
#        rospy.sleep(1.0)

def listener():
    cmd_vel=rospy.Subscriber("resultant_cmd_base_velocity", Odometry, callback_1)
    act_vel=rospy.Subscriber("resultant_actual_base_velocity", Odometry, callback_2)
    difference = math.fabs(cmd_vel - act_vel)
    rospy.spin()
    
    return difference


if __name__ == '__main__':
    rospy.init_node('velocity_difference', anonymous=True)
    
    try:
        listener()
    except rospy.ROSInterruptException:
        pass