import kolibri  # noqa F401
import django
import sys
import uuid
import csv
import argparse
from django.core.exceptions import ObjectDoesNotExist

django.setup()

from kolibri.core.auth.models import (
    Facility,
    FacilityDataset,
    FacilityUser,
    Classroom
)  # noqa E402


from helpers import get_or_create_classroom, get_or_create_learnergroup

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

# List of the LearnerGroups we want to create in each class
wanted_learnergroups = ["Level 1","Level 2","Level 3","Level 4","Level 5","Unknown"]


def create_classes_and_groups(input_file, facilityname=def_facility,delete_existing_classrooms=True):
    """Function to created classrooms and groups inside each classroom based on a csv file
    The file is expected to have columns centre and grade. All other columns are ignored
    The grade column represents the names of the classrooms to create.

    Args:
        input_file (string): Path to the csv file containing the users
        facility (string): Name of the facility in which to create the classrooms(default facility if not specified)

    Returns:
        None
    """

    # Check if the Facility supplied exists
    try:
        # Attempt to get a reference to the Facility supplied if it exists
        facility_obj = Facility.objects.get(name=facilityname)

        facility_id = facility_obj.id
        dataset_id = facility_obj.dataset_id

    # Catch the exception when the Facility does not exist
    except ObjectDoesNotExist:
        # Print out the name of the Facility that does not exist and terminate the script
        print("Error: Facility with the name {} does not exist".format(facilityname))
        # exit in an error state
        sys.exit("Classrooms and Groups have not been created. Check the error(s) above")


    # Delete all classrooms in the facility
    if delete_existing_classrooms:
        Classroom.objects.filter(parent_id = facility_id).delete()

    # Use csv dictreader to get the contents of the file
    with open(input_file) as f:
        reader = csv.DictReader(f)
        centres_and_classrooms = [r for r in reader]

        # Loop through the list of centres and classrooms read from the csv above
        for row in centres_and_classrooms:

            facility_exists = facility_obj.name == row["centre"]

            # If the facility exists, create the classroom specified in the grade column
            if facility_exists:
                classroom_to_create = get_or_create_classroom(row["grade"], facilityname)
                # in the classroom that has just been created, create all of the wanted learnergroups
                for learnergroup in wanted_learnergroups:
                    get_or_create_learnergroup(learnergroup, classroom_to_create.name, facilityname)
                
            # If the facility does not exist,  continue to the next iteration of the loop
            else:
                continue

# Main function called when script is run
if __name__ == "__main__":
    args = argParser.parse_args()
    # If the file is supplied and facility is not supplied
    # Create the classrooms and learnergroups in the default facility
    if args.file and not (args.centre):
        open_file = args.file
        create_classes_and_groups(open_file)

    # If both the file and the facility are supplied
    # Create the classrooms and learnergroups based on the facility supplied
    elif args.file and args.centre:
        facility = args.centre
        open_file = args.file
        create_classes_and_groups(open_file, facility)

    # If neither the file nor the facility are passed in, stop the script in an error state
    else:
        sys.exit(
            "No arguments passed in. Please pass in the path to the file and centre_id (optional)"
        )
