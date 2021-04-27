# WIP
# Restore users from a past backup
# or transfer users from one database to another (remember to update facility_id)

# extract rows from backup
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY ( select * from kolibriauth_facilityuser where id in () ) TO STDOUT WITH CSV HEADER " > ~/kolibriauth_facilityuser.csv
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY ( select * from logger_attemptlog where user_id in () ) TO STDOUT WITH CSV HEADER" > ~/logger_attemptlog.csv
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY ( select * from logger_contentsessionlog where user_id in () ) TO STDOUT WITH CSV HEADER" > ~/logger_contentsessionlog.csv
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY ( select * from logger_contentsummarylog where user_id in () ) TO STDOUT WITH CSV HEADER" > ~/logger_contentsummarylog.csv
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY ( select * from logger_examattemptlog where user_id in () ) TO STDOUT WITH CSV HEADER" > ~/logger_examattemptlog.csv
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY ( select * from logger_examlog where user_id in () ) TO STDOUT WITH CSV HEADER" > ~/logger_examlog.csv
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY ( select * from logger_masterylog where user_id in () ) TO STDOUT WITH CSV HEADER" > ~/logger_masterylog.csv
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY ( select * from logger_usersessionlog where user_id in () ) TO STDOUT WITH CSV HEADER" > ~/logger_usersessionlog.csv

# insert rows into live database
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY kolibriauth_facilityuser FROM '~/kolibriauth_facilityuser.csv' DELIMITER ',' CSV HEADER;"
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY logger_attemptlog FROM '~/logger_attemptlog.csv' DELIMITER ',' CSV HEADER;"
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY logger_contentsessionlog FROM '~/logger_contentsessionlog.csv' DELIMITER ',' CSV HEADER;"
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY logger_contentsummarylog FROM '~/logger_contentsummarylog.csv' DELIMITER ',' CSV HEADER;"
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY logger_examattemptlog FROM '~/logger_examattemptlog.csv' DELIMITER ',' CSV HEADER;"
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY logger_examlog FROM '~/logger_examlog.csv' DELIMITER ',' CSV HEADER;"
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY logger_masterylog FROM '~/logger_masterylog.csv' DELIMITER ',' CSV HEADER;"
PGPASSWORD=$KOLIBRI_DATABASE_PASSWORD psql -h $KOLIBRI_DATABASE_HOST -U $KOLIBRI_DATABASE_USER -d $KOLIBRI_DATABASE_NAME -c "COPY logger_usersessionlog FROM '~/logger_usersessionlog.csv' DELIMITER ',' CSV HEADER;"
