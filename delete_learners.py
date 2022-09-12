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
    "--file", "-f", help="File containing user_ids of users to delete"
)

argParser.add_argument(
    "--hard",
    "-d",
    action="store_true",
    default=False,
    help="Permanently delete users with user_ids in the file provided. The default value is False",
)


def delete_users(input_file,permanently_delete_user=False):
    """Function to delete users supplied in a csv file
    The csv file is expected to have a column user_id (uuid of each user to be deleted)

    Args:
        input_file (string): Path to the file containig the ids of users to delete

    Returns:
        None
    """

    # open the csv file provided and read each line into a dictionary data structure
    with open(input_file) as f:
        reader = csv.DictReader(f)

        # use a list comprehension to store all of the lines an array
        to_delete = [r for r in reader]

        # initialize a counter variable to track how many users have been deleted
        num_deleted = 0

        # loop through the objects in the array
        for user in to_delete:
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
            user_to_delete = str(FacilityUser.objects.get(id=user["id"]).full_name)

            user_obj = FacilityUser.objects.get(id=user["id"])

            #if the hard delete flag is supplied, permanently delete the user
            if permanently_delete_user:
                # delete the user
                # note: deleting in this way cascades to other models that reference the user
                # i.e memberships, roles, loggers etc
                user_obj.delete()

                # print out a message containing the name of the user that was permanently deleted
                print_colored(
                    "User {} has been permanently deleted".format(user_to_delete),
                    colors.fg.yellow,
                )

                # increment the counter by 1
                num_deleted += 1
            else:
                #soft delete
                user_obj.set_deleted = True #set deleted to true
                user_obj.save()

                # print out a message containing the name of the user that was soft deleted
                print_colored(
                    "User {} has been soft deleted".format(user_to_delete),
                    colors.fg.yellow,
                )

                # increment the counter by 1
                num_deleted += 1

        # once the loop completes, print out the number of users that were deleted
        if len(to_delete) == num_deleted:
            print_colored(
                "Done! {} users were deleted".format(num_deleted),
                colors.fg.lightgreen,
            )
        else:
            print_colored(
                "{} user(s) deleted but {} were supplied. Please check the errors above".format(
                    num_deleted, len(to_delete)
                ),
                colors.fg.lightcyan,
            )


# Main function called when the script is run
if __name__ == "__main__":
    args = argParser.parse_args()
    if args.file:
        open_file = args.file
        delete_users(open_file,permanently_delete_user=args.hard)
    else:
        sys.exit("Please supply a file containing the users to delete")
