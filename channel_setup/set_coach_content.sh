#!/bin/bash

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  echo "NAME"
  echo " set_coach_content - Set Coach conent"
  echo
  echo "DESCRIPTION"
  echo "   Makes Coach Professional Development channel only available to Coaches "
  echo
  echo "Example"
  echo " ./set_coach_content.sh "
  exit 1
fi

# Run the set coach content sql on the kolibri database
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql \
-h "$KOLIBRI_DATABASE_HOST" \
-U "$KOLIBRI_DATABASE_USER" \
-d "$KOLIBRI_DATABASE_NAME" \
-a -f ~/.kolibri_helper_scripts/sql/set_coach_content.sql
