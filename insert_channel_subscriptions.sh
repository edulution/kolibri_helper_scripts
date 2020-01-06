#!/bin/bash
PGPASSWORD=TestL0cal psql -h localhost -U baseline_testing -d baseline_testing_swap -a -f channel_subscriptions.sql
