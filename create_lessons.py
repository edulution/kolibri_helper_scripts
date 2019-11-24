# import kolibri and django to ensure the script runs in kolibri shell
import kolibri
import django
django.setup()

# import other libraries required
import os
import sys

import datetime
from django.utils import timezone
from django.db import connection

# import kolibri auth models
from kolibri.core.auth.models import *

# import kolibri lessons models
from kolibri.core.lessons.models import *

# import kolibri exams models
from kolibri.core.exams.models import *

from django.contrib.auth.hashers import *
import uuid


# helper function to create a classroom object in the a facility if it does not exist
# creates the object in the default facility if no facility passed in
# returns a reference to the object created
def get_or_create_classroom(classroomname, facilityname=None):
	# check if facilityname argument was passed in
	if facilityname:
		#if it was passed in
		# check if the facility requested exists
		facility_exists = Facility.objects.filter(name = facilityname).exists()
		# if the facility exists, store a reference to the object in the facility_for_class variable
		if facility_exists:
			facility_for_class = Facility.objects.get(name = facilityname)
			# inform the user which facility will be used to create the class
			print('Using Facility: {}'.format(str(facility_for_class.name)))
		else:
			 # if the facility does not exist, raise a value error and terminate the script
			raise ValueError('There is no Facility called {}. Please the Facility before creating Classes in it'.format(facilityname))
			sys.exit()

	else:
	# if the facilityname argument was not passed in, use the default facility as the place to create the class
		facility_for_class = Facility.get_default_facility()
		# inform the user that the default facility will be used when creating the classs
		print('Using Default Facility: {}'.format(str(facility_for_class.name)))


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


# def create_lessons():
# 	#get all channels
# 	channels = ChannelMetadata.objects.all()

# 	# channels are found in topics but have no parent_id and id == parent_id
# 	# get all topics by getting all contentnodes of type topic which fulfil criteria above
# 	topics = ContentNode.objects.filter(kind = 'topic').exclude(parent__id_isnull = TRUE)


# 	# get contentnode_ids of all the topics as an array
# 	topics_ids = [topic.id for topic in topics]  

# 	# begin looping through topics
# 	for topic_id in topic_ids:
# 		nodes_in_topic = ContentNode.objects.filter(parent_id = topic_id)


		# {
		#   contentnode_id: string,
		#   content_id: string,
		#   channel_id: string
		# }




	

	
