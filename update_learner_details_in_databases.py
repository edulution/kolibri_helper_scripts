import argparse
import csv
import os
import django
import kolibri
import psycopg2
django.setup()
from kolibri.core.auth.models import FacilityUser
from django.core.exceptions import ObjectDoesNotExist
from colors import *

def parse_arguments():
    parser = argparse.ArgumentParser(description='Update learner details in the database.')
    parser.add_argument('input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def update_learner_details(input_file):
    """
    Update learner details in both the Kolibri and baseline_testing databases based on the information provided in a CSV file.

    Args:
        input_file (str): Path to the input CSV file.
    """
    try:
        with open(input_file) as f:
            reader = csv.DictReader(f)
            users = [r for r in reader]

            for user in users:
                try:
                    # Get user object from the Kolibri database by user_id
                    user_object = FacilityUser.objects.get(id=user["user_id"])

                    # Update user's full name and username in the Kolibri database
                    user_object.full_name = user["full_name"]
                    user_object.username = user["username"]
                    user_object.save()
                    success = "User with ID {}: Full name has been changed to {}. Username has been changed to {}".format(
                        user_object.id, user_object.full_name, user_object.username
                    )
                    print_colored(success, fg.green)

                    # Connect to baseline_testing database and update username in responses table
                    conn = psycopg2.connect(
                        dbname=os.environ['BASELINE_DATABASE_NAME'],
                        user=os.environ['BASELINE_DATABASE_USER'],
                        password=os.environ['BASELINE_DATABASE_PASSWORD'],
                        host=os.environ['BASELINE_DATABASE_HOST']
                    )
                    cursor = conn.cursor()
                    sql_query = "UPDATE responses SET username = %s WHERE user_id = %s"
                    cursor.execute(sql_query, (user["username"], user["user_id"]))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    print_colored("Username updated in baseline_testing database", fg.green)

                except ObjectDoesNotExist:
                    error = "Error: User with ID {} does not exist".format(user['user_id'])
                    print_colored(error, fg.red)

                    continue
    except OSError as e:
        error = "Error: {}".format(e)
        print_colored(error, fg.red)

if __name__ == '__main__':
    args = parse_arguments()
    update_learner_details(args.input_file)