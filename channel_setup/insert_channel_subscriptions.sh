#!/bin/bash
# Run the channel subscriptions sql on the kolibri database
# Check if a centre gives literacy lessons using the environment variable IS_LITERACY_CENTRE
# Then run the appropriate SQL script to update the channel channel subscriptions

if [[ "$IS_LITERACY_CENTRE" == "TRUE" ]]; then
	PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h "$KOLIBRI_DATABASE_HOST" -U "$KOLIBRI_DATABASE_USER" -d "$KOLIBRI_DATABASE_NAME" -a -f ~/.kolibri_helper_scripts/sql/channel_subscriptions_lit.sql
else
	PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h "$KOLIBRI_DATABASE_HOST" -U "$KOLIBRI_DATABASE_USER" -d "$KOLIBRI_DATABASE_NAME" -a -f ~/.kolibri_helper_scripts/sql/channel_subscriptions.sql
fi

