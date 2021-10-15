#!/bin/bash

# function to drop and recreate the baseline database then restore the supplied backup file
restore_baseline_backup(){
	echo "Restoring backup file: $1 into Database: $BASELINE_DATABASE_NAME"
	PGPASSWORD=$BASELINE_DATABASE_PASSWORD pg_restore -U "$BASELINE_DATABASE_USER" -h "$BASELINE_DATABASE_HOST" -p "$BASELINE_DATABASE_PORT" -d "$BASELINE_DATABASE_NAME" --clean --create --no-owner "$1"
}

restore_kolibri_backup "$1"
