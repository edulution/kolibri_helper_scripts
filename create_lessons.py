# import kolibri and django to ensure the script runs in kolibri shell
import kolibri
import django
django.setup()

# import other libraries required
import os
import sys
import random

import datetime
from django.utils import timezone
from django.db import connection

# import kolibri content models
from kolibri.core.content.models import *

# import kolibri auth models
from kolibri.core.auth.models import *

# import kolibri lessons models
from kolibri.core.lessons.models import *

# import kolibri exams models
from kolibri.core.exams.models import *

from django.contrib.auth.hashers import *
import uuid


# helper function to delete all the lessons created for a class
def delete_all_lessons_for_class(classroomname,facilityname=None):
	facility_for_class = get_facility_or_default(facilityname)

	class_exists = Classroom.objects.filter(name = classroomname, parent = facility_for_class.id).exists()
	if class_exists:
		# if the class exists, delete all the lessons that were created for that class
		class_obj = Classroom.objects.get(name = classroomname, parent = facility_for_class)

		# print out a count of the number of lessons found
		print('{} Lessons found in class {}'.format(Lesson.objects.filter(collection = class_obj).count(),classroomname))

		# delete all the lessons found for that class
		Lesson.objects.filter(collection = class_obj).delete()
		print('Lessons successfully deleted')
	else:
		raise ValueError('There is no Class called {} in Facility {}. No Lessons were deleted'.format(classroomname,facility_for_class))
		sys.exit()


# Helper function to check if a facility exists or get the default facility
def get_facility_or_default(facilityname=None):
	# check if facilityname argument was passed in
	if facilityname:
		#if it was passed in
		# check if the facility requested exists
		facility_exists = Facility.objects.filter(name = facilityname).exists()
		# if the facility exists, store a reference to the object in the chosen_facility variable
		if facility_exists:
			chosen_facility = Facility.objects.get(name = facilityname)
			# inform the user which facility has been chosen
			print('Using Facility: {}'.format(str(chosen_facility.name)))
		else:
			 # if the facility does not exist, raise a value error and terminate the script
			raise ValueError('There is no Facility called {}'.format(facilityname))
			sys.exit()
	else:
		# if the facilityname argument was not passed in, choose the default facility
		chosen_facility = Facility.get_default_facility()
		# inform the user which facility has been chosen
		print('Using Default Facility: {}'.format(str(chosen_facility.name)))

	# return chosen facility
	return chosen_facility


# helper function to create a classroom object in the a facility if it does not exist
# creates the object in the default facility if no facility passed in
# returns a reference to the object created
def get_or_create_classroom(classroomname, facilityname=None):

	# get the facility passed in or the default facility
	facility_for_class = get_facility_or_default(facilityname)

	# filter the collections objects to check if a class with the name passed in already exists
	# get a boolean of whether found or not
	class_exists = Classroom.objects.filter(name = classroomname, parent = facility_for_class.id).exists()
	if class_exists:
		# if the class already exists return a reference of the object
		print('Class {} already exists in Facility {}'.format(classroomname, facility_for_class.name))
		class_obj = Classroom.objects.get(name = classroomname, parent = facility_for_class)
	else:
		print('Creating Class {} in Facility {}'.format(classroomname, facility_for_class.name))
		class_obj = Classroom.objects.create(name = classroomname,parent = facility_for_class)

	# return the ClassRoom object that was fetched or created
	return class_obj


# creates 1 lesson for each topic in each channel having the module passed in (module specified in channel_module table)
# e.g create_lessons('numeracy','a1') will create 1 lesson for each topic in each numeracy channel
def create_lessons(modulename,classroomname,facilityname=None):
	
	# set the seed that will be used to generate the sequence of lesson_ids
	seed = random.randint(1,100)
	
	# get or create the class to create the lessons for
	# store a reference to the classroom object if it is created
	class_for_lessons = get_or_create_classroom(classroomname,facilityname)

	# get a list of the admin and coach accounts on the device
	admins = FacilityUser.objects.raw("select * from kolibriauth_facilityuser where id in (select user_id from kolibriauth_role where kind in ('admin','coach'))")

	# if there is no admin or coach account on the device
	# raise an error and terminate the script
	if len(list(admins))==0:
		raise ValueError('There is no Admin or Coach account on the device. Cannot create lessons without an Admin or Coach account ')
		sys.exit()
	else:
		# if admin accounts exist, choose the first one and use it to create and assign the lessons
		admin_for_lessons = admins[0]


	#get all channels with the module passed in
	channels = ChannelMetadata.objects.raw("select * from content_channelmetadata where id in (select channel_id from channel_module where module = %s)", [modulename.lower()])

	# get a list of all the channel ids for the channels in the above query
	channel_ids = [channel.id for channel in channels]

	# if there are no channel_ids, then there are no channels that have the module requested
	# raise an error and terminate the script
	if len(channel_ids)==0:
		raise ValueError('There are no channels with a Module called {}. Cannot create lessons without channels '.format(modulename))
		sys.exit()

	# loop through the channels with the module passed in	
	for channel_id in channel_ids:
		# get the channel name for use in the inner loop
		channel_name = str(ChannelMetadata.objects.get(id = channel_id).name)

		# channels are found in topics but have no parent_id and id == parent_id
		# get all topics by getting all contentnodes of type topic which fulfil criteria above
		topics = ContentNode.objects.filter(kind = 'topic', parent_id = channel_id).exclude(parent_id__isnull = True).order_by('sort_order')


		# get contentnode_ids of all the topics as an array
		topic_ids = [topic.id for topic in topics]  

		# begin looping through topics
		for topic_id in topic_ids:
			# create the title for the lesson using the  title of the topic + the channel name
			lesson_title = str(ContentNode.objects.get(id = topic_id).title)+' - '+channel_name

			# lesson titles have a constraint of 50 characters
			# if this is exceeded, remove the difference from the topic title
			if len(lesson_title) > 50:
				diff_len = len(lesson_title) - 50
				lesson_title = str(ContentNode.objects.get(id = topic_id).title[:-diff_len])+' - '+channel_name

			# instantiate a new lesson object for the topic
			# title, collection and created by are needed to instantiate a lesson object. Other attributes can be set later
			# set the title of the lesson as the title of the topic + the channel name
			lesson_for_topic = Lesson.objects.create(id = uuid.uuid1(node=None, clock_seq=seed), title = lesson_title, collection = class_for_lessons, created_by = admin_for_lessons, _morango_source_id = uuid.uuid4())

			# get the child nodes of the topic
			child_nodes = ContentNode.objects.filter(parent_id = topic_id)

			# create an array of the resources for the lesson
			# structure of content resource in a lesson
			# {
			#   contentnode_id: string,
			#   content_id: string,
			#   channel_id: string
			# }
			lesson_for_topic.resources = [{'contentnode_id': node.id ,'content_id': node.content_id,'channel_id': node.channel_id} for node in child_nodes]

			# set the morango partition the lesson
			lesson_for_topic._morango_partition	= lesson_for_topic.calculate_partition() 		

			# save the object
			lesson_for_topic.save()

			# inform the user that the lesson has been created
			print('Created Lesson {} with {} resources'.format(lesson_title,len(lesson_for_topic.resources)))
