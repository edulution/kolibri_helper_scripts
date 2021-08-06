import kolibri  # noqa F401
import django


django.setup()

from kolibri.core.auth.models import FacilityUser, Role  # noqa E402

from kolibri.core.logger.models import *  # noqa


def delete_learners_activity():
    """
    Funtion to delete all learners' activity from Kolibri

    Pre-conditon: None

    Post-condition: Deletes all activity for learners only, exluding coaches and admins.

    Return Value:
                None
    """
    # Exclude any coach and admin users by excluding all accounts in the role logger
    to_delete = FacilityUser.objects.exclude(
        id__in=[r.user_id for r in Role.objects.all()]
    )

    if (to_delete.count()) > 5:
        print(
            "\n{} users found, deleting users' activity might take several minutes."
            .format(to_delete.count())
        )
    else:
        print("\nDeleting activity for {} users".format(to_delete.count()))

    print("")

    # initialising the accumulater deletion
    num_deleted = 0

    # initialising the accumulater for errors
    count_errors = 0

    # loop through the learners
    for user in to_delete:

        # gettting each learner's id and full names from data base
        user_id = FacilityUser.objects.get(id=user.id).id
        user_full_name = str(FacilityUser.objects.get(id=user.id).full_name)

        # check if learner with given id has any activity
        try:
            # Divide into 0 to get error if leaner has no activity
            # Only check with one because the loggers are connected
            0 / ContentSummaryLog.objects.filter(user_id=user.id).count()
        except ZeroDivisionError:
            count_errors += 1
            print("Error: User with id {} has no activity to delete.".format(user_id))
            # continue to the next iteration of the loop
            continue

        # delete the user's activity
        # note: deleting in this way cascades to other logger tables that reference the user deleted loggers
        # i.e attemptlogs, masterylog etc
        ContentSummaryLog.objects.filter(user_id=user.id).delete()

        # delete contentsession logs becuase it does no cascade
        ContentSessionLog.objects.filter(user_id=user.id).delete()
        # UserSessionLog.objects.filter(user_id=user.id).delete()

        # delete exam logs logger becuase it does no cascade
        ExamLog.objects.filter(user_id=user.id).delete()
        ExamAttemptLog.objects.filter(user_id=user.id).delete()

        # print the user whose activity has been deleted
        print("All activity for {} has been deleted".format(user_full_name))

        # keeping track of deletions
        num_deleted += 1

    # once the loop completes, print out the number of users' activity that were deleted
    if (to_delete.count()) == num_deleted:
        print("\nDone! Activity for {} user(s) deleted".format(num_deleted))

    elif (to_delete.count()) == count_errors:
        print("\nNo user activity was deleted!")
    else:
        print(
            "\nActivity for {} user(s) deleted but {} users were found. Please"
            " check the errors above".format(num_deleted, len(to_delete))
        )


delete_learners_activity()
