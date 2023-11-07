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

from kolibri.core.auth.models import (
    Facility,
    FacilityDataset,
    FacilityUser,
)  # noqa E402

# Initalize argparse and define command line args that can be passed to this module
argParser = argparse.ArgumentParser()
argParser.add_argument("--file", "-f", help="File to create users from")

argParser.add_argument(
    "--centre",
    "-c",
    help="Name of Facility( centre_id) in the case of multiple facilities on 1 device",
)


# Get the name of the default facility on the device
# used as the default value in case facility is not passed in
def_facility = str(Facility.get_default_facility().name)


def validate_gender(gender):
    return len(gender) == 1 and gender in ["M", "F"]


def validate_birth_year(birth_year):
    return birth_year.isdigit() and len(birth_year) == 4 and birth_year >= 1900


def create_users(input_file, facility=def_facility):
    """Function to create new users from a csv file
    The file is expected to have coolumns full_name and username. All other columns are ignored
    The resulting users will have password == username

    Args:
        input_file (string): Path to the csv file containing the users
        facility (string): Name of the facility in which to create the users(default facility if not specified)

    Returns:
        None
    """

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
        print_colored(
            "Error: Facility with the name {} does not exist".format(facility),
            colors.fg.red,
        )
        # exit in an error state
        sys.exit("Learners were not created successfully. Check the error(s) above")

    # Use csv dictreader to get the contents of the file
    with open(input_file) as f:
        reader = csv.DictReader(f)
        users = [r for r in reader]

        # Loop through the list of users read from the input file
        for user in users:
            user_exists = FacilityUser.objects.filter(
                username=user["username"], facility_id=facility_id
            ).exists()
            if user_exists:
                # if a user with the same username already exists in the facility
                # raise a value error and terminate the script
                raise ValueError(
                    print_colored(
                        "Duplicate username. There is already a user called {}".format(
                            user["username"]
                        ),
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

            elif not validate_birth_year(user["gender"]):
                # check if birth_year is a digit or lenght is not egual to 4
                raise ValueError(
                    "Invalid birth year. Please use a 4-digit integer. {}".format(
                        user["username"],
                        colors.fg.red,
                    )
                )
                sys.exit()

            else:
                # Create the user
                # Generate a new user_id
                new_user_id = uuid.uuid4()

                # Use the new user_id and the dataset_id to generate the morango partition
                _morango_partition = "{dataset_id}:user-ro:{user_id}".format(
                    dataset_id=dataset_id, user_id=new_user_id
                )

                # Create the new FacilityUser object
                FacilityUser.objects.create(
                    id=new_user_id,
                    full_name=user["full_name"],
                    username=user["username"],
                    gender=user["gender"],
                    birth_year=user["birth_year"],
                    password=make_password(user["username"]),
                    dataset_id=dataset_id,
                    facility_id=facility_id,
                    _morango_partition=_morango_partition,
                    _morango_source_id=uuid.uuid4(),
                )

                # Print out the full name of the user that has been created
                print_colored(
                    "Created user: {} in Facility {}".format(
                        user["full_name"], str(facility_obj.name)
                    ),
                    colors.fg.yellow,
                )

                # Increment the number of users created by one
                num_created += 1

    # Print out the total number of users that were created
    if num_created == 0:
        # If not learners were created, something is wrong and there will be errors displayed in the console
        print_colored(
            "No learners were created. Kindly check the errors above",
            colors.fg.red,
        )
    else:
        print_colored(
            "{} user(s) were created".format(num_created),
            colors.fg.lightgreen,
        )


# Main function called when script is run
if __name__ == "__main__":
    args = argParser.parse_args()
    # If the file is supplied and facility is not supplied
    # Create the users on the default facility
    if args.file and not (args.centre):
        open_file = args.file
        create_users(open_file)

    # If both the file and the facility are supplied
    # Create the users in the facility supplied
    elif args.file and args.centre:
        facility = args.centre
        open_file = args.file
        create_users(open_file, facility)

    # If neither the file nor the facility are passed in, stop the script in an error state
    else:
        sys.exit(
            "No arguments passed in. Please pass in the path to the file and centre_id (optional)"
        )
