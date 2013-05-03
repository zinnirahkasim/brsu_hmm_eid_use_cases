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
roslib.load_manifest('brsu_hmm_eid_use_cases')

import rospy
import os
import random 
import yaml

from gazebo.srv import *
from geometry_msgs.msg import *
import tf.transformations as tft


class set_param_for_new_object:
    def __init__(self, amount):
        self.x = random.uniform(0, 1.52)
        self.y = random.uniform(0, -1.22)
        self.amount=amount
        print self.x
        print self.y
        print self.amount
        
    def write_yaml_files(self):
        #amount = raw_input("How many objects would you like to spawn? ")
        new_obj_yaml_file = open('/home/zinnirah/ros/workspace/kee_use_cases/objects/obj.yaml', 'w')
        for i in range(self.amount):
            #self.x = random.uniform(-1.52, 1.52)
            #self.y = random.uniform(1.22, -1.22)
            self.x = random.uniform(-1.52, 1.52)
            self.y = random.uniform(-1, 1)  
            object_details = {'box_'+str(i):{'object_type': 'box_1', 'model_type': 'urdf', 'position': [self.x, self.y, 0.33], 'orientation': [0, 0, 0]}}
            yaml.dump(object_details,new_obj_yaml_file)
        
        new_obj_yaml_file.close()

    def set_parameter(self):
        read_yaml_file = open('/home/zinnirah/ros/workspace/kee_use_cases/objects/obj.yaml', 'r')
        rospy.set_param("/simulation/random_objects/", yaml.load(read_yaml_file))
        print yaml.load(read_yaml_file)
        read_yaml_file.close()
     
#if __name__ == "__main__":
def main():
    rospy.init_node('add_object_randomly')    
    ### wait for gazebo world being loaded
    #rospy.loginfo("Wait for service <</gazebo/get_world_properties>>")
    #rospy.wait_for_service('/gazebo/get_world_properties', 300)
    
    #world_loaded = False
    #while not world_loaded:    
    #    srv_world_infos = rospy.ServiceProxy('/gazebo/get_world_properties', GetWorldProperties)
    
    #    try:
    #        req = GetWorldPropertiesRequest()
    #        res = srv_world_infos(req)
    #        
    #        for item in res.model_names:
    #            if item == 'arena':
    #                world_loaded = True
    #                break
    #    except rospy.ServiceException, e:
    #        print "Service call <</gazebo/get_world_properties>> failed: %s"%e
    #    
    #    rospy.sleep(1)
        
    #rospy.loginfo("Arena loaded successfully. Start loading objects ...")
    
    # get object information
    amount=input("Please enter the amount of objects you would like to spawn: ")
    sp = set_param_for_new_object(amount)
    sp.write_yaml_files()
    sp.set_parameter()
        
    if rospy.has_param('/simulation/random_objects/'):
        print "yay!"
    

    
    param_obj_preffix = '/simulation/random_objects/'
    object_names = rospy.get_param(param_obj_preffix)
    #rospy.get_param(param_name, default)
    for obj_name in object_names:

        model_type = rospy.get_param(param_obj_preffix + "/" + obj_name + "/model_type")
        object_type = rospy.get_param(param_obj_preffix + "/" + obj_name + "/object_type")
        orientation = rospy.get_param(param_obj_preffix + "/" + obj_name + "/orientation")
        position = rospy.get_param(param_obj_preffix + "/" + obj_name + "/position")
        
        # convert rpy to quaternion for Pose message
        quaternion = tft.quaternion_from_euler(orientation[0], orientation[1], orientation[2])

        object_pose = Pose()
        object_pose.position.x = float(position[0])
        object_pose.position.y = float(position[1])
        object_pose.position.z = float(position[2])
        object_pose.orientation.x = quaternion[0]
        object_pose.orientation.y = quaternion[1]
        object_pose.orientation.z = quaternion[2]
        object_pose.orientation.w = quaternion[3]

        file_localition = roslib.packages.get_pkg_dir('kee_use_cases') + '/objects/' + object_type + '.' + model_type

        # call gazebo service to spawn model (see http://ros.org/wiki/gazebo)
        if model_type == "urdf":
            srv_spawn_model = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
            file_xml = open(file_localition)
            xml_string=file_xml.read()

        elif model_type == "urdf.xacro":
            p = os.popen("rosrun xacro xacro.py " + file_localition)
            xml_string = p.read()   
            p.close()
            srv_spawn_model = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)

        elif model_type == "model":
            srv_spawn_model = rospy.ServiceProxy('/gazebo/spawn_gazebo_model', SpawnModel)
            file_xml = open(file_localition)
            xml_string=file_xml.read()
        else:
            print 'Error: Model type not know. model_type = ' + model_type
            sys.exit()


        req = SpawnModelRequest()
        req.model_name = obj_name # model name from command line input
        req.model_xml = xml_string
        req.initial_pose = object_pose

        res = srv_spawn_model(req)
    
        # evaluate response
        if res.success == True:
            print " %s model spawned succesfully. status message = "% object + res.status_message 
        else:
            print "Error: model %s not spawn. error message = "% object + res.status_message
	
	rospy.spin()

if __name__ == '__main__':
    main()

#TODO:
#Add random objects
#Add more objects that will give more effects (like a stick))