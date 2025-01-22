import argparse
import csv
import logging
import os
import psycopg2
from contextlib import contextmanager

@contextmanager
def connect_to_db(config):
    """Connects to the database using provided configuration

    Args:
        config (dict): Dictionary containing database connection parameters

    Yields:
        psycopg2.connect: A connection object to the database
    """
    conn = None
    try:
        conn = psycopg2.connect(**config)
        yield conn
    except Exception as e:
        logging.error("Error connecting to database with config {}: {}".format(config, e))
        raise
    finally:
        if conn:
            conn.close()

def export_data(user_ids, output_file, table_name, cursor, user_column='user_id'):
    """Exports data for a specific table using provided user IDs

    Args:
        user_ids (list): List of user IDs
        output_file (str): Path to the output CSV file
        table_name (str): Name of the table to export data from
        cursor (psycopg2.cursor): Database cursor object
        user_column (str): Name of the user ID column in the table
    """
    formatted_ids = ', '.join(["'{}'".format(uid) for uid in user_ids])
    query = "COPY (SELECT * FROM {} WHERE {} IN ({})) TO STDOUT WITH DELIMITER ',' CSV HEADER;".format(table_name, user_column, formatted_ids)

    try:
        # Create the directory if it does not exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_file, 'w') as f:
            cursor.copy_expert(query, f)
        logging.info("Data exported successfully for table: {}".format(table_name))
    except Exception as e:
        logging.error("Error exporting data for table {}: {}".format(table_name, e))

def validate_env_vars(vars_list):
    """Validates that all required environment variables are set

    Args:
        vars_list (list): List of environment variable names

    Returns:
        dict: Dictionary with environment variable values

    Raises:
        EnvironmentError: If any environment variable is missing
    """
    env_vars = {}
    for var in vars_list:
        value = os.environ.get(var)
        if value is None:
            logging.error("Required environment variable {} is not set.".format(var))
            raise EnvironmentError("Required environment variable {} is not set.".format(var))
        env_vars[var] = value
    return {
        'host': env_vars[vars_list[0]],
        'user': env_vars[vars_list[1]],
        'password': env_vars[vars_list[2]],
        'dbname': env_vars[vars_list[3]],
        'port': env_vars[vars_list[4]]
    }

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Export activity data for user IDs specified in a CSV file')
    parser.add_argument('-f', '--csv-file', help='CSV file containing user IDs', required=True)
    args = parser.parse_args()

    # Validate and fetch database connection parameters
    BASELINE_VARS = ['BASELINE_DATABASE_HOST', 'BASELINE_DATABASE_USER', 'BASELINE_DATABASE_PASSWORD',
                     'BASELINE_DATABASE_NAME', 'BASELINE_DATABASE_PORT']
    KOLIBRI_VARS = ['KOLIBRI_DATABASE_HOST', 'KOLIBRI_DATABASE_USER', 'KOLIBRI_DATABASE_PASSWORD',
                    'KOLIBRI_DATABASE_NAME', 'KOLIBRI_DATABASE_PORT']
    
    BASELINE_DATABASE_CONFIG = validate_env_vars(BASELINE_VARS)
    KOLIBRI_DATABASE_CONFIG = validate_env_vars(KOLIBRI_VARS)

    # Define tables to export
    tables_to_export = [
        ('responses', 'responses.csv', 'user_id'),
        ('kolibriauth_facilityuser', 'kolibriauth_facilityuser.csv', 'id'),
        ('logger_attemptlog', 'logger_attemptlog.csv', 'user_id'),
        ('logger_contentsessionlog', 'logger_contentsessionlog.csv', 'user_id'),
        ('logger_contentsummarylog', 'logger_contentsummarylog.csv', 'user_id'),
        ('logger_masterylog', 'logger_masterylog.csv', 'user_id'),
        ('logger_usersessionlog', 'logger_usersessionlog.csv', 'user_id')
    ]

    # Read user IDs from CSV file
    user_ids = []
    try:
        with open(args.csv_file, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip header
            for row in reader:
                if row:  # Ignore empty rows
                    user_id = row[0].strip()  # Remove potential whitespace
                    if user_id:  # Check if user_id is not empty
                        logging.info("Processing user ID: {}".format(user_id))
                        user_ids.append(user_id)
                    else:
                        logging.warning("Empty user ID found in CSV, skipping")
    except FileNotFoundError as e:
        logging.error("CSV file not found: {}".format(e))
        return
    except Exception as e:
        logging.error("Error reading CSV file: {}".format(e))
        return

    if not user_ids:
        logging.error("No valid user IDs found in the CSV file.")
        return

    # Connect to baseline and Kolibri databases
    try:
        with connect_to_db(BASELINE_DATABASE_CONFIG) as baseline_conn:
            with baseline_conn.cursor() as baseline_cursor:
                # Connect to Kolibri database
                with connect_to_db(KOLIBRI_DATABASE_CONFIG) as kolibri_conn:
                    with kolibri_conn.cursor() as kolibri_cursor:
                        # Export data for each table
                        for table, csv_file, user_column in tables_to_export:
                            if table == 'responses':
                                export_data(user_ids, csv_file, table, baseline_cursor, user_column)
                            else:
                                export_data(user_ids, csv_file, table, kolibri_cursor, user_column)
    except Exception as e:
        logging.error("Error during data export: {}".format(e))
    
    logging.info("Data export process completed successfully.")

if __name__ == "__main__":
    main()
