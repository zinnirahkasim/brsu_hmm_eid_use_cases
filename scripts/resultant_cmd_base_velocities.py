#!/usr/bin/env python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy
import math
#from std_msgs.msg import String
from std_msgs.msg import *
from geometry_msgs.msg import Twist


def callback(msg):
    rospy.loginfo("Received /cmd_vel message!")
    rospy.loginfo("Linear Components: [%f, %f, %f]"%(msg.linear.x, msg.linear.y, msg.linear.z))
    rospy.loginfo("Angular Components: [%f, %f, %f]"%(msg.angular.x, msg.angular.y, msg.angular.z))

    # Do velocity processing here:
    # Use the kinematics of your robot to map linear and angular velocities into motor commands

    linear_x=msg.linear.x
    linear_y=msg.linear.y
    
    sq_linear_x = math.pow(linear_x, 2)
    sq_linear_y = math.pow(linear_y, 2)
    resultant = math.sqrt((sq_linear_x+sq_linear_y))
    
    rospy.loginfo("resultant cmd velocity is: %f" %resultant)

    # Then set your wheel speeds (using wheel_left and wheel_right as examples)
    #wheel_left.set_speed(v_l)
    #wheel_right.set_speed(v_r)
    return resultant

#def talker(resultant):
#    pub = rospy.Publisher('resultant_cmd_base_velocity', Twist)
    #rospy.init_node('talker')
#    while not rospy.is_shutdown():
        #str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(str)
#        pub.publish(Twist(resultant))
#        rospy.sleep(1.0)

def listener():
    rospy.init_node('resultant_cmd_base_velocities', anonymous=True)
    res=rospy.Subscriber("cmd_vel", Twist, callback)
#    talker(res)
    rospy.spin()


if __name__ == '__main__':
    listener()