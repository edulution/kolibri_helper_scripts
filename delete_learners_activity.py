import kolibri  # noqa F401
import django

import time
import csv
import argparse
import sys

django.setup()

from kolibri.core.auth.models import *  # noqa E402

from kolibri.core.logger.models import *  # noqa

argParser = argparse.ArgumentParser()
argParser.add_argument("input")


def warning(message, timer):
    """Print a warning message and allow time
    for the use to cancel before the program starts
    Pre-condition: take string message, and and int value
    Post-condition: displat warning message and wait given time before executing the program
    Return Value: None
    """

    cancel = "Ctrl-C to cancel"
    print(" " + "_" * (len(message) + 2))
    print("|" + " " * (len(message) + 2) + "|")
    print("| " + message + " |")
    print("|" + " " * (len(message) + 2) + "|")
    print("| " + cancel + " " * ((len(message) + 1) - len(cancel)) + "|")
    print("|" + "_" * (len(message) + 2) + "|")
    print(" ")


def deletion(to_delete, get_id):
    """Delete user activity
    Pre-condition: a list of users whose activity to delete
                    a value for get_id to assign the correct object attributes
    Post-condition: delete learner activity

    Return Value: None
    """

    # initialising the deletion accumulater
    num_deleted = 0

    # initialising the accumulater for errors
    count_errors = 0

    # initialising the accumulater for IDs that do not exist
    count_non_exits = 0

    count_exist = 0

    # loop through the learners
    for user in to_delete:

        # get user_id by assigning the right object attribute depending on get_id value
        if get_id == 0:
            # user_id for FacilityUser objects is an attribute id
            user_id = user.id
        elif get_id == 1:
            # user_id for Memebrship objects is an attribute user_id
            user_id = user.user_id
        elif get_id == 2:
            # user_id for CSV is from a column user_id
            user_id = user["user_id"]

        # check if a user with the id specified exists
        try:
            FacilityUser.objects.get(id=user_id)
            count_exist += 1
        # catch the exception when the object does not exist
        except ObjectDoesNotExist:
            count_non_exits += 1
            # print out the id that does not exist
            print("Error: User with id {} does not exist".format(user_id))
            # continue to the next iteration of the loop
            continue

        # gettting each learner's full names from data base
        user_full_name = str(FacilityUser.objects.get(id=user_id).full_name)

        # check if learner with given id has any activity
        try:
            # Divide into 0 to get error if leaner has no activity
            # Only check with one because the loggers are connected
            0 / ContentSummaryLog.objects.filter(user_id=user_id).count()
        except ZeroDivisionError:
            count_errors += 1
            print("Error: User with id {} has no activity to delete.".format(user_id))
            # continue to the next iteration of the loop
            continue

        # delete the user's activity
        # note: deleting in this way cascades to other logger tables that reference the user deleted loggers
        # i.e attemptlogs, masterylog etc
        ContentSummaryLog.objects.filter(user_id=user_id).delete()

        # delete contentsession logs becuase it does no cascade
        ContentSessionLog.objects.filter(user_id=user_id).delete()
        # UserSessionLog.objects.filter(user_id=user.id).delete()

        # delete exam logs logger becuase it does no cascade
        ExamLog.objects.filter(user_id=user_id).delete()
        ExamAttemptLog.objects.filter(user_id=user_id).delete()

        # print the user whose activity has been deleted
        print("All activity for {} has been deleted".format(user_full_name))

        # keeping track of deletions
        num_deleted += 1

    # once the loop completes, give the user feedback on what has been deleted and what errors were found
    # all learner activity has been deleted
    if len(to_delete) == num_deleted:
        print("\nDONE! \nActivity for {} user(s) deleted".format(num_deleted))
    # no user activity was deleted
    elif len(to_delete) == count_errors:
        print("\nNO USER(S) ACTIVITY WAS DELETED!\n check the errors above.")
    # no supplied users were found
    elif len(to_delete) == count_non_exits:
        print(
            "\nNO MATCHING IDs FOUND! \nMake sure the the has a column 'user_id'"
            " with user IDs"
        )
    elif len(to_delete) > count_non_exits:
        print(
            "\nActivity for {} user(s) deleted but {} user(s) were found. Please"
            " check the errors above".format(num_deleted, count_exist)
        )
    # some activity was deleted
    else:
        print(
            "\nActivity for {} user(s) deleted but {} user(s) were found. Please"
            " check the errors above".format(num_deleted, len(to_delete))
        )


def feed_back(to_delete):
    # Give the user feedback if alot of users are found from a list of leaners
    if len(to_delete) > 2:
        print(
            "\n{} users found, deleting users' activity might take several minutes."
            .format(len(to_delete))
        )
    else:
        print("\nDeleting activity for {} users".format(len(to_delete)))

    print("")


def delete_all_activity():
    """Delete all leaner activity
    Pre-condition: None
    Post-condition: delete all learner acitvity excluding coach and admin accounts
    Return Value: None"""

    # Exclude any coach and admin users by excluding all accounts in the role logger
    to_delete = FacilityUser.objects.exclude(
        id__in=[r.user_id for r in Role.objects.all()]
    )

    # warning message to user
    message = "WARNING! THIS WILL IS DELETE ACTIVTY FOR ALL LEARNERS."

    # call the warning function to display warning message and assign delay time
    warning(message, 5)

    # call feedback function to tell the user how many users were found
    feed_back(to_delete)

    # call the deletion to pass a list to delete
    deletion(to_delete, 0)


def delete_activity_with_exclusion(input_grade):
    """Delete all leaner activity except for a specific grade
    Pre-condition: an integer value for the grade to exempt from the deletion
    Post-condition: learner activity for leanrers other than the provided grade is deleted
    Return Value: None
    """

    # filtering non-grade 7 classes and excluding admin and coach accounts
    to_delete = Membership.objects.filter(
        collection_id__in=[
            r.id for r in Classroom.objects.exclude(name__icontains=input_grade)
        ]
    ).exclude(user_id__in=[r.user_id for r in Role.objects.all()])

    # warning message to user
    message = (
        "WARNING! THIS WILL IS DELETE ACTIVTY FOR ALL LEARNERS EXCEPT FOR "
        + input_grade.upper()
    )

    # call the warning function to display warning message and assign delay time
    warning(message, 5)

    # call feedback function to tell the user how many users were found
    feed_back(to_delete)

    # call the deletion to pass a list to delete
    deletion(to_delete, 1)


def delete_supplied_user_activity(input_file):
    """Function to delete users supplied in a csv file
    The csv file is expected to have a column id (uuid of each user to be deleted)

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

        # warning message to user
        message = (
            "WARNING! THIS WILL IS DELETE ACTIVTY FOR ALL LEARNERS SUPPLIED IN THE CSV"
            " FILE."
        )

        # call the warning function to display warning message and assign delay time
        warning(message, 5)

        # call feedback function to tell the user how many users were found
        feed_back(to_delete)

        # call the deletion to pass a list to delete
        deletion(to_delete, 2)


# Main function called when the script is run
if __name__ == "__main__":
    args = argParser.parse_args()
    if (args.input).lower() == 'all':
        delete_all_activity()
    elif args.input.isdigit():
        input_grade = str('Grade ' + args.input)
        delete_activity_with_exclusion(input_grade)
    elif args.input:
        input_file = args.input
        delete_supplied_user_activity(input_file)
    else:
        sys.exit(
            "\nPlease supply one of the following:\n  A grade to exempt \n  A file"
            " containing the users activity to delete \n  Enter 'all' to delete all"
            " user activity"
        )
