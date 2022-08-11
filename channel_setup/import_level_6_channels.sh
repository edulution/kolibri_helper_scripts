#!/bin/bash

# channel_ids
#==============
# Level 6 Section 1 - cf1b82ba14524cf78a08ce8c01626b28
# Level 6 Section 2 - b21103bd85f64e18b6a6e4cb50665386
# Level 6 Section 3 - 20e95963caea4ab5ac505c60f3c5a5bb
# Level 6 Section 4 - 1ab4e3287ce745ee9166bb13021a3b55


# Default directory to look for Kolibri content
DEFAULT_CONTENT_DIR=/opt/KOLIBRI_DATA/

import_level_six_local(){
	# Use the directory passed in or the default directory if no argument is passed in
	CONTENT_DIR=${1:-$DEFAULT_CONTENT_DIR}

	# Declare array containing all channel_ids
	declare -a channel_ids=(
        "1ab4e3287ce745ee9166bb13021a3b55"
        "20e95963caea4ab5ac505c60f3c5a5bb"
        "b21103bd85f64e18b6a6e4cb50665386"
        "cf1b82ba14524cf78a08ce8c01626b28"
		)

	# Inform the user that the importing has begun
	echo "Importing numeracy playlists from local storage directory : $CONTENT_DIR"

	# To import channels individually, 
	# run the two lines as below and insert the appropriate channel_id and content directory e.g
	# python -m kolibri manage importchannel -- disk <channel_id> <content directory>
	# python -m kolibri manage importcontent -- disk <channel_id> <content directory>

	# Loop through channel_ids array
	for channel in "${channel_ids[@]}"
	do
		# For each channel, always importchannel before importcontent
		python -m kolibri manage importchannel -- disk "$channel" "$CONTENT_DIR"
		python -m kolibri manage importcontent -- disk "$channel" "$CONTENT_DIR"
	done

	echo "Done!"
}

import_level_six_local "$1"