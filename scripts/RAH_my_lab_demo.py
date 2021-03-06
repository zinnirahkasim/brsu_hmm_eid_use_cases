#!/usr/bin/python

#################################################################


import roslib
roslib.load_manifest('brsu_lab_demo')
import rospy
import smach
import smach_ros

import sys
sys.path.append("../../brsu_common_states_lab_demo/src")
from math import *

from simple_script_server import *
sss = simple_script_server()

from common_states_lab_demo import *

from std_msgs.msg import *
import brsu_srvs.srv

from common_statemachines_lab_demo import *

light_pub = rospy.Publisher('light_controller/command', ColorRGBA)

red_light = ColorRGBA()
red_light.r = 1.0
red_light.g = 0.0
red_light.b = 0.0
red_light.a = 0.1

green_light = ColorRGBA()
green_light.r = 0.0
green_light.g = 1.0
green_light.b = 0.0
green_light.a = 0.1
	
INTRODUCE = 'introduce'
LEARN_PERSON = 'learn_person'
FIND_PERSON = 'find_person'
IDENTIFY_PERSON = 'identify_person'
FOLLOW = 'follow_person'
GUIDE = 'guide'
MOVE_TO = 'move_to'
DETECT_OBJECT = 'detect_object'
POINT_TO_OBJECT = 'point_to_object'
GRASP = 'grasp'
CLEAN_TABLE = 'clean_table'
EXIT = 'exit'
PENDING = 'pending'
WEIGHT = 'weight'
RELEASE = 'release'
HANDOVER = 'handover'
CATEGORIZE_OBJECTS = 'categorize_objects'
CARRY_BOX = 'carry_box'

GPSR_PREFIX = 'gpsr_'

IT = "it"


