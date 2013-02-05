#!/usr/bin/python
import roslib; roslib.load_manifest('kee_use_cases')
import rospy

import smach
import smach_ros

# generic states
from generic_basic_states import *
from generic_navigation_states import *
from generic_manipulation_states import *
from generic_state_machines import *

# scenario specific states
#from fetch_and_carry_demo_states import *

def main():
    rospy.init_node('stretch_arm')
    
    SM = smach.StateMachine(outcomes=['overall_failed', 'overall_success'])
    
    #world knowledge
     # world knowledge
    SM.userdata.base_pose_list = ["S3", "D1"]
    SM.userdata.base_pose_to_approach = -1; 
    SM.userdata.object_list = [];
                                            # x, y, z, roll, pitch, yaw
    SM.userdata.rear_platform_free_poses = ['platform_centre']
    SM.userdata.rear_platform_occupied_poses = []
    
    SM.userdata.obj_goal_configuration_poses = []
    
        # open the container
    with SM:
        # add states to the container
        
        smach.StateMachine.add('INIT_ROBOT', init_robot(),
            transitions={'succeeded':'SELECT_POSE_TO_APPROACH'})
        
        #stretch arm 
        smach.StateMachine.add('STRETCH ARM', move_arm("grasp_laying", do_blocking=false),
                               transitions={'succeeded':'MOVE_TO_GRASP_POSE'})
        
        smach.StateMachine.add('MOVE_TO_DESTINATION_POSE', approach_pose("D1"),
            transitions={'succeeded':'ADJUST_POSE_WRT_WORKSPACE', 
                        'failed':'overall_failed'})
        # place object at destination pose
        smach.StateMachine.add('MOVE_TO_DESTINATION_POSE', approach_pose("S2"),
            transitions={'succeeded':'ADJUST_POSE_WRT_WORKSPACE', 
                        'failed':'overall_failed'})
        
        smach.StateMachine.add('MOVE_TO_DESTINATION_POSE', approach_pose("D2"),
            transitions={'succeeded':'ADJUST_POSE_WRT_WORKSPACE', 
                        'failed':'overall_failed'})
        smach.StateMachine.add('MOVE_TO_DESTINATION_POSE', approach_pose("S1"),
            transitions={'succeeded':'ADJUST_POSE_WRT_WORKSPACE', 
                        'failed':'overall_failed'})
        
        smach.StateMachine.add('MOVE_TO_DESTINATION_POSE', approach_pose("D1"),
            transitions={'succeeded':'ADJUST_POSE_WRT_WORKSPACE', 
                        'failed':'overall_failed'})
        
        smach.StateMachine.add('MOVE_TO_DESTINATION_POSE', approach_pose("S3"),
            transitions={'succeeded':'ADJUST_POSE_WRT_WORKSPACE', 
                        'failed':'overall_failed'})
        
        smach.StateMachine.add('MOVE_TO_DESTINATION_POSE', approach_pose("D2"),
            transitions={'succeeded':'ADJUST_POSE_WRT_WORKSPACE', 
                        'failed':'overall_failed'})
                
        smach.StateMachine.add('MOVE_TO_EXIT', approach_pose("EXIT"),
            transitions={'succeeded':'overall_success', 
                        'failed':'overall_failed'})
              
            
    # Start SMACH viewer
    smach_viewer = smach_ros.IntrospectionServer('LALA', SM, 'LALA')
    smach_viewer.start()

    SM.execute()

    # stop SMACH viewer
    rospy.spin()
    # smach_thread.stop()
    smach_viewer.stop()

if __name__ == '__main__':
    main()