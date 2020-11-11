#!/bin/bash
# Run the set coach content sql on the kolibri database
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h "$KOLIBRI_DATABASE_HOST" -U "$KOLIBRI_DATABASE_USER" -d "$KOLIBRI_DATABASE_NAME" -a -f ~/.kolibri_helper_scripts/sql/set_coach_content.sql
