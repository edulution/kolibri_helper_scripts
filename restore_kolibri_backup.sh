#!/bin/bash

# function to drop and recreate the kolibri database then restore the supplied backup file
restore_kolibri_backup(){
	echo "Restoring backup file: $1 into Database: $KOLIBRI_DATABASE_NAME"
	PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD pg_restore -U "$KOLIBRI_DATABASE_USER" -h "$KOLIBRI_DATABASE_HOST" -p "$KOLIBRI_DATABASE_PORT" -d "$KOLIBRI_DATABASE_NAME" --clean --create --no-owner "$1"
}

restore_kolibri_backup "$1"
