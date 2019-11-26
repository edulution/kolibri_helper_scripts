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


# helper function to create a learnergroup object in a classroom in a facility if it does not exist
# creates a classroom object with the name passed in if it does not exist
# creates the classroom object in the default facility if no facility passed in
# returns a reference to the learnergroup object created
def get_or_create_learnergroup(groupname,classroomname, facilityname=None):

	# get the facility passed in or the default facility
	facility_for_class = get_facility_or_default(facilityname)

	# get the classroom passed in or create it
	class_for_group = get_or_create_classroom(classroomname,facilityname)

	learnergroup_exists = LearnerGroup.objects.filter(name = groupname, parent = class_for_group).exists()
	if learnergroup_exists:
		# if the class already exists return a reference of the object
		print('Group {} already exists in Class {}'.format(groupname, str(class_for_group.name)))
		learnergroup_obj = LearnerGroup.objects.get(name = groupname, parent = class_for_group)
	else:
		print('Creating Group {} in Class {}'.format(groupname, str(class_for_group.name)))
		learnergroup_obj = LearnerGroup.objects.create(name = groupname, parent = class_for_group)

	return learnergroup_obj

