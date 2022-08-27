#!/bin/bash

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  echo "NAME"
  echo "	restore_backup - Restore Kolibri and Basline backup"
  echo
  echo "SYNOPSIS"
  echo "	./restore_backup [path /to /Kolibri backup] [path /to /Basline backup] ... [NO DB's]"
  echo
  echo "DESCRIPTION"
  echo "	Drops and recreates both Kolibri and Basline databases."
  echo "	The script terminates all active connections to both Kolibri and Basline dbs."
  echo "	This disconnects any leaners who might be logged in or submitting tests"
  echo ""
  echo "NOTE"
  echo "	With no dbs, the script drops and recreates empty Kolibri and Basline databases"
  echo "	Always backup before runing the script"
  echo 
  echo "Examples"
  echo
  echo "	./restore_backup "
  echo "	./restore_backup xxx_kolibri_20220517.backup"
  echo "	./restore_backup xxx_kolibri_20220517.backup xxx_baseline_20220517.backup"
  exit 1
fi
# function to drop and recreate the kolibri database then restore the supplied backup file
restore_database_backups(){

# Assign the args to variables
kolibri_backup_file=$1
baseline_backup_file=$2

# Stop forever
forever stopall

# Stop kolibri
kolibri stop

# Terminate all active connections to both Kolibri and Basline dbs
PGPASSWORD=$BASELINE_DATABASE_PASSWORD psql \
-h "$BASELINE_DATABASE_HOST" \
-U "$BASELINE_DATABASE_USER" \
-d "$BASELINE_DATABASE_NAME" \
-c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$BASELINE_DATABASE_NAME' AND pid <> pg_backend_pid()";
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql \
-h "$KOLIBRI_DATABASE_HOST" \
-U "$KOLIBRI_DATABASE_USER" \
-d "$KOLIBRI_DATABASE_NAME" \
-c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$KOLIBRI_DATABASE_NAME' AND pid <> pg_backend_pid()";


# Drop and recreate kolibri and baseline databases
sudo -i -u postgres psql << EOF
	drop database kolibri;
	create database kolibri;
	drop database baseline_testing;
	create database baseline_testing;
	grant all on database baseline_testing to baseline_testing;
EOF

# Restore the kolibri backup into the kolibri db. get credentials from env variables
	echo "Restoring backup file: $1 into Database: $KOLIBRI_DATABASE_NAME"
	PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD 
	pg_restore -U "$KOLIBRI_DATABASE_USER" \
	-h "$KOLIBRI_DATABASE_HOST" \
	-p "$KOLIBRI_DATABASE_PORT" \
	-d "$KOLIBRI_DATABASE_NAME" \
	--no-owner --verbose "$kolibri_backup_file"

# Restore the kolibri backup into the kolibri db. get credentials from env variables
	echo "Restoring backup file: $2 into Database: $BASELINE_DATABASE_NAME"
	PGPASSWORD=$BASELINE_DATABASE_PASSWORD
	pg_restore -U "$BASELINE_DATABASE_USER" \
	-h "$BASELINE_DATABASE_HOST" \
	-p "$BASELINE_DATABASE_PORT" \
	-d "$BASELINE_DATABASE_NAME" \
	--no-owner --verbose "$baseline_backup_file"
}

restore_database_backups "$1" "$2"
