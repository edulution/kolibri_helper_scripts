import kolibri # noqa F401
import django

import sys
import uuid
import csv
import argparse
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist

django.setup()

from kolibri.core.auth.models import Facility, FacilityUser # noqa F402

# Initalize argparse and define all of the arguments to this module
argParser = argparse.ArgumentParser()
argParser.add_argument(
    '--file',
    '-f',
    help='CSV file to import users from. Must contain the fields id,username,full_name')
argParser.add_argument(
    '--centre',
    '-c',
    help='Name of Facility( centre_id) in the case of multiple facilities on 1 device')


# get the name of the default facility on the device
def_facility = str(Facility.get_default_facility().name)


def insert_users(input_file, facility=def_facility):
    # get a reference to the Facility with the name supplied and it's dataset_id
    try:
        facility_obj = Facility.objects.get(name=facility)

        facility_id = facility_obj.id
        dataset_id = facility_obj.dataset_id

        # catch the exception when the object does not exist
    except ObjectDoesNotExist:
        # print out the id that does not exist
        print('Error: Facility with the name {} does not exist'.format(facility))
        # exit in an error state
        sys.exit('Learners were not inserted successfully. Check the error(s) above')
    with open(input_file) as f:
        reader = csv.DictReader(f)
        users = [r for r in reader]

        for user in users:
            _morango_partition = "{dataset_id}:user-ro:{user_id}".format(dataset_id=dataset_id, user_id=user['id'])
            FacilityUser.objects.create(
                id=user['id'],
                full_name=user['full_name'],
                username=user['username'],
                password=make_password(user['username']),
                dataset_id=dataset_id,
                facility_id=facility_id,
                _morango_partition=_morango_partition,
                _morango_source_id=uuid.uuid4())
            print('Created user: {}'.format(user['full_name']))


if __name__ == '__main__':
    args = argParser.parse_args()
    if args.file and not(args.centre):
        open_file = args.file
        insert_users(open_file)

    elif args.file and args.centre:
        facility = args.centre
        open_file = args.file
        insert_users(open_file, facility)
    else:
        sys.exit('No arguments passed in. Please pass in the path of the file and centre_id (optional)')
