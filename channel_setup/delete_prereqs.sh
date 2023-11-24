#!/bin/bash


if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  echo "NAME"
  echo "  delete_prereqs - Delete channel prerequisites"
  echo
  echo "DESCRIPTION"
  echo "  Deletes all numeracy channel prerequisites"
  echo 
  echo "Example"
  echo " ./delete_prereqs.sh"
  exit 1
fi

# Delete all content prerequisites
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql \
  -h "$KOLIBRI_DATABASE_HOST" \
  -U "$KOLIBRI_DATABASE_USER" \
  -d "$KOLIBRI_DATABASE_NAME" \
  -p "$KOLIBRI_DATABASE_PORT" \
  -c "DELETE FROM content_contentnode_has_prerequisite;"
