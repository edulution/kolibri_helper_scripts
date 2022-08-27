#!/bin/bash

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  echo "NAME"
  echo "  insert_channel_subscriptions -  Insert numeracy channel subscription"
  echo
  echo "DESCRIPTION"
  echo "  Inserts subscription for each channel level using the channel subscriptions sql script."
  echo 
  echo "Example"
  echo " ./insert_channel_subscriptions.sh"
  exit 1
fi

# Run the channel subscriptions sql on the kolibri database
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h "$KOLIBRI_DATABASE_HOST" -U "$KOLIBRI_DATABASE_USER" -d "$KOLIBRI_DATABASE_NAME" -a -f ~/.kolibri_helper_scripts/sql/channel_subscriptions.sql

