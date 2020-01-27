#!/bin/bash
# Run the channel subscriptions sql on the kolibri database
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -a -f ~/.kolibri_helper_scrips/sql/channel_subscriptions.sql
