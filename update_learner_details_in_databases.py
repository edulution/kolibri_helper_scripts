import argparse
import csv
import django
import os
import sys
import psycopg2
import kolibri
django.setup()

from colors import print_colored, colors
from django.core.exceptions import ObjectDoesNotExist
from kolibri.core.auth.models import FacilityUser

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Update learner details in the database.')
    parser.add_argument('input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def update_learner_details(input_file):
    """
    Update learner details in the database based on the information provided in a CSV file.

    Args:
        input_file (str): Path to the input CSV file.
    """
    success_count = 0
    unchanged_count = 0
    not_exist_count = 0

    try:
        # Connect to the baseline_testing database using environmental variables
        conn = psycopg2.connect(
            dbname=os.environ.get('BASELINE_DATABASE_NAME'),
            user=os.environ.get('BASELINE_DATABASE_USER'),
            password=os.environ.get('BASELINE_DATABASE_PASSWORD'),
            host=os.environ.get('BASELINE_DATABASE_HOST')
        )
        # Read the input file and update learner details
        with open(input_file) as f:
            reader = csv.DictReader(f)
            users = [r for r in reader]

            for user in users:
                user_id = user["user_id"]

                try:
                    # Get user object from the Kolibri database by user_id using Django ORM
                    user_object = FacilityUser.objects.get(id=user_id)
                except ObjectDoesNotExist:
                    not_exist_count += 1
                    # Print error message and continue to the next user in the input file
                    error_msg = "User with ID {}: Does not exist".format(user_id)
                    print_colored(error_msg, colors.fg.red)
                    continue

                # Check if the username already exists in the Kolibri database and is not the same as the current user's username
                if FacilityUser.objects.exclude(id=user_id).filter(username=user["username"]).exists():
                    print_colored(
                        "Duplicate username. There is already a user called {}".format(user["username"]),
                        colors.fg.red
                    )
                    continue
                # Check if the full name and username have not changed
                if (user_object.full_name == user["full_name"]) and (user_object.username == user["username"]):
                    unchanged_count += 1
                    print_colored("User with ID {}: Details have not changed".format(user_id), colors.fg.yellow)
                else:
                    # Update user details in the Kolibri database using Django ORM
                    user_object.full_name = user["full_name"]
                    user_object.username = user["username"]
                    user_object.save()

                    success_count += 1
                    success_msg = "User with ID {}: Full name has been changed to {}. Username has been changed to {}".format(
                        user_id, user_object.full_name, user_object.username
                    )
                    print_colored(success_msg, colors.fg.green)

                    # Update username in the baseline_testing database using psycopg2 module
                    cursor = conn.cursor()
                    sql_query = "UPDATE responses SET username = %s WHERE user_id = %s"
                    cursor.execute(sql_query, (user["username"], user_id))
                    conn.commit()
                    # Close the cursor after executing the query to avoid memory leaks
                    cursor.close()
                    success_msg = "User with ID {}: Username updated in baseline_testing database".format(user_id)
                    print_colored(success_msg, colors.fg.green)

    # Handle exceptions and close the connection to the database
    except psycopg2.Error as e:
        error_msg = "Error: {}".format(e)
        print_colored(error_msg, colors.fg.red)

    finally:
        if conn is not None:
            conn.close()
    
    # Print summary of updates and errors
    print_summary(success_count, unchanged_count, not_exist_count, len(users))

# Print summary of updates and errors in different colors
def print_summary(success_count, unchanged_count, not_exist_count, total_users):
    """
    Print summary of updates and errors.

    Args:
        success_count (int): Number of users whose details were successfully updated.
        unchanged_count (int): Number of users whose details have not changed.
        not_exist_count (int): Number of users who do not exist.
        total_users (int): Total number of users processed.
    """
    if success_count == 0:
        print_colored("No learners' details were updated.", colors.fg.red)
    elif success_count != total_users:
        print_colored("{} learner(s) had their details successfully updated.".format(success_count), colors.fg.lightgreen)
    else:
        print_colored("All {} learner(s) had their details successfully updated.".format(success_count), colors.fg.lightgreen)

    if unchanged_count > 0:
        print_colored("{} learner(s) details have not changed.".format(unchanged_count), colors.fg.yellow)

    if not_exist_count > 0:
        print_colored("{} learner(s) do not exist.".format(not_exist_count), colors.fg.red)

if __name__ == '__main__':
    args = parse_arguments()
    update_learner_details(args.input_file)
