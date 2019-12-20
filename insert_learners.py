import kolibri
import django
django.setup()

# import all the helper functions
from helpers import *
from django.contrib.auth.hashers import *
import datetime
import uuid
import csv

import argparse

argParser = argparse.ArgumentParser()

argParser.add_argument('--file', '-f' ,help='File to import users from')

dataset_id=FacilityDataset.objects.first().id

def_facility = Facility.get_default_facility().id

def insert_users(input_file):
	with open(input_file) as f:
	    reader = csv.DictReader(f)
	    users = [r for r in reader]

	    for user in users:
	    	_morango_partition = "{dataset_id}:user-ro:{user_id}".format(dataset_id=dataset_id, user_id=user['id'])
	    	FacilityUser.objects.create(id=user['id'],full_name=user['full_name'],username=user['username'],password=make_password(user['username']),dataset_id=dataset_id,facility_id=def_facility,_morango_partition = _morango_partition, _morango_source_id = uuid.uuid4())
	    	print('Created user: {}'.format(user['full_name']))

if __name__ == '__main__':
	args = argParser.parse_args()
	if args.file:
		open_file = args.file
		insert_users(open_file)
