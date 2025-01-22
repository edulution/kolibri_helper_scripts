import os
import csv
import logging
import psycopg2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set environment variables
KOLIBRI_DATABASE_PASSWORD = os.getenv('KOLIBRI_DATABASE_PASSWORD')
KOLIBRI_DATABASE_HOST = os.getenv('KOLIBRI_DATABASE_HOST')
KOLIBRI_DATABASE_USER = os.getenv('KOLIBRI_DATABASE_USER')
KOLIBRI_DATABASE_NAME = os.getenv('KOLIBRI_DATABASE_NAME')
KOLIBRI_DATABASE_PORT = os.getenv('KOLIBRI_DATABASE_PORT')

def fetch_replacements():
    """Fetches distinct facility_id and dataset_id from the database."""
    try:
        conn = psycopg2.connect(
            dbname=KOLIBRI_DATABASE_NAME,
            user=KOLIBRI_DATABASE_USER,
            password=KOLIBRI_DATABASE_PASSWORD,
            host=KOLIBRI_DATABASE_HOST,
            port=KOLIBRI_DATABASE_PORT
        )
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT facility_id, dataset_id FROM kolibriauth_facilityuser;")
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except psycopg2.Error as e:
        logging.error("Error connecting to database: %s", e)
        return []

def generate_replacement_dicts(results):
    """Generates dictionaries for facility_id and dataset_id replacements."""
    facility_replacements = {}
    dataset_replacements = {}
    
    for result in results:
        old_facility_id, new_facility_id = result[0], result[0]  # Placeholder for actual logic
        old_dataset_id, new_dataset_id = result[1], result[1]  # Placeholder for actual logic
        facility_replacements[old_facility_id] = new_facility_id
        dataset_replacements[old_dataset_id] = new_dataset_id

    return facility_replacements, dataset_replacements

def generate_morango_partition_replacement(old_partition, dataset_replacements):
    """Generates the new _morango_partition based on dataset_id replacements."""
    for old_id, new_id in dataset_replacements.items():
        stripped_old_id = old_id.replace('-', '')
        if stripped_old_id in old_partition:
            stripped_new_id = new_id.replace('-', '')
            return old_partition.replace(stripped_old_id, stripped_new_id)
    return old_partition

def replace_ids_in_csv(file_path, column_replacements):
    """Replaces IDs in the specified columns of a CSV file."""
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            fieldnames = reader.fieldnames
        
        if fieldnames is None:
            logging.error("No fieldnames found in file: %s", file_path)
            return

        with open(file_path, 'w') as file:  # Removed newline='' for Python 2 compatibility
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                for column, replacements in column_replacements.items():
                    if column in row:
                        if column == '_morango_partition':
                            row[column] = generate_morango_partition_replacement(row[column], replacements)
                        else:
                            row[column] = replacements.get(row[column], row[column])
                writer.writerow(row)
        logging.info("Processed file: %s", file_path)
    except IOError as e:
        logging.error("Error processing file %s: %s", file_path, e)

def main():
    results = fetch_replacements()
    if not results:
        logging.error("No replacements fetched, exiting.")
        return

    facility_replacements, dataset_replacements = generate_replacement_dicts(results)

    # List of CSV files to process and the specific columns to replace
    csv_files = {
        'kolibriauth_facilityuser.csv': {'facility_id': facility_replacements, 'dataset_id': dataset_replacements, '_morango_partition': dataset_replacements},
        'logger_attemptlog.csv': {'dataset_id': dataset_replacements, '_morango_partition': dataset_replacements},
        'logger_contentsessionlog.csv': {'dataset_id': dataset_replacements, '_morango_partition': dataset_replacements},
        'logger_contentsummarylog.csv': {'dataset_id': dataset_replacements, '_morango_partition': dataset_replacements},
        'logger_masterylog.csv': {'dataset_id': dataset_replacements, '_morango_partition': dataset_replacements},
        'logger_usersessionlog.csv': {'dataset_id': dataset_replacements, '_morango_partition': dataset_replacements}
    }

    for csv_file, columns in csv_files.items():
        file_path = os.path.expanduser('~/{0}'.format(csv_file))
        replace_ids_in_csv(file_path, columns)

if __name__ == '__main__':
    main()
