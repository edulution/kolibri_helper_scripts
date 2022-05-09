# import kolibri and django to ensure the script runs in kolibri shell
import kolibri  # noqa F401
import django
from colors import *

django.setup()  # noqa F401

# import other libraries required
import os
from datetime import timedelta
from django.db import connection
from django.utils import timezone
from kolibri.core.logger.models import UserSessionLog
from django.db.utils import OperationalError
import psycopg2


def get_live_learners():
    """Get learners that are active based on Kolibri idle session timeout
    Args:
        None
    Returns:
        A list of user_ids of the learners currently logged in
    """
    # get kolibri idle session timeout as an integer
    sess_timeout = int(os.environ["KOLIBRI_SESSION_TIMEOUT"])
    # initalize cut-off time using kolibri idle session timeout to decide which learners qualify as live learners
    live_learners_cutoff = timezone.now() - timedelta(seconds=sess_timeout)
    try:
        # ensure that there is a conenction to the database
        connection.ensure_connection()

        # live learners are learners that have been active in the last 10 minutes
        # get all usersessionlogs
        # where the last interaction timestamp is greater or equal to current time minus kolibri idle seesion timeout
        live_sessions = (
            UserSessionLog.objects.filter(
                last_interaction_timestamp__gte=live_learners_cutoff
            )
            .values("user_id")
            .distinct()
        )

        # get array of user_ids of live learners
        live_learners = [user.get("user_id") for user in live_sessions]

    except OperationalError:
        # catch operational errors and inform the user
        print_colored(
            "Database unavailable, not able to retrieve users and sessions info",
            colors.fg.red,
        )

    # return an array of user_ids of live learners
    return live_learners


def insert_live_learners_into_db(live_learners_arr):
    """Insert an array of live learners into the live_learners table in the baseline database
    Args:
        A list of user_ids
    Returns:
        None
    """

    # get the database credentials from environment variables
    dbname = os.environ["BASELINE_DATABASE_NAME"]
    dbpassword = os.environ["BASELINE_DATABASE_PASSWORD"]
    dbuser = os.environ["BASELINE_DATABASE_USER"]
    dbhost = os.environ["BASELINE_DATABASE_HOST"]
    dbport = os.environ["BASELINE_DATABASE_PORT"]

    try:
        # connect to the postgresql database
        connection = psycopg2.connect(
            user=dbuser, password=dbpassword, host=dbhost, port=dbport, database=dbname
        )

        # create connection cursor object
        cursor = connection.cursor()

        # clear out the live learners table
        cursor.execute("delete from live_learners")

        # insert the array of user_ids into the live_learners table
        for user_id in live_learners_arr:
            cursor.execute("insert into live_learners(user_id) values (%s)", (user_id,))

        # commit the changes to the database
        connection.commit()

        # Print the number of live learners that have been inserted into the table
        print_colored(
            "%s users(s) currently logged in" % len(live_learners_arr),
            colors.fg.lightgreen,
        )

    except (Exception, psycopg2.Error) as error:
        # catch any errors from the database and print them to the console
        print_colored("Error while connecting to the database", error)


# main excecution of script
# Get the live learners then insert them into live learners table
if __name__ == "__main__":
    live_learners = get_live_learners()
    insert_live_learners_into_db(live_learners)
