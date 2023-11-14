#!/bin/bash

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  echo "NAME"
  echo "  assign_learners - Assign Learners to appropriate groups"
  echo
  echo "DESCRIPTION"
  echo "  Updates the subscriptions on each group and classroom, generate all content "
  echo "  prerequisites and assign live learners into appropriate groups"
  echo 
  echo "Example"
  echo
  echo "  ./assign_learners.sh"
  exit 1
fi

# update the subscriptions on each of the groups in case they were modified
~/.kolibri_helper_scripts/channel_setup/insert_channel_subscriptions.sh

# Generate prerequisites on all channels if they do not exist
Rscript ~/.kolibri_helper_scripts/channel_setup/generate_prereqs.R

# get the live learners/coaches and insert them into the live learners table
python ~/.kolibri_helper_scripts/get_live_learners.py

# call the procedure to assign them into the appropriate groups
PGPASSWORD=$BASELINE_DATABASE_PASSWORD psql \
-h "$BASELINE_DATABASE_HOST" \
-U "$BASELINE_DATABASE_USER" \
-d "$BASELINE_DATABASE_NAME" \
-c "call spassignmembership('numeracy');"