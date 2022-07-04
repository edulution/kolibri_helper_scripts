import kolibri  # noqa F401
import django
import sys
import csv
import argparse
from django.core.exceptions import ObjectDoesNotExist

django.setup()

from kolibri.core.auth.models import (
    Facility,
    FacilityUser,
)  # noqa E402

# Initalize argparse and define command line args that can be passed to this module
argParser = argparse.ArgumentParser()
argParser.add_argument(
    "--file", "-f", help="File containing user_ids of users to update"
)


# Get the name of the default facility on the device
# used as the default value in case facility is not passed in
def_facility = str(Facility.get_default_facility().name)


def update_users(input_file):
    num_updated = 0
    # Use csv dictreader to get the contents of the file
    with open(input_file) as f:
        reader = csv.DictReader(f)
        users = [r for r in reader]

        # Loop through the list of users read from the input file
        for user in users:
            user_id = user["id"]
            new_username = user["new_username"]

            # Check if username already exist
            user_exists = FacilityUser.objects.filter(username=new_username).exists()
            if user_exists:
                # if a user with the same username already exists in the facility
                # raise a value error and continue
                print(
                    "Duplicate username. There is already a user called {}".format(
                        new_username
                    )
                )
                continue
            else:
                # Update the user
                user_to_update = FacilityUser.objects.get(id=user_id)
                user_to_update.username = new_username
                user_to_update.save()

                # Print out the user's full name and latest username
                print(
                    "Updated user: {} username to {}".format(
                        user_to_update.full_name, new_username
                    )
                )

                # Increment the number of users created by one
                num_updated += 1

    # Print out the total number of users that were updated
    if len(users) == 0:
        # If no learners were updated, something is wrong and there will be errors displayed in the console
        print("Done! {} users were updated".format(num_updated))
    else:
        print(
            "{} user(s) updated but {} were supplied.".format(num_updated, len(users))
        )


# Main function called when script is run
if __name__ == "__main__":
    args = argParser.parse_args()
    if args.file:
        open_file = args.file
        update_users(open_file)
    else:
        sys.exit("Please supply a file containing the users to update")
