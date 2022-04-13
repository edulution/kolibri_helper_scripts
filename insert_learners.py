import kolibri  # noqa F401
import django

import sys
import uuid
import csv
import argparse
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist

django.setup()

from kolibri.core.auth.models import Facility, FacilityUser  # noqa F402

# Initalize argparse and define all of the arguments to this module
argParser = argparse.ArgumentParser()
argParser.add_argument(
    "--file",
    "-f",
    help="CSV file to import users from. Must contain the fields id,username,full_name",
)
argParser.add_argument(
    "--centre",
    "-c",
    help="Name of Facility( centre_id) in the case of multiple facilities on 1 device",
)


# get the name of the default facility on the device
def_facility = str(Facility.get_default_facility().name)


def insert_users(input_file, facility=def_facility):
    """Insert users into a Facility from a csv file.
    Fields expected in the csv file:
        user_id
        full_name
        username
    Generally used to recreate users that already existed before without generating new user_ids

        Args:
            input_file (string): Path to the input csv file
            facility (string): The name of the facility, default is the first facility that was created on a device

        Returns:
            None
    """

    # get a reference to the Facility with the name supplied and it's dataset_id
    try:
        facility_obj = Facility.objects.get(name=facility)

        facility_id = facility_obj.id
        dataset_id = facility_obj.dataset_id

        # catch the exception when the object does not exist
    except ObjectDoesNotExist:
        # print out the id that does not exist
        print("Error: Facility with the name {} does not exist".format(facility))
        # exit in an error state
        sys.exit("Learners were not inserted successfully. Check the error(s) above")
    with open(input_file) as f:
        reader = csv.DictReader(f)
        users = [r for r in reader]

        # Initialize num_inserted to 0
        num_inserted = 0

        for user in users:

            user_exists = FacilityUser.objects.filter(
                username=user["username"], facility_id=facility_id
            ).exists()
            user_id_exists = FacilityUser.objects.filter(
                id=user["user_id"], facility_id=facility_id
            ).exists()
            if user_id_exists:
                # if a user with the same user_id already exists in the facility
                # raise a value error and terminate the script
                raise ValueError(
                    "Duplicate user ID. There is already a user with ID {}".format(
                        user["user_id"]
                    )
                )
                sys.exit()
            elif user_exists:
                # if a user with the same username already exists in the facility
                # raise a value error and terminate the script
                raise ValueError(
                    "Duplicate username. There is already a user called {}".format(
                        user["username"]
                    )
                )
                sys.exit()
            else:
                # Generate the morango partition
                _morango_partition = "{dataset_id}:user-ro:{user_id}".format(
                    dataset_id=dataset_id, user_id=user["user_id"]
                )

                # Create the user
                FacilityUser.objects.create(
                    id=user["user_id"],
                    full_name=user["full_name"],
                    username=user["username"],
                    password=make_password(user["username"]),
                    dataset_id=dataset_id,
                    facility_id=facility_id,
                    _morango_partition=_morango_partition,
                    _morango_source_id=uuid.uuid4(),
                )
                print("Created user: {}".format(user["full_name"]))
            # Increment num_inserted by 1
            num_inserted += 1

        # Print out the total number of users that were inserted
        if num_inserted == 0:
            # If not learners were inserted, something is wrong and there will be errors displayed in the console
            print("No learners were inserted. Kindly check the errors above")
        else:
            print("{} user(s) were inserted".format(num_inserted))


if __name__ == "__main__":
    args = argParser.parse_args()
    if args.file and not (args.centre):
        open_file = args.file
        insert_users(open_file)

    elif args.file and args.centre:
        facility = args.centre
        open_file = args.file
        insert_users(open_file, facility)
    else:
        sys.exit(
            "No arguments passed in. Please pass in the path of the file and centre_id (optional)"
        )
