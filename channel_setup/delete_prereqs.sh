#!/bin/bash
# Delete all content prerequisites
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h "$KOLIBRI_DATABASE_HOST" -U "$KOLIBRI_DATABASE_USER" -d "$KOLIBRI_DATABASE_NAME" -p "$KOLIBRI_DATABASE_PORT" -c "DELETE FROM content_contentnode_has_prerequisite;"
