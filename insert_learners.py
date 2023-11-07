import kolibri  # noqa F401
import django

import sys
import uuid
import csv
import argparse
from colors import *
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


def validate_gender(gender):
    return len(gender) == 1 and gender in ["M", "F"]


def validate_birth_year(birth_year):
    return birth_year.isdigit() and len(birth_year) == 4 and int(birth_year) >= 1900


def generate_unique_username(original_username, facility_id, first_name):
    new_username = original_username
    count = 1

    while FacilityUser.objects.filter(
        username=new_username, facility_id=facility_id
    ).exists():
        new_username = "{}{}{}".format(
            original_username[0], first_name[count], original_username[1:]
        )
        count += 1

        if count > len(first_name):
            # Append a character from the first name to the username to make it unique
            final_count = 1
            new_username = "{}{}{}".format(
                original_username[0], first_name[1:final_count], original_username[1:]
            )
            count += 1

    return new_username


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
            final_username = ""
            username_exists = FacilityUser.objects.filter(
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
                        user["user_id"],
                        colors.fg.red,
                    )
                )
                sys.exit()

            elif not validate_gender(user["gender"]):
                # check if gender is a single character and is f or m
                raise ValueError(
                    "Invalid gender. Please use 'M' for male or 'F' for female. {}".format(
                        user["username"],
                        colors.fg.red,
                    )
                )
                sys.exit()

            elif not validate_birth_year(user["birth_year"]):
                # check if birth_year is a digit or lenght is not egual to 4
                raise ValueError(
                    "Invalid birth year. Please use a 4-digit integer. {}".format(
                        user["username"],
                        colors.fg.red,
                    )
                )
                sys.exit()

            elif username_exists:
                original_username = user["username"]
                first_name = user["full_name"].split()[0]
                final_username = generate_unique_username(
                    original_username, first_name, facility_id
                )
                print_colored(
                    "Duplicate username. There is already a user called {}. The new username is {}".format(
                        original_username, final_username
                    ),
                    colors.fg.yellow,
                )
            else:
                final_username = user["username"]
                # Generate the morango partition

            _morango_partition = "{dataset_id}:user-ro:{user_id}".format(
                dataset_id=dataset_id, user_id=user["user_id"]
            )

            # Create the user
            FacilityUser.objects.create(
                id=user["user_id"],
                full_name=user["full_name"],
                username=final_username,
                gender=user["gender"],
                birth_year=user["birth_year"],
                password=make_password(final_username),
                dataset_id=dataset_id,
                facility_id=facility_id,
                _morango_partition=_morango_partition,
                _morango_source_id=uuid.uuid4(),
            )
            print_colored(
                "Created user: {}".format(user["full_name"]),
                colors.fg.yellow,
            )
            # Increment num_inserted by 1
            num_inserted += 1

        # Print out the total number of users that were inserted
        if num_inserted == 0:
            # If not learners were inserted, something is wrong and there will be errors displayed in the console
            print_colored(
                "No learners were inserted. Kindly check the errors above",
                colors.fg.red,
            )
        else:
            print_colored(
                "{} user(s) were inserted".format(num_inserted),
                colors.fg.lightgreen,
            )


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
