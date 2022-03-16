import kolibri  # noqa F401
import django
import sys
import uuid
import csv
import argparse
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
    help="Delete all existing memberships. The default value is False",
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
        print("Error: Facility with the name {} does not exist".format(facility))
        # exit in an error state
        sys.exit("Learners were not enrolled successfully. Check the error(s) above")

    # Delete all existing memberships
    if delete_existing_memberships:
        Membership.objects.all().delete()

    # Use csv dictreader to get the contents of the file
    with open(input_file) as f:
        reader = csv.DictReader(f)
        users = [r for r in reader]

        # Loop through the list of users read from the input file
        for user in users:

            user_exists = (
                FacilityUser.objects.filter(
                    id=user["user_id"], facility_id=facility_id
                ).exists()
                and user["centre"] == facilityname
            )

            classroom_exists = Classroom.objects.filter(name=user["grade"]).exists()

            # If the user and classroom exist, create the membership
            if user_exists and classroom_exists:
                user_obj = FacilityUser.objects.get(
                    id=user["user_id"], facility_id=facility_id
                )

                classroom_for_user = classroom_exists = Classroom.objects.get(
                    name=user["grade"], parent_id=facility_id
                )

                Membership.objects.create(user=user_obj, collection=classroom_for_user)

                # Print out a message confirming the membership has been created
                print(
                    "Created Membership for user: {} in Classroom {}".format(
                        str(user_obj.full_name), str(classroom_for_user.name)
                    )
                )

                num_enrolled += 1
            # If the user and classroom do not exist, skip to the next iteration of the loop
            else:
                continue

    # Print out the total number of users that were created
    if num_enrolled == 0:
        # If not learners were enrolled, something is wrong and there will be errors displayed in the console
        print("No learners were enrolled. Kindly check the errors above")
    else:
        print("{} user(s) were enrolled into their classes".format(num_enrolled))


# Main function called when script is run
if __name__ == "__main__":
    args = argParser.parse_args()
    # If the file is supplied and facility is not supplied
    # Enroll learners into classes based on the defualt facility
    if args.file and not (args.centre or args.delete):
        open_file = args.file
        enroll_learners_into_class(open_file)

    # If both the file and the facility are supplied
    # Enroll learners into classes based on the supplied
    elif args.file and args.centre:
        facility = args.centre
        open_file = args.file
        enroll_learners_into_class(open_file, facility)

    # If the file and the delete existing membership are supplied
    # Enroll learners into classes based on the supplied
    elif args.file and args.delete:

        # convert provided option to lowercase
        if args.delete.lower() == "true":
            open_file = args.file
            enroll_learners_into_class(open_file, delete_existing_memberships=True)
        elif args.delete.lower() == "false":
            open_file = args.file
            enroll_learners_into_class(open_file)
        else:
            print(
                'Error: value "{}" is incorrect for the optional arguement "Delete existing memberships". Type either True or False'.format(
                    args.delete
                )
            )
    elif args.file and args.delete and args.centre:
        if args.delete.lower() == "true":
            open_file = args.file
            facility = args.centre
            enroll_learners_into_class(
                open_file, facility, delete_existing_memberships=True
            )
        elif args.delete.lower() == "false":
            open_file = args.file
            facility = args.centre
            enroll_learners_into_class(open_file, facility)
        else:
            print(
                'Error: value "{}" is incorrect for the optional arguement "Delete existing memberships". Type either True or False'.format(
                    args.delete
                )
            )

    # If neither the file nor the facility are passed in, stop the script in an error state
    else:
        sys.exit(
            "No arguments passed in. Please pass in the path to the file and centre_id (optional)"
        )
