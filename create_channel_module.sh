#!/bin/bash
# create and populate the channel module table on kolibri database
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -a -f sql/channel_module.sql
