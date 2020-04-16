# Create new users from a csv file with the columns full name and username

import kolibri # noqa F401
import django
# import all the helper functions
import sys
import uuid
import csv
import argparse
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist

django.setup()

from kolibri.core.auth.models import Facility, FacilityDataset, FacilityUser # noqa E402

# Initalize argparse and define arguments that can be passed to this module
argParser = argparse.ArgumentParser()
argParser.add_argument(
    '--file',
    '-f',
    help='File to create users from')

argParser.add_argument(
    '--centre',
    '-c',
    help='Name of Facility( centre_id) in the case of multiple facilities on 1 device')


# Get the name of the default facility on the device
# used as the default value in case facility is not passed in
def_facility = str(Facility.get_default_facility().name)


def create_users(input_file, facility=def_facility):

    # Initialize variable for number of users created
    num_created = 0

    # Check if the Facility supplied exists
    try:
        # Attempt to get a reference to the Facility supplied if it exists
        facility_obj = Facility.objects.get(name=facility)

        facility_id = facility_obj.id
        dataset_id = facility_obj.dataset_id

    # Catch the exception when the Facility does not exist
    except ObjectDoesNotExist:
        # Print out the name of the Facility that does not exist and terminate the script
        print('Error: Facility with the name {} does not exist'.format(facility))
        # exit in an error state
        sys.exit('Learners were not created successfully. Check the error(s) above')

    with open(input_file) as f:
        reader = csv.DictReader(f)
        users = [r for r in reader]

        # Loop through the list of users read from the input file
        for user in users:

            user_exists = FacilityUser.objects.filter(username=user['username'], facility_id=facility_id).exists()
            if user_exists:
                # if a user with the same username already exists in the facility
                # raise a value error and terminate the script
                raise ValueError('Duplicate username. There is already a user called {}'.format(user['username']))
                sys.exit()
            else:
                # Create the user
                # Generate a new user_id
                new_user_id = uuid.uuid4()

                # Use the new user_id and the dataset_id to generate the morango partition
                _morango_partition = "{dataset_id}:user-ro:{user_id}".format(dataset_id=dataset_id, user_id=new_user_id)

                # Create the new FacilityUser object
                FacilityUser.objects.create(
                    id=new_user_id,
                    full_name=user['full_name'],
                    username=user['username'],
                    password=make_password(user['username']),
                    dataset_id=dataset_id,
                    facility_id=facility_id,
                    _morango_partition=_morango_partition,
                    _morango_source_id=uuid.uuid4())

                # Print out the full name of the user that has been created
                print('Created user: {} in Facility {}'.format(user['full_name'], str(facility_obj.name)))

                # Increment the number of users created by one
                num_created += 1

    # Print out the total number of users that were created
    if num_created == 0:
        # If not learners were created, something is wrong and there will be errors displayed in the console
        print('No learners were created. Kindly check the errors above')
    else:
        print('{} user(s) were created'.format(num_created))


if __name__ == '__main__':
    args = argParser.parse_args()
    if args.file and not(args.centre):
        open_file = args.file
        create_users(open_file)

    elif args.file and args.centre:
        facility = args.centre
        open_file = args.file
        create_users(open_file, facility)
