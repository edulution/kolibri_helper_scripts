#!/bin/bash

# Script to delete all numeracy channels from a device

# channel_ids
#==============
# Pre Alpha A - 3d6c9d72a2e047d4b7a0ed20699e1b1f
# Pre Alpha B - 6380a6a98a4c4b268b3147ad1c7ada13
# Pre Alpha C - 20113bf1ba074e08bcc7faaca03ade8a
# Pre Alpha D - 1700bf9e71094857abf36c04a1963004
# Alpha A - 8784b9f78d584273aff579b246529215
# Alpha B - cc80537886cb498eb564242f44c87723
# Alpha C - 7035e7921ddf489fad4544c814a199fb
# Alpha D - 1d8f1428da334779b95685c4581186c4
# Bravo A - 57995474194c4068bfed1ee16108093f
# Bravo B - b7214b921fd94a1cb758821919bcd3e0
# Bravo C - 5aee4435135b4039a3a824d96f72bfcb
# Bravo D - 98ab8048107545da92e3394409955526
# Grade 7 Numeracy (Zambia) - 8d368058656544e2b7fe62eb2a632698
# Grade 7 Literacy (Zambia) - 96578ffc06e44a46b021540cb217f9c9
# Coach Professional Development - 19ea4c94ee484cb0b5bb617f5511f4c1


delete_channels(){
	
	# Declare array containing all channel_ids
	declare -a channel_ids=(
		"3d6c9d72a2e047d4b7a0ed20699e1b1f"
		"6380a6a98a4c4b268b3147ad1c7ada13"
		"20113bf1ba074e08bcc7faaca03ade8a"
		"1700bf9e71094857abf36c04a1963004"
		"8784b9f78d584273aff579b246529215"
		"cc80537886cb498eb564242f44c87723"
		"7035e7921ddf489fad4544c814a199fb"
		"1d8f1428da334779b95685c4581186c4"
		"57995474194c4068bfed1ee16108093f"
		"b7214b921fd94a1cb758821919bcd3e0"
		"5aee4435135b4039a3a824d96f72bfcb"
		"98ab8048107545da92e3394409955526"
		"8d368058656544e2b7fe62eb2a632698"
		"19ea4c94ee484cb0b5bb617f5511f4c1"
		"96578ffc06e44a46b021540cb217f9c9"
		"2c8cd5f3a4694adbb4be45025d9ca3dc"
		
		)

	# Inform the user that the deletion has begun
	echo "Deleting all channels"

	# To delete channels individually, 
	# run the line below and insert the appropriate channel_id e.g
	# python -m kolibri manage deletechannel <channel_id>

	# Loop through channel_ids array
	for channel in "${channel_ids[@]}"
	do
		# For each channel, delete by channel_id
		python -m kolibri manage deletechannel "$channel"
	done

	echo "Done!"
}

delete_channels
