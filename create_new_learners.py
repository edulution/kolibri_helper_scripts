# Create new users from a csv file with the columns full name and username

import kolibri
import django
# import all the helper functions
from helpers import *
import datetime
import csv
import argparse

django.setup()

argParser = argparse.ArgumentParser()

argParser.add_argument('--file', '-f', help='File to create users from')

dataset_id = FacilityDataset.objects.first().id

def_facility = Facility.get_default_facility().id


def create_users(input_file):
    with open(input_file) as f:
        reader = csv.DictReader(f)
        users = [r for r in reader]

        for user in users:
            # generate a new user_id
            new_user_id = uuid.uuid4()

            # use the new user_id and the dataset_id to generate the morango partition
            _morango_partition = "{dataset_id}:user-ro:{user_id}".format(dataset_id=dataset_id, user_id=new_user_id)

            # create the new facilityuser object
            FacilityUser.objects.create(
                id=new_user_id,
                full_name=user['full_name'],
                username=user['username'],
                password=make_password(user['username']),
                dataset_id=dataset_id,
                facility_id=def_facility,
                _morango_partition=_morango_partition,
                _morango_source_id=uuid.uuid4())

            # print out the full name of the user that has been created
            print('Created user: {}'.format(user['full_name']))


if __name__ == '__main__':
    args = argParser.parse_args()
    if args.file:
        open_file = args.file
        create_users(open_file)
