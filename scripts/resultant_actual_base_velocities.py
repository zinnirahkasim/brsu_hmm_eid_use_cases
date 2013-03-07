#!/usr/bin/env python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy
import math
#from std_msgs.msg import String
from std_msgs.msg import *
from nav_msgs.msg import Odometry


def callback(msg):
    rospy.loginfo("Received /odom message!")
    rospy.loginfo("Linear Components: [%f, %f, %f]"%(msg.twist.twist.linear.x, msg.twist.twist.linear.y, msg.twist.twist.linear.z))
    rospy.loginfo("Angular Components: [%f, %f, %f]"%(msg.twist.twist.angular.x, msg.twist.twist.angular.y, msg.twist.twist.angular.z))

    # Do velocity processing here:
    # Use the kinematics of your robot to map linear and angular velocities into motor commands

    linear_x=msg.twist.twist.linear.x
    linear_y=msg.twist.twist.linear.y
    
    sq_linear_x = math.pow(linear_x, 2)
    sq_linear_y = math.pow(linear_y, 2)
    resultant = math.sqrt((sq_linear_x+sq_linear_y))
    
    rospy.loginfo("resultant cmd velocity is: %f" %resultant)

    # Then set your wheel speeds (using wheel_left and wheel_right as examples)
    #wheel_left.set_speed(v_l)
    #wheel_right.set_speed(v_r)
    return resultant

#def talker(resultant):
#    pub = rospy.Publisher('resultant_actual_base_velocity', Float64 )
    #rospy.init_node('talker')
#    while not rospy.is_shutdown():
#        pub.publish(Float64(resultant))
#        rospy.sleep(1.0)

def listener():
    rospy.init_node('resultant_actual_base_velocities', anonymous=True)
    res=rospy.Subscriber("odom", Odometry, callback)
    talker(res)
    rospy.spin()


if __name__ == '__main__':
    listener()