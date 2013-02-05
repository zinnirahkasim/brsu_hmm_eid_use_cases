#!/usr/bin/python

    #
    #
    #                                    Wall 1
    #                    ____1______________2______________3________
    #          Wall 7    ||  |              |              |    ||
    #                    ||__| Wall 8       | Wall 5       |_11_||
    #                                 A           B        |    || Wall 2
    #                      __                      wall 10 |_12_|| 
    #                    ||  | Wall 9       | Wall 4       |    ||
    #          Wall 6    ||__|______________|______________|____||
    #                        4            Wall 3           6
    #  
import sys
import roslib
roslib.load_manifest('kee_use_cases')

import rospy
import os
import random 
import yaml

def main():
    rospy.init_node('remove_object')
    
    rospy.delete_param("simulation/objects/")
    
    rospy.spin()

if __name__ == '__main__':
    main()