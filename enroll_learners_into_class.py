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
    Classroom,
    LearnerGroup,
    Membership,
)  # noqa E402

# Initalize argparse and define command line args that can be passed to this module
argParser = argparse.ArgumentParser()
argParser.add_argument("--file", "-f", help="File to create users from")

argParser.add_argument(
    "--centre",
    "-c",
    help="Name of Facility( centre_id) in the case of multiple facilities on 1 device",
)
argParser.add_argument(
    "--delete",
    "-d",
    action="store_true",
    default=False,
    help="Delete existing memberships for each user before memberships. The default value is False",
)

# Get the name of the default facility on the device
# used as the default value in case facility is not passed in
def_facility = str(Facility.get_default_facility().name)


def enroll_learners_into_class(
    input_file, facilityname=def_facility, delete_existing_memberships=False
):
    """Function to enroll learners into classes using a csv file
    The file is expected to have columns user_id, centre, and grade. All other columns are ignored
    The grade column represents the name of the classroom the learner should be enrolled into.
    It is assumed that the classrooms have already been created

    Args:
        input_file (string): Path to the csv file containing the users
        facility (string): Name of the facility which contains the classrooms(default facility if not specified)

    Returns:
        None
    """

    # Initialize variable for number of users created
    num_enrolled = 0

    # Check if the Facility supplied exists
    try:
        # Attempt to get a reference to the Facility supplied if it exists
        facility_obj = Facility.objects.get(name=facilityname)

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
        sys.exit("Learners were not enrolled successfully. Check the error(s) above")

    # Use csv dictreader to get the contents of the file
    with open(input_file) as f:
        reader = csv.DictReader(f)
        users = [r for r in reader]

        # Loop through the list of users read from the input file
        for user in users:

            try:
                # Attempt to get a reference to the user object supplied if it exists in the supplied centre(facility)
                user_obj = FacilityUser.objects.get(
                    id=user["user_id"],
                    facility_id=Facility.objects.get(name=user["centre"]).id,
                )

            # Catch the exception when the user does not exist
            except ObjectDoesNotExist:
                # Print out the user id that does not exist in the facility and terminate the script
                print_colored(
                    "Error: User with id {} does not exist in Facility {}".format(
                        user["user_id"], user["centre"]
                    ),
                    colors.fg.red,
                )
                continue

            try:
                # Attempt to get a reference to the grade(classroom) supplied if it exists
                classroom_for_user = Classroom.objects.get(
                    name=user["grade"], parent_id=facility_id
                )

            # Catch the exception when the grade(classroom) does not exist
            except ObjectDoesNotExist:
                # Print out the name of the grade(classroom) that does not exist and terminate the script
                print_colored(
                    "Error: Classroom with the name {} does not exist".format(
                        user["grade"]
                    ),
                    colors.fg.red,
                )
                # exit in an error state
                continue

            # If the delete flag is supplied, delete all existing memberships for the user
            if delete_existing_memberships:
                print(
                    "Deleting Memberships for user: {}....".format(
                        str(user_obj.full_name)
                    )
                )
                Membership.objects.filter(user_id=user_obj.id).delete()

            if not user_obj.is_member_of(classroom_for_user):
                Membership.objects.create(user=user_obj, collection=classroom_for_user)
                # Print out a message confirming the membership has been created
                print_colored(
                    "Created Membership for user: {} in Classroom {}".format(
                        str(user_obj.full_name), str(classroom_for_user.name)
                    ),
                    colors.fg.green,
                )
                num_enrolled += 1

            else:
                print_colored(
                    "User : {} is already enrolled in Classroom {}. Skipping...".format(
                        str(user_obj.full_name), str(classroom_for_user.name)
                    ),
                    colors.fg.yellow,
                )
                continue

    # Print out the total number of users that were created
    if num_enrolled == 0:
        # If not learners were enrolled, something is wrong and there will be errors displayed in the console
        print_colored(
            "No learners were enrolled. Kindly check the errors/messages above",
            colors.fg.yellow,
        )
    elif num_enrolled != len(users):
        print_colored(
            "{} user(s) were enrolled into their classes. Some learners were not enrolled successfully or were skipped. Kindly check the errors/messages above".format(
                num_enrolled
            ),
            colors.fg.yellow,
        )
    else:
        print_colored(
            "{} user(s) were enrolled into their classes".format(num_enrolled),
            colors.fg.green,
        )


# Main function called when script is run
if __name__ == "__main__":
    args = argParser.parse_args()
    # If the file is supplied and facility is not supplied
    # Enroll learners into classes based on the defualt facility
    if args.file and not (args.centre):
        open_file = args.file
        enroll_learners_into_class(open_file, delete_existing_memberships=args.delete)

    # If both the file and the facility are supplied
    # Enroll learners into classes based on the supplied
    elif args.file and args.centre:
        open_file = args.file
        facility = args.centre
        enroll_learners_into_class(
            open_file, facility, delete_existing_memberships=args.delete
        )

    # If neither the file nor the facility are passed in, stop the script in an error state
    else:
        sys.exit(
            "No arguments passed in. Please pass in the path to the file, centre_id (optional) and delete_existing_memberships(optional)"
        )
