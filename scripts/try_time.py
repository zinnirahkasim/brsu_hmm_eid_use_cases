#!/usr/bin/env python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy
import math



if __name__ == '__main__':
    rospy.init_node('trytime', anonymous=True)
    
    duration = 4
    
    while not rospy.is_shutdown():
        try:
          now = rospy.Time.now()
          rospy.loginfo("Current time %f", now.secs)  
          rospy.loginfo("do this every %f seconds ", duration)
          
          if now.secs == 0:
              rospy.loginfo("call this once and break")
          else:
              diff = now.secs-then.secs
              rospy.loginfo("diff :%f ", diff)
          
          then = rospy.Time.now()
          rospy.loginfo("then time %f", then.secs)
          rospy.sleep(duration)
          #seconds = rospy.get_time()
          #rospy.loginfo("get time %f", seconds)
        except rospy.ROSInterruptException:
            pass