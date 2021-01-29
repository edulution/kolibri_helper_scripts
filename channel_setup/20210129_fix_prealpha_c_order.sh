#!/bin/bash
# Fix the bug with Pre-Alpha C - Measurement and Geometry (Content not ordered on Kolibri Studio)
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h "$KOLIBRI_DATABASE_HOST" -U "$KOLIBRI_DATABASE_USER" -d "$KOLIBRI_DATABASE_NAME" -p "$KOLIBRI_DATABASE_PORT" -a -f ~/.kolibri_helper_scripts/sql/20210129_fix_prealpha_c_measurement_and_geometry.sql
