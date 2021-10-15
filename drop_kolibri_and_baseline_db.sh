#!/bin/bash

# Drop and recreate baseline testing and kolibri databases
sudo -i -u postgres psql <<-EOF
	drop database baseline_testing;
	drop database kolibri;
	create database baseline_testing;
	create database kolibri;
EOF