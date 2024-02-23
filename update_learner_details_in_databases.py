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

    Returns:
        argparse.Namespace: Object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Update learner details in the database."
    )
    parser.add_argument("input_file", type=str, help="Path to the input file")
    return parser.parse_args()


def update_learner_details(input_file):
    """
    Update learner details in the database based on the information provided in a CSV file.

    Args:
        input_file (str): Path to the input CSV file.
    """
    # Initialize counters for success, unchanged, not exist, and skipped users to 0
    success_count, unchanged_count, not_exist_count, skipped_count = 0, 0, 0, 0

    try:
        # Open and read the input CSV file
        with open(input_file) as f:
            reader = csv.DictReader(f)
            users = [r for r in reader]

            # Iterate over each user in the CSV file
            for user in users:
                user_id = user["user_id"]
                new_username = user["username"]
                new_full_name = user["full_name"]

                # Check for missing or empty fields
                if not new_username.strip() or not new_full_name.strip():
                    print_colored(
                        "Skipping user with ID {}: Username or Full name is missing or empty".format(
                            user_id
                        ),
                        colors.fg.red,
                    )
                    skipped_count += 1
                    continue

                try:
                    # Get user object from the database by user_id and check if it exists
                    user_object = FacilityUser.objects.get(id=user_id)
                except ObjectDoesNotExist:
                    not_exist_count += 1
                    # Print error message and continue to the next user
                    print_colored(
                        "User with ID {}: Does not exist".format(user_id), colors.fg.red
                    )
                    continue

                # Check for duplicate username in the database
                if (
                    FacilityUser.objects.exclude(id=user_id)
                    .filter(username=new_username)
                    .exists()
                ):
                    print_colored(
                        "Duplicate username. There is already a user called {}".format(
                            new_username
                        ),
                        colors.fg.red,
                    )
                    continue

                # Check if user details have changed and update them
                if (user_object.full_name == new_full_name) and (
                    user_object.username == new_username
                ):
                    unchanged_count += 1
                    print_colored(
                        "User with ID {}: Details have not changed".format(user_id),
                        colors.fg.yellow,
                    )
                else:
                    # Update user details in the database
                    if user_object.full_name != new_full_name:
                        user_object.full_name = new_full_name
                        user_object.save()
                        print_colored(
                            "User with ID {}: Full name has been changed to {}".format(
                                user_id, new_full_name
                            ),
                            colors.fg.green,
                        )

                    # Establish connection to the database
                    if user_object.username != new_username:
                        user_object.username = new_username
                        user_object.save()
                        print_colored(
                            "User with ID {}: Username has been changed to {}".format(
                                user_id, new_username
                            ),
                            colors.fg.green,
                        )

                        # Establish connection to the database

                        # Update username in the baseline_testing database
                        cursor = conn.cursor()
                        try:
                            conn = psycopg2.connect(
                                dbname=os.environ.get("BASELINE_DATABASE_NAME"),
                                user=os.environ.get("BASELINE_DATABASE_USER"),
                                password=os.environ.get("BASELINE_DATABASE_PASSWORD"),
                                host=os.environ.get("BASELINE_DATABASE_HOST"),
                            )

                            # Update username in the database for the user with the given user_id
                            sql_query = (
                                "UPDATE responses SET username = %s WHERE user_id = %s"
                            )
                            cursor.execute(sql_query, (new_username, user_id))
                            conn.commit()

                            # Print success message and close the cursor and connection to the database
                            print_colored(
                                "User with ID {}: Username updated in baseline_testing database".format(
                                    user_id
                                ),
                                colors.fg.green,
                            )
                        except psycopg2.Error as e:
                            print_colored(
                                "Error updating username in baseline_testing database for user with ID {}: {}".format(
                                    user_id, e
                                ),
                                colors.fg.red,
                            )
                        finally:
                            cursor.close()
                            if conn is not None:
                                conn.close()

                    success_count += 1

    except Exception as e:
        print_colored("An unexpected error occurred: {}".format(e), colors.fg.red)

    # Print summary of updates and errors
    print_summary(
        success_count, unchanged_count, not_exist_count, skipped_count, len(users)
    )


# Function to print summary of updates and errors
def print_summary(
    success_count, unchanged_count, not_exist_count, skipped_count, total_users
):
    """
    Print summary of updates and errors.

    Args:
        success_count (int): Number of users whose details were successfully updated.
        unchanged_count (int): Number of users whose details have not changed.
        not_exist_count (int): Number of users who do not exist.
        skipped_count (int): Number of users whose details were skipped due to missing or empty fields.
        total_users (int): Total number of users processed.
    """
    if success_count == 0:
        print_colored("No learners' details were updated.", colors.fg.red)
    elif success_count != total_users:
        print_colored(
            "{} learner(s) had their details successfully updated.".format(
                success_count
            ),
            colors.fg.lightgreen,
        )
    else:
        print_colored(
            "All {} learner(s) had their details successfully updated.".format(
                success_count
            ),
            colors.fg.lightgreen,
        )

    if unchanged_count > 0:
        print_colored(
            "{} learner(s) details have not changed.".format(unchanged_count),
            colors.fg.yellow,
        )

    if not_exist_count > 0:
        print_colored(
            "{} learner(s) do not exist.".format(not_exist_count), colors.fg.red
        )

    if skipped_count > 0:
        print_colored(
            "{} learner(s) were skipped due to missing or empty fields.".format(
                skipped_count
            ),
            colors.fg.red,
        )


# Main function
if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()
    if not args.input_file:
        print_colored(
            "Error: Please provide the path to the input file.", colors.fg.red
        )
        sys.exit(1)

    # Update learner details in the database based on the information provided in the input file
    update_learner_details(args.input_file)
