import kolibri  # noqa F401
import django
import sys
import csv
import argparse
from colors import *

from django.core.exceptions import ObjectDoesNotExist

django.setup()

from kolibri.core.auth.models import FacilityUser  # noqa E402

argParser = argparse.ArgumentParser()

argParser.add_argument(
    "--file", "-f", help="File containing user_ids of users to restore"
)


def restore_users(input_file):
    """Function to restore users supplied in a csv file
    The csv file is expected to have a column user_id (uuid of each user to be restored)

    Args:
        input_file (string): Path to the file containig the ids of users to restore

    Returns:
        None
    """

    # open the csv file provided and read each line into a dictionary data structure
    with open(input_file) as f:
        reader = csv.DictReader(f)

        # use a list comprehension to store all of the lines in an array
        to_restore = [r for r in reader]

        # initialize a counter variable to track how many users have been restored
        num_restored = 0

        # loop through the objects in the array
        for user in to_restore:
            # check if a user with the id specified exists
            try:
                FacilityUser.objects.get(id=user["id"])
            # catch the exception when the object does not exist
            except ObjectDoesNotExist:
                # print out the id that does not exist
                print_colored(
                    "Error: User with id {} does not exist".format(user["id"]),
                    colors.fg.red,
                )
                # continue to the next iteration of the loop
                continue
            # get the full name of the user from the database
            user_to_restore = str(FacilityUser.objects.get(id=user["id"]).full_name)

            user_obj = FacilityUser.objects.get(id=user["id"])

            user_obj.set_deleted = False #set deleted property to false
            user_obj.save()

            # print out a message containing the name of the user that was restored
            print_colored(
                "User {} has been restored".format(user_to_restore),
                colors.fg.yellow,
            )

            # increment the counter by 1
            num_restored += 1

        # once the loop completes, print out the number of users that were restored
        if len(to_restore) == num_restored:
            print_colored(
                "Done! {} users were restored".format(num_restored),
                colors.fg.lightgreen,
            )
        else:
            print_colored(
                "{} user(s) restored but {} were supplied. Please check the errors above".format(
                    num_restored, len(to_restore)
                ),
                colors.fg.lightcyan,
            )


# Main function called when the script is run
if __name__ == "__main__":
    args = argParser.parse_args()
    if args.file:
        open_file = args.file
        restore_users(open_file)
    else:
        sys.exit("Please supply a file containing the users to restore")
