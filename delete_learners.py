import kolibri  # noqa F401
import django

import sys
import csv
import argparse

from django.core.exceptions import ObjectDoesNotExist

django.setup()

from kolibri.core.auth.models import FacilityUser  # noqa E402

argParser = argparse.ArgumentParser()

argParser.add_argument(
    "--file", "-f", help="File containing user_ids of users to delete"
)


def delete_users(input_file):
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
                print("Error: User with id {} does not exist".format(user["id"]))
                # continue to the next iteration of the loop
                continue
            # get the full name of the user from the database
            user_to_delete = str(FacilityUser.objects.get(id=user["id"]).full_name)

            # delete the user
            # note: deleting in this way cascades to other models that reference the user
            # i.e memberships, roles, loggers etc
            FacilityUser.objects.get(id=user["id"]).delete()

            # print out a message containing the name of the user that was deleted
            print("User {} deleted".format(user_to_delete))

            # increment the counter by 1
            num_deleted += 1

        # once the loop completes, print out the number of users that were deleted
        if len(to_delete) == num_deleted:
            print("Done! {} users were deleted".format(num_deleted))
        else:
            print(
                "{} user(s) deleted but {} were supplied. Please check the errors above".format(
                    num_deleted, len(to_delete)
                )
            )


# Main function called when the script is run
if __name__ == "__main__":
    args = argParser.parse_args()
    if args.file:
        open_file = args.file
        delete_users(open_file)
    else:
        sys.exit("Please supply a file containing the users to delete")