class load_faces(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success','failed'])
		self.load_person_face = rospy.ServiceProxy('/brsu_face_recognition/load_person_face', brsu_srvs.srv.FaceName)

	def execute(self, userdata):
		rospy.wait_for_service('/brsu_face_recognition/load_person_face', 3)
		light_pub.publish(red_light)
		try:
			#self.load_person_face("nico")
			#self.load_person_face("fred")
			#self.load_person_face("jan")
			#self.load_person_face("sven")
			#self.load_person_face("azden")
			#self.load_person_face("rhama")
			return 'success'
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
			return 'failed'
		
		
class move_actuators_to_home_poses(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success'])

	def execute(self, userdata):
		sss.move("head","front_face")
		sss.move("torso","home")	
		sss.move("tray","down")

		return 'success'


class Speech_keyword():
	def __init__(self, keyword="", confidence=0.0):
		self.keyword = keyword
		self.confidence = confidence

# Command to execute contains action, object and location
class Speech_command():
	
	def __init__(self, the_action="", the_object="", the_location =""):
		self.speech_action = Speech_keyword(keyword=the_action)
		self.speech_object = Speech_keyword(keyword=the_object)
		self.speech_location = Speech_keyword(keyword=the_location)
	
		self.actions_with_object = [GRASP, CLEAN_TABLE, POINT_TO_OBJECT, DETECT_OBJECT]
		self.actions_with_location = [FIND_PERSON, DETECT_OBJECT, GRASP, CLEAN_TABLE, POINT_TO_OBJECT, HANDOVER, CATEGORIZE_OBJECTS]
	
	# create a speakable string representation	
	def createPhrase(self):
		phrase = self.speech_action.keyword
		#actions with object get it appended
		if self.speech_object.keyword != "" and self.speech_action.keyword in self.actions_with_object:
			#if Keyword is if, the "the" is obsolete
			if self.speech_object.keyword != IT:
				phrase = phrase + " the "
			phrase = phrase + self.speech_object.keyword
		if self.speech_location.keyword != "" and self.speech_action.keyword in self.actions_with_location:
			phrase = phrase + " in the " + self.speech_location.keyword
		if self.speech_location.keyword != "" and self.speech_action.keyword == MOVE_TO:
			phrase = phrase + " the " + self.speech_location.keyword
		return phrase


class detected_object():
	def __init__(self, new_name = "", new_object_grasp_position = [], new_object_grasp_base_position = ""):
		self.object_name = new_name
		self.object_grasp_position = new_object_grasp_position
		self.object_grasp_base_position = new_object_grasp_base_position
	
	
class Robot_state():
	
	def __init__(self):
		self.actual_location = ""
		self.object_in_hand = ""
		self.found_objects = []
	
	def grasped_object(self, object_name):
		#delete object from found ones
		for some_object in self.found_objects:
			if(some_object.object_name == object_name):
				self.found_objects.remove(some_object)
		self.object_in_hand = object_name
		
	def moved(self, pose):
		self.actual_location = pose
		
	def found_object(self, new_base_position, new_grasp_position, new_object_name, pose):		
		new_object = detected_object(new_name = new_object_name, new_object_grasp_position = new_grasp_position, new_object_grasp_base_position = new_base_position)
		self.found_objects.append(new_object)
		self.actual_location = pose
		
		
	def __str__(self):
		#print self.found_objects
		for item in self.found_objects:
			print "item_name: " + item.object_name
			print "bPose: " + item.object_grasp_base_position

		return "location: " + self.actual_location + " \nobject_in_hand: " + self.object_in_hand
		
	def handed_object_over(self):
		print "TODO"

class update_robot_state(smach.State):

	def __init__(self):
		smach.State.__init__(self, outcomes=['success'], 
						output_keys=['robot_state_out'],
						input_keys = ['robot_state_in', 'robot_position_in', 'object_name_in', 'executed_action_in', 'grasp_pose_in'])
	
	def execute(self, userdata):
		new_robot_state = Robot_state()
		new_robot_state.actual_location = userdata.robot_state_in.actual_location
		new_robot_state.object_in_hand = userdata.robot_state_in.object_in_hand
		new_robot_state.found_objects = userdata.robot_state_in.found_objects
				
		if(userdata.executed_action_in == MOVE_TO):
			new_robot_state.moved(userdata.robot_position_in)
		if(userdata.executed_action_in == GRASP):
			new_robot_state.grasped_object(userdata.object_name_in)
		if(userdata.executed_action_in == DETECT_OBJECT):
			new_robot_state.found_object(new_object_name = userdata.object_name_in, new_base_position = userdata.robot_position_in, new_grasp_position = userdata.grasp_pose_in, pose = userdata.robot_position_in)
			
		userdata.robot_state_out = new_robot_state
		return 'success'

class get_robot_state(smach.State):

	def __init__(self):
		smach.State.__init__(self, outcomes=['success'], 
						output_keys=['actual_location_out', 'object_in_hand_out', 'found_objects_out'],
						input_keys = ['robot_state_in'])
	
	def execute(self, userdata):
		userdata.actual_location_out = userdata.robot_state_in.actual_location
		userdata.object_in_hand_out = userdata.robot_state_in.object_in_hand
		userdata.found_objects_out = userdata.robot_state_in.found_objects
		
		return 'success'



# replaces a sequence in a given string with a given char set
class filter_from_string(smach.State):

	def __init__(self):
		smach.State.__init__(self, outcomes=['success'], input_keys=['string_to_filter_in', 'sequence_to_remove_in','replacement_in' ], output_keys=['result_string_out'])

	def execute(self, userdata):
		userdata.result_string_out = userdata.string_to_filter_in.replace(userdata.sequence_to_remove_in, userdata.replacement_in)
		return 'success'


class introduce(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success'])
	
	def execute(self, userdata):
		handle_base = sss.move("base", "living_room", False)
		SAY("Hello ladies and gentlemen. My name is Jenny. I am a Care O bot 3 robot.")
		sss.sleep(1)
		SAY("I live at the bonn rhein sieg university in sankt augustin. I have my own appartment in the RoboCup lab. I am a member of the b i t bots team.")
		handle_base.wait()
		
		handle_arm = sss.move("arm", "folded-to-look_at_table" ,False)
		SAY("I am designed to be an autonomous domestic service robot. This means that I can help you with your household chores.")
		
		sss.sleep(1)
		SAY("I am equipped with an omnidirectional base, a 7 degree of freedom arm and a gripper.")
		handle_arm.wait()
		handle_base = sss.move("base", "second_intro", False)
		SAY("My base is omnidirectional which allows me to move forwards, backwards, sideways and even turn at the same time.")
		sss.sleep(3)
		handle_head = sss.move("head", "back", False)
		SAY("I can see with my color cameras and 3 d sensor. I can use them to detect objects and people. Currently I'm also learning to read.")
		handle_head.wait()
		handle_head = sss.move("head", "front", False)
		handle_head.wait()
		
		handle_tray = sss.move("tray","up",False)
		sss.sleep(2)
		SAY("With my tray I can hand over objects.")
		handle_tray.wait()
		
		
		#sss.move("sdh","cylopen")
		handle_arm = sss.move("arm", "look_at_table-to-folded", False)
		SAY("I'm able to reach positions on my front and backside with my arm. If you need a hand carrying things, I can lift up to 7 kilos.")
		sss.sleep(2)
		#sss.move("sdh","cylclosed")
		handle_arm.wait()
		
		handle_tray = sss.move("tray","down",False)
		
		handle_torso = sss.move("torso","nod",False)		
		handle_torso.wait()
		
		handle_base.wait()
		#SAY("Guys, do you need anything now or shall I return to my room?")
		handle_tray.wait()
		return 'success'


# takes any phrase and returns success if something understood. all understood keywords are in the userdata
class wait_for_arbitrary_phrase(smach.State):

	def __init__(self):
		smach.State.__init__(self, outcomes=['success','not_understood'], 
									output_keys=['keyword_list_out', 'confidence_list_out'])
		self.get_last_recognized_speech = rospy.ServiceProxy('/brsu_speech_recognition/get_last_recognized_speech', brsu_srvs.srv.GetLastRecognizedSpeech)
	
	def execute(self, userdata):
		# wait for the command
		light_pub.publish(green_light)
		rospy.wait_for_service('/brsu_speech_recognition/get_last_recognized_speech', 3)
		res = self.get_last_recognized_speech()
		
		if res.keyword.strip() != "no_speech" and res.keyword.strip() != "not_understood":
			userdata.keyword_list_out = res.keyword_list
			userdata.confidence_list_out = list(res.confidence_list)
			light_pub.publish(red_light)
			return 'success'
		else:
			rospy.sleep(0.2)
			return 'not_understood'

# separates the understood phras into command / action / location 
class decompose_speech_phrase(smach.State):

	def __init__(self):
		smach.State.__init__(self, outcomes=['success','not_understood'], 
									input_keys=['keyword_list_in','confidence_list_in','previous_understood_action_list_in',
												'current_room_in'],
									output_keys=['understood_phrase_out', 'action_list_out']
									)
	
	def execute(self, userdata):
		speech_objects = rospy.get_param("/script_server/brsu_speech_objects")
		speech_objects.append('it') #count "it" as object	
		
		speech_locations = rospy.get_param("/script_server/brsu_speech_places")	
		#speech_locations = speech_locations + rospy.get_param("/script_server/brsu_speech_grasp_locations")	
			
		speech_actions = rospy.get_param("/script_server/brsu_speech_actions")
			
		words = userdata.keyword_list_in
		confidences = userdata.confidence_list_in
		
		print words
		
		#store the commands in
		speech_commands  = []
		#awful decomposition by many if's
		# As long as there are words available:
		# check if first word is an action
		# if yes, delete and check next word for object/location
		# if yes do this again for appropriate missing part
		while(words):
			c = Speech_command()
			
			#take first word (is always action and erase)
			if words[0] in speech_actions:
				c.speech_action = Speech_keyword(words[0], confidences[0])
				del words[0]
				del confidences[0]
				#if more words available and its a location, store it		
				if words and words[0] in speech_locations:
					c.speech_location = Speech_keyword(words[0], confidences[0])
					del words[0]						
					del confidences[0]
					#third may be a object -> store
					if words and words[0] in speech_objects:
						c.speech_object = Speech_keyword(words[0], confidences[0])
						del words[0]
						del confidences[0]
				#otherwise it might be object					
				elif words and words[0] in speech_objects:
					c.speech_object = Speech_keyword(words[0], confidences[0])
					del words[0]
					del confidences[0]
					#if more words available and its a location, store it		
					if words: 
						if words[0] in speech_locations:
							c.speech_location = Speech_keyword(words[0], confidences[0])
							del words[0]	
							del confidences[0]
				#Add the new command									
				speech_commands.append(c)
			else:
				return "not_understood"
					
		#check with confidence if previous understood or current shall be used
#		for i in range(len(userdata.previous_understood_action_list_in)):
#			# if actions differ, check the confidence
#			if userdata.previous_understood_action_list_in[i].speech_action.keyword != speech_commands[i].speech_action.keyword:
				# exchange with previous, if previous confidence was higher or confidence is the same (because previous was def. not understood)
#				if (userdata.previous_understood_action_list_in[i].speech_action.confidence - speech_commands[i].speech_action.confidence) > 0.001 :									
#					speech_commands[i].speech_action = userdata.previous_understood_action_list_in[i].speech_action
#					speech_commands[i].speech_location = userdata.previous_understood_action_list_in[i].speech_location
#					speech_commands[i].speech_object = userdata.previous_understood_action_list_in[i].speech_object
			#IF OBJECTS AND SO ARE THERE, DONT EXCHANGE THW WHOLE ACTION
			#actions are the same, check location and 
			#else:
			#	if userdata.previous_understood_action_list_in[i].speech_object.conidence > speech_commands[i].speech_object.confidence:
			#		speech_commands[i].speech_object = userdata.previous_understood_action_list_in[i].speech_object
			#	if userdata.previous_understood_action_list_in[i].speech_location.conidence > speech_commands[i].speech_location.confidence:
			#		speech_commands[i].speech_location = userdata.previous_understood_action_list_in[i].speech_location
		
		confirmation_phrase = ""
		for action in speech_commands:
			confirmation_phrase = confirmation_phrase + ", " + action.createPhrase()
											
		'''Many commands don't contain a location if e.g. the current room is Implicitly mentioned. For execution
		this is important -> add current room resp. last annouced room. Same for object
		This also handles phrases like "find the chips, grasp it" whre it implicitly referes to prev. item '''
		current_pose = userdata.current_room_in
		current_object = ""
		for action in speech_commands:
			if action.speech_location.keyword == "":
				action.speech_location.keyword = current_pose
				action.speech_location.confidence = 0.0
			else:
				current_pose = action.speech_location.keyword
			if action.speech_object.keyword == "" or action.speech_object.keyword == IT:
				action.speech_object.keyword = current_object
				action.speech_object.confidence = 0.0
			else:
				current_object = action.speech_object.keyword
		
		#Reverse actionlist since its used as a stack
		speech_commands.reverse()
		userdata.action_list_out = speech_commands
				
		userdata.understood_phrase_out = confirmation_phrase
		
		return 'success'


class execute_commands(smach.State):
	
	def __init__(self):
		smach.State.__init__(self, outcomes=['success', 'failed',PENDING, INTRODUCE, LEARN_PERSON, FIND_PERSON,
											 IDENTIFY_PERSON, FOLLOW, GUIDE, MOVE_TO, DETECT_OBJECT,
											 GRASP, CLEAN_TABLE, POINT_TO_OBJECT, EXIT, WEIGHT, RELEASE, HANDOVER, CATEGORIZE_OBJECTS, CARRY_BOX],
									input_keys=['actions_to_execute_in', 'robot_state_in', 'already_executed_actions_in'],
									output_keys=['actions_left_out', 'pose_out', 'object_out', 'already_executed_actions_out', 'current_action_out'])
	
	def execute(self, userdata):
		#if all actions done return success
		if(not userdata.actions_to_execute_in):
			return 'success'
		
		action_list = userdata.actions_to_execute_in	
					
		#pop current action from the list and execute
		action_to_execute = action_list.pop()
		
		#Store the  next action / transition
		result = ''
		#announce action and  decompose or return appropriate transition
		if action_to_execute.speech_action.keyword == INTRODUCE:
			# Move exactly to appropriate location if not already there
			if action_to_execute.speech_location.keyword != userdata.robot_state_in.actual_location:	
				action_list.append(action_to_execute)
				action_list.append(Speech_command(MOVE_TO, action_to_execute.speech_object.keyword, action_to_execute.speech_location.keyword))
				result = PENDING
			else:
				SAY("Please let me introduce myself")
				result = INTRODUCE
		elif action_to_execute.speech_action.keyword == LEARN_PERSON:
			# Move exactly to appropriate location if not already there
			if action_to_execute.speech_location.keyword != userdata.robot_state_in.actual_location:	
				action_list.append(action_to_execute)
				action_list.append(Speech_command(MOVE_TO, action_to_execute.speech_object.keyword, action_to_execute.speech_location.keyword))
				result = PENDING
			else:
				SAY("I'll learn a person now.")
				result = LEARN_PERSON
		elif action_to_execute.speech_action.keyword == FIND_PERSON:
			# Move exactly to appropriate location if not already there
			if action_to_execute.speech_location.keyword != userdata.robot_state_in.actual_location:	
				action_list.append(action_to_execute)
				action_list.append(Speech_command(MOVE_TO, action_to_execute.speech_object.keyword, action_to_execute.speech_location.keyword))
				result = PENDING
			else:
				SAY("I'm gonna find a person now.")
				result = FIND_PERSON	
		elif action_to_execute.speech_action.keyword == IDENTIFY_PERSON:
			# Move exactly to appropriate location if not already there
			if action_to_execute.speech_location.keyword != userdata.robot_state_in.actual_location:	
				action_list.append(action_to_execute)
				action_list.append(Speech_command(MOVE_TO, action_to_execute.speech_object.keyword, action_to_execute.speech_location.keyword))
				result = PENDING
			else:
				SAY("I will identify a person now. Please come close.")
				result = IDENTIFY_PERSON	
		elif action_to_execute.speech_action.keyword == FOLLOW:
				# Move exactly to appropriate location if not already there
			if action_to_execute.speech_location.keyword != userdata.robot_state_in.actual_location:	
				action_list.append(action_to_execute)
				action_list.append(Speech_command(MOVE_TO, action_to_execute.speech_object.keyword, action_to_execute.speech_location.keyword))
				result = PENDING
			else:
				result = FOLLOW		
		elif action_to_execute.speech_action.keyword == GUIDE:
			result = GUIDE		
		elif action_to_execute.speech_action.keyword == MOVE_TO:
			SAY("I'm moving to the " + action_to_execute.speech_location.keyword.replace(GPSR_PREFIX, ''))
			result =  MOVE_TO		
		elif action_to_execute.speech_action.keyword == DETECT_OBJECT:
			# check if we are in the same room (after find person we are not exactly in the room pose but person might be in front)
			if action_to_execute.speech_location.keyword not in userdata.robot_state_in.actual_location:	
				action_list.append(action_to_execute)
				action_list.append(Speech_command(MOVE_TO, action_to_execute.speech_object.keyword, action_to_execute.speech_location.keyword))
				result = PENDING
			else:
				SAY("I'll search the " + action_to_execute.speech_object.keyword)
				result =  DETECT_OBJECT		
		elif action_to_execute.speech_action.keyword == POINT_TO_OBJECT:
			# If object detected, grasp, otherwise find object!		
			is_object_found = False
			# check if we know the object pose already
			for item in userdata.robot_state_in.found_objects:
				#if the one request is there, it is known
				if item.object_name == action_to_execute.speech_object.keyword:
					is_object_found = True
			
			#if location of object is different than ours, put grasp action on the stack with location equal to the object location
			if (is_object_found):# and item.object_grasp_base_position != userdata.robot_state_in.actual_location):
				action_list.append(Speech_command(POINT_TO_OBJECT, action_to_execute.speech_object.keyword, item.object_grasp_base_position))                                                                                                                                                              
				action_list.append(Speech_command(MOVE_TO, action_to_execute.speech_object.keyword, item.object_grasp_base_position))         
				result = PENDING
			else:
				SAY("I'll show you the " + action_to_execute.speech_object.keyword + " from the " + action_to_execute.speech_location.keyword.replace(GPSR_PREFIX, ''))			
				result =  POINT_TO_OBJECT	
		elif action_to_execute.speech_action.keyword == GRASP:
			# If object detected, grasp, otherwise find object!		
			is_object_found = False
			# check if we know the object pose already
			for item in userdata.robot_state_in.found_objects:
				#if the one request is there, it is known
				if item.object_name == action_to_execute.speech_object.keyword:
					is_object_found = True
				
			#if location of object is different than ours, put grasp action on the stack with location equal to the object location
			if(is_object_found and item.object_grasp_base_position != userdata.robot_state_in.actual_location):
				action_list.append(Speech_command(GRASP, action_to_execute.speech_object.keyword, item.object_grasp_base_position))																					
				action_list.append(Speech_command(MOVE_TO, action_to_execute.speech_object.keyword, item.object_grasp_base_position))																	
				print "HAVE TO MOVE " + item.object_grasp_base_position
				result = PENDING
			else:
				SAY("I'll grasp the " + action_to_execute.speech_object.keyword + " from the " + action_to_execute.speech_location.keyword.replace(GPSR_PREFIX, ''))			
				result =  GRASP		
		elif action_to_execute.speech_action.keyword == CLEAN_TABLE:
			# If sponge detected, clean, otherwise find object!		
			is_object_found = False
			# check if we know the object pose already
			for item in userdata.robot_state_in.found_objects:
				#if the one request is there, it is known
				if item.object_name == action_to_execute.speech_object.keyword:
					is_object_found = True
				
			#if location of object is different than ours, put grasp action on the stack with location equal to the object location
			if(is_object_found and item.object_grasp_base_position != userdata.robot_state_in.actual_location):
				action_list.append(Speech_command(CLEAN_TABLE, action_to_execute.speech_object.keyword, item.object_grasp_base_position))																					
				action_list.append(Speech_command(MOVE_TO, action_to_execute.speech_object.keyword, item.object_grasp_base_position))																	
				print "HAVE TO MOVE " + item.object_grasp_base_position
				result = PENDING
			else:
				SAY("I'll clean the table in the " + action_to_execute.speech_location.keyword.replace(GPSR_PREFIX, ''))			
				result = CLEAN_TABLE	
			
		elif action_to_execute.speech_action.keyword == EXIT:
			SAY("I'll leave the arena now.")
			result = EXIT
		elif action_to_execute.speech_action.keyword == WEIGHT:
			SAY("I'll weigh a bottle now.")
			result = WEIGHT
		elif action_to_execute.speech_action.keyword == CATEGORIZE_OBJECTS:
			SAY("I will categorize the objects now.")
			result = CATEGORIZE_OBJECTS
		elif action_to_execute.speech_action.keyword == RELEASE:
			result = RELEASE
		elif action_to_execute.speech_action.keyword == CARRY_BOX:
			result = CARRY_BOX
		elif action_to_execute.speech_action.keyword == HANDOVER:
			# check if we are in the same room
			if action_to_execute.speech_location.keyword not in userdata.robot_state_in.actual_location:	
				action_list.append(action_to_execute)
				action_list.append(Speech_command(MOVE_TO, action_to_execute.speech_object.keyword, action_to_execute.speech_location.keyword))
				result = PENDING
			else:
				result = HANDOVER
		
		
		else:
			result = 'failed'
			
		# store pose and object in userdata
		userdata.pose_out = action_to_execute.speech_location.keyword
		userdata.object_out = action_to_execute.speech_object.keyword
		
		#return open actions for next execution (either all if a pseudo move to was used, or all minus the next executed one)
		userdata.actions_left_out = action_list
		
		#append next action to the already executed
		tmp = userdata.already_executed_actions_in
		tmp.append(action_to_execute)
		userdata.already_executed_actions_out = tmp
		
		userdata.current_action_out = result
		return result


class get_room_poses(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success'], 
					input_keys=['room_name', 'room_poses'],
					output_keys=['room_poses'])
									
	def execute(self, userdata):
		userdata.room_poses = []
		for i in range(1,5): #for poses living_room1 - living_room4
			pose = userdata.room_name + str(i)
			print pose
			userdata.room_poses.append(pose)
		
		sss.move("head", "front")
		return 'success'	
		
class move_to_exit(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['success'])

	def execute(self, userdata):
		SAY("Goodbye")
		sss.move("base","exit")
		return 'success'

# main
def main():
	rospy.init_node('gpsr1')

	# Create a SMACH state machine
	sm = smach.StateMachine(outcomes=['overall_success', 'overall_failed'])
	
	
	names_to_understand = rospy.get_param('/script_server/brsu_speech_names')
	speech_grammar_file = rospy.get_param('/SpeechGrammarFile')
	
	# TODO: Adapt for competiton######################################### 
	sm.userdata.pose = "living_room" 
	sm.userdata.robot_state = Robot_state()
	sm.userdata.robot_state.actual_location = sm.userdata.pose
	
	sm.userdata.person_pose = ""
	sm.userdata.commands_to_wait_for = ["stop_follow_me", "stop_guiding"]
	sm.userdata.keyword_list = []
	sm.userdata.confidence_list = []
	sm.userdata.understood_command = ""
	sm.userdata.action_list = []
	sm.userdata.action_object = ""
	sm.userdata.clean_object = "sponge"
	sm.userdata.person_name = ""
	sm.userdata.grasp_pose = ""
	sm.userdata.gpsr_prefix = GPSR_PREFIX
	sm.userdata.getit_prefix = 'gpsr_'
	sm.userdata.recognized_person_name = ""
	
	sm.userdata.search_persons_room_suffix = '' 
	sm.userdata.announce_phrase = ""
	sm.userdata.already_executed_actions = []
	sm.userdata.search_person_pose = ""
	sm.userdata.robot_state = Robot_state()
	sm.userdata.current_action = ""
	
	sm.userdata.underscore = "_"
	sm.userdata.space = " "
	sm.userdata.empty_string = ""
	
	sm.userdata.bottle_state = 0
	sm.userdata.force_x_with_bottle = 0
	sm.userdata.room_poses = []
	
	#COMPETITION TODO:
	#Adapt  speech locations + grammar
		#define 'speech_location' for each defined location
		#define gpsr_'speech_location'+i for each search pose -> can the gogetit be reused?
		#define gpsr_'speech_location_find_person'+i for each search pose -> can the who_is_who be reused?
		
	#Adapt  speech objects + grammar
	#Adapt  speech names + grammar
	# define pose initially (~line 252) with the room that is started
	
	# Open the container
	with sm:
		
		# init base
		mystate = smach.StateMachine.add('init_base', init_base(), transitions={'success':'init_torso', 'failed':'overall_failed'})

		# init torso
		smach.StateMachine.add('init_torso', init_torso(), transitions={'success':'init_manipulator', 'failed':'overall_failed'})
	
		# init manipulator
		smach.StateMachine.add('init_manipulator', init_manipulator(), transitions={'success':'load_faces', 'failed':'overall_failed'})
	
		
		# checklist
		smach.StateMachine.add('general_checklist', general_checklist(),  transitions={'success':'announce_ready'})
		
		# announce ready
		smach.StateMachine.add('announce_ready', announce_ready(), transitions={'success':'wait_for_start','failed':'overall_failed'})

		# wait for start
		smach.StateMachine.add('wait_for_start', wait_for_start(), transitions={'success':'approach_start', 'pending':'wait_for_start'})
		
		# enter arena output_keys=['pose']
		smach.StateMachine.add('enter_arena', enter_arena(), transitions={'success':'approach_start', 'failed':'overall_failed'})
		
		smach.StateMachine.add('approach_start', approach_pose("living_room"), transitions={'success':'init_speech', 'failed':'init_speech'})
		

		
		############################# Understanding phase ##############################
		# init speech
		smach.StateMachine.add('init_speech', init_speech(speech_grammar_file), transitions={'success':'move_actuators_to_home_poses', 'failed':'overall_failed'})
		
		smach.StateMachine.add('move_actuators_to_home_poses', move_actuators_to_home_poses(), transitions={'success':'request_commands'})
		
		# announce ready
		smach.StateMachine.add('request_commands',say_state("please state your command"), 
											transitions={'success':'wait_for_command'})	
		
		# wait for complex command
		smach.StateMachine.add('wait_for_command', wait_for_arbitrary_phrase(), 
							transitions={'success':'decompose_speech_phrase', 'not_understood':'wait_for_command'},
							remapping={'keyword_list_out':'keyword_list',
										'confidence_list_out':'confidence_list'})
	
		# decompose to a set of 3 actions / commands
		smach.StateMachine.add('decompose_speech_phrase', decompose_speech_phrase(), 
							transitions={'success':'acknowledge_phrase', 'not_understood':'please_repeat'},
							remapping={'keyword_list_in':'keyword_list', 
										'confidence_list_in':'confidence_list',
										'understood_phrase_out':'understood_command',
										'previous_understood_action_list_in':'action_list',
										'action_list_out':'action_list',
										'current_room_in':'pose'})
		
		# ask for repition
		smach.StateMachine.add('please_repeat', say_state("I didn't understand you"), 
									transitions={'success':'init_speech'})	
		
		#switch grammar to yes / no
		#smach.StateMachine.add('load_ack_grammar', init_speech("acknowledge_top_level.xml"), transitions={'success':'acknowledge_phrase', 'failed':'approach_start'})
		
		#acknowledge the command
		smach.StateMachine.add('acknowledge_phrase', acknowledge_command_with_loading_grammar(), 
						transitions={'yes':'execute_commands', 'no':'init_speech'},
						remapping={'understood_command':'understood_command'})
		
		
		##################### execution phase ######################
		smach.StateMachine.add('execute_commands', execute_commands(), 
						transitions={'success': 'approach_start',
									'failed' : 'approach_start',
									PENDING : 'execute_commands',
									INTRODUCE : 'introduce',
									LEARN_PERSON:'learn_person_sub',
									FIND_PERSON:'get_room_poses_for_person_finding',
									IDENTIFY_PERSON:'wait_for_person_to_recognize',
									FOLLOW : 'change_grammar_follow_me',
									GUIDE : 'change_grammar_guiding',
									MOVE_TO:'move_to_pose',
									DETECT_OBJECT:'search_object_sub',
									GRASP:'identify_object',
									CLEAN_TABLE:'identify_object_for_cleaning',
									POINT_TO_OBJECT:'identify_object_for_pointing',
									WEIGHT:'put_bottle_in_hand',
									CARRY_BOX: 'carry_beer_box',
									RELEASE:'release_object',
									HANDOVER:'deliver_object',
									CATEGORIZE_OBJECTS:'categorize_objects',
									EXIT:'leave_arena'},
						remapping={'actions_to_execute_in':'action_list', 
									'actions_left_out':'action_list',
									'already_executed_actions_in':'already_executed_actions',
									'already_executed_actions_out':'already_executed_actions',
									'robot_state_in' : 'robot_state',
									'pose_out' : 'pose',
									'object_out': 'action_object',
									'current_action_out':'current_action'})
		
		smach.StateMachine.add('introduce', introduce(), 
									transitions={'success':'execute_commands'})
		
		
		# guiding behavior
			# change grammar for guiding
		smach.StateMachine.add('change_grammar_guiding', init_speech("guide.xml"), transitions={'success':'init_guiding', 'failed':'execute_commands'})
		
			# init the guiding behavior	
		smach.StateMachine.add('init_guiding', init_guiding(), transitions={'success':'announce_guiding','failed':'execute_commands'})
			#say how to stop
		smach.StateMachine.add('announce_guiding', say_state("Please tell me to stop by saying stop guiding me"), 
						transitions={'success':'wait_for_guiding_stop_command'})	

			# wait for the stop command	
		smach.StateMachine.add('wait_for_guiding_stop_command', wait_for_command(), 
								transitions={'success':'confirm_stop_guiding'})
		
		smach.StateMachine.add('confirm_stop_guiding', acknowledge_command(), 
					transitions={'yes':'stop_guiding', 'no':'wait_for_guiding_stop_command'})
		
		smach.StateMachine.add('stop_guiding', stop_guiding(), 
					transitions={'success':'execute_commands', 'failed':'execute_commands'})
		
		#carry box sub state machine
		smach.StateMachine.add('carry_beer_box', carry_beer_box(), 
					transitions={'success':'execute_commands', 'failed':'execute_commands'})
		
		#move_to
		smach.StateMachine.add('move_to_pose', approach_pose(), transitions={'success':'update_robot_state', 'failed':'execute_commands'},
											remapping={'pose':'pose'})

		#detect object / find object
			#load the sub-statemachine
		sub_sm_search_object = sm_search_object()		
		smach.StateMachine.add('search_object_sub', sub_sm_search_object, 
								transitions={'success_search_object':'say_found_object', 'overall_failed':'restore_robot_state_after_find_object'}, #redo search otherwise its lost anyway
								remapping={'sm_search_object_grasp_pose_out':'grasp_pose',
											'sm_search_object_base_pose_out':'pose',
											'sm_search_object_room_to_search_in':'pose',
											'sm_search_object_room_prefix_in': 'getit_prefix',
											'sm_search_object_room_suffix_in': 'empty_string',
											'sm_search_object_object_to_search_in':'action_object'})
		
		smach.StateMachine.add('restore_robot_state_after_find_object', get_robot_state(), 
											transitions={'success':'execute_commands'},
											remapping={'actual_location_out':'pose',
														'robot_state_in':'robot_state'})	
				
		smach.StateMachine.add('say_found_object',say_state_dynamic("I found the ", ""), 
											transitions={'success':'update_robot_state'},
											remapping={'phrase_in':'action_object'})	
		
		#point to object
		smach.StateMachine.add('identify_object_for_pointing', find_object_moped(),
								transitions={'success':'point_to_object', # point to if found
											'failed':'execute_commands'}, # otherwise search again
								remapping={'grasp_position': 'grasp_pose', 'object_name': 'action_object'})	
			# point
		smach.StateMachine.add('point_to_object', point_to_object(),
								transitions={'success':'execute_commands',
											'failed':'execute_commands'},
								remapping={'grasp_position':'grasp_pose'})		
		
		#clean table
			# Detect Item if inital grasp didn't succeed	
		smach.StateMachine.add('identify_object_for_cleaning', find_object_moped(),
								transitions={'success':'clean_table', # grasp if found
											'failed':'execute_commands'}, # otherwise search again
								remapping={'grasp_position': 'grasp_pose', 'object_name': 'clean_object'})	
			# clean the table
		smach.StateMachine.add('clean_table', clean_table(),
								transitions={'success':'execute_commands', # ALTERNATIVE move_back_to_start 
											'failed':'execute_commands'},
								remapping={'grasp_position':'grasp_pose'})	
		
		#grasp
			# Detect Item if inital grasp didn't succeed	
		smach.StateMachine.add('identify_object', find_object_moped(),
								transitions={'success':'grasp_object', # grasp if found
											'failed':'execute_commands'}, # otherwise search again
								remapping={'grasp_position': 'grasp_pose', 'object_name': 'action_object'})	
			# grasp Item
		smach.StateMachine.add('grasp_object', grasp_object(),
								transitions={'success':'update_robot_state', # ALTERNATIVE move_back_to_start 
											'failed':'execute_commands',
											'retry':'identify_object'},
								remapping={'grasp_position':'grasp_pose'})	

		#release object
		smach.StateMachine.add('release_object', release_object(), transitions={'success':'update_robot_state', 'failed':'update_robot_state'})	


		#Weight Bottle
		smach.StateMachine.add('put_bottle_in_hand', put_object_in_hand(), transitions={'success':'weight_bottle', 'failed':'execute_commands'})	

		smach.StateMachine.add('weight_bottle', weight_bottle(), transitions={'success':'release_object', 'failed':'update_robot_state'}, 
																remapping={'bottle_state':'bottle_state','force_x_with_bottle':'force_x_with_bottle'})	
		
		
		# move back and deliver object after cmmands execution						
	#	smach.StateMachine.add('move_back_to_start', approach_pose("living_room"), transitions={'success':'deliver_object', 'failed':'deliver_object'})
		
		smach.StateMachine.add('deliver_object', hand_over_object(), transitions={'success':'update_robot_state', 'failed':'update_robot_state'})
		
		smach.StateMachine.add('categorize_objects', categorize_objects(), transitions={'success':'update_robot_state', 'failed':'update_robot_state'})			
		
		
		
		# after every movement, grasp, object_detection, the robot state is updated
		smach.StateMachine.add('update_robot_state', update_robot_state(), transitions={'success':'execute_commands'},
									remapping={'robot_position_in':'pose', 
										'object_name_in':'action_object',										
										'grasp_pose_in':'grasp_pose',
										'executed_action_in':'current_action',
										'robot_state_in':'robot_state',
										'robot_state_out':'robot_state'})
		
		#exit
		smach.StateMachine.add('leave_arena', move_to_exit(), transitions={'success':'overall_success'})

									
	# Create and start the introspection server
	sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
	sis.start()

	# Execute the state machine
	#rospy.sleep(5)
	outcome = sm.execute()
	
	# Wait for ctrl-c to stop the application
	rospy.spin()
	sis.stop()

if __name__ == '__main__':
	main()

