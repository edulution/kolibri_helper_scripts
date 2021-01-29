#!/bin/bash

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
# Grade 7 (Zambia) - 8d368058656544e2b7fe62eb2a632698
# Coach Professional Development (Old) - 2c8cd5f3a4694adbb4be45025d9ca3dc
# Coach Professional Development - 19ea4c94ee484cb0b5bb617f5511f4c1



# Export channels to a specified directory
export_channels(){
	# Directory to export the channels to
	EXPORT_DIR=$1
	
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
		#"19ea4c94ee484cb0b5bb617f5511f4c1"
		)

	# Inform the user that the exporting has begun
	echo "Begin exporting Kolibri channels to $EXPORT_DIR"

	# To export channels individually, 
	# run the two lines as below and insert the appropriate channel_id e.g
	# python -m kolibri manage exportchannel -- network <channel_id>
	# python -m kolibri manage exportchannel -- network <channel_id>

	# Loop through channel_ids array
	for channel in "${channel_ids[@]}"
	do
		# For each channel, always exportchannel before exportcontent
		python -m kolibri manage exportchannel "$channel" "$EXPORT_DIR"
		python -m kolibri manage exportcontent "$channel" "$EXPORT_DIR"
	done

	echo "${GREEN}Done!${RESET}"
}


# Path to the content pack directory
CONTENT_PACK_DIR=~/new_kolibri_content_pack/KOLIBRI_DATA/

# If the content pack directory does not exist, create it
if [ ! -d "$CONTENT_PACK_DIR" ]; then
	mkdir -p "$CONTENT_PACK_DIR"
	echo "Creating directory : $CONTENT_PACK_DIR"
else
	echo "${BLUE}$CONTENT_PACK_DIR already exists. Skipping this step${RESET}"
fi

# Run the export channels function passing in the content pack directory
export_channels $CONTENT_PACK_DIR

