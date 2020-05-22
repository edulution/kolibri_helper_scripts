#!/bin/bash
# Run the missing prerequisites into the kolibri database
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h "$KOLIBRI_DATABASE_HOST" -U "$KOLIBRI_DATABASE_USER" -d "$KOLIBRI_DATABASE_NAME" -a -f ../sql/insert_prerequisites.sql