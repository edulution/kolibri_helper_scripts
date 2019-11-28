# import kolibri and django to ensure the script runs in kolibri shell
import kolibri
import django
django.setup()

# import other libraries required
import os
from django.utils import timezone
from datetime import timedelta
from django.db import connection
from kolibri.core.logger.models import UserSessionLog
from kolibri.core.auth.models import *
import psycopg2


# function to get learners that were active in the last 10 minutes and return their user_ids
def get_live_learners():
	last_ten_minutes = timezone.now() - timedelta(minutes=10)
	try:
		# ensure that there is a conenction to the database
	    connection.ensure_connection()

	    # live learners are learners that have been active in the last 10 minutes
	    # get all usersessionlogs where the last interaction timestamp is greater or equal to current time minus 10 minutes
	    live_sessions = UserSessionLog.objects.filter(last_interaction_timestamp__gte=last_ten_minutes).values('user_id').distinct()

	    # get array of user_ids of live learners
	    live_learners = [user.get('user_id') for user in live_sessions]

	except OperationalError:
		# catch operational errors and print the error to the console
		print('Database unavailable, impossible to retrieve users and sessions info')

	# return an array of user_ids of live learners
	return live_learners

# function to insert an array of live learners into the live_learners table in the kolibri database
def insert_live_learners_into_db(live_learners_arr):
	# get the database credentials from environment variables
	dbname = os.environ['KOLIBRI_DATABASE_NAME']
	dbpassword = os.environ['KOLIBRI_DATABASE_PASSWORD']
	dbuser = os.environ['KOLIBRI_DATABASE_USER']
	dbhost = os.environ['KOLIBRI_DATABASE_HOST']
	dbport = os.environ['KOLIBRI_DATABASE_PORT']


	try:
		# connect to the postgresql database
	    connection = psycopg2.connect(user = dbuser,
	                                  password = dbpassword,
	                                  host = dbhost,
	                                  port = dbport,
	                                  database = dbname)

	    # create connection cursor object
	    cursor = connection.cursor()

	    # clear out the live learners table
	    cursor.execute('delete from live_learners')

	    # insert the array of user_ids into the live_learners table
	    for user_id in live_learners_arr:	
	    	cursor.execute("insert into live_learners(user_id) values (%s)",(user_id,))

	    # commit the changes to the database
	   	connection.commit()

	   	# Print the number of live learners that have been inserted into the table
	    print("%s live learner(s) inserted" % len(live_learners_arr))

	    
	except (Exception, psycopg2.Error) as error :
		# catch any errors from the database and print them to the console
	    print ("Error while connecting to the database", error)


# main excecution of script
if __name__ == '__main__':
	live_learners = get_live_learners()
	insert_live_learners_into_db(live_learners)







