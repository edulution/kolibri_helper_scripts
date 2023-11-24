#!/bin/bash

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  echo "NAME"
  echo "  create_channel_module -  Create channel module table"
  echo
  echo "DESCRIPTION"
  echo "  Create and populate the channel module table on kolibri database"
  echo 
  echo "Example"
  echo " ./create_channel_module.sh"
  exit 1
fi

# create and populate the channel module table on kolibri database
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql \
-h "$KOLIBRI_DATABASE_HOST" \
-U "$KOLIBRI_DATABASE_USER" \
-d "$KOLIBRI_DATABASE_NAME" \
-a -f ~/.kolibri_helper_scripts/sql/channel_module.sql
