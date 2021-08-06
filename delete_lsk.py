import kolibri  # noqa F401
import django


django.setup()

from kolibri.core.auth.models import *  # noqa E402

from kolibri.core.logger.models import *  # noqa


def delete_learners_activity():

    # filtering non-grade 7 classes and excluding admin and coach accounts
    to_delete = Membership.objects.filter(
        collection_id__in=[
            r.id for r in Classroom.objects.exclude(name__icontains='Grade 7')
        ]
    ).exclude(user_id__in=[r.user_id for r in Role.objects.all()])

    # feedback to user
    if (to_delete.count()) > 2:
        print(
            "\n{} user(s) found, deleting user(s) activity might take several minutes."
            .format(to_delete.count())
        )
    else:
        print("\nDeleting user activity for {} user(s)".format(to_delete.count()))

    print("")

    # initialising the accumulater deletion
    num_deleted = 0

    # initialising the accumulater for errors
    count_errors = 0

    for user in to_delete:

        user_id = user.user_id
        full_name = str(FacilityUser.objects.get(id=user.user_id).full_name)

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
        # UserSessionLog.objects.filter(user_id=user_id).delete()

        # delete exam logs logger becuase it does no cascade
        ExamLog.objects.filter(user_id=user_id).delete()
        ExamAttemptLog.objects.filter(user_id=user_id).delete()

        # print the user whose activity has been deleted
        print("All activity for {} has been deleted".format(full_name))

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
