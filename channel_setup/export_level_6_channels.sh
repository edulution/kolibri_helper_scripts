#!/bin/bash

# Export channels to a specified directory
export_channels(){
	# Directory to export the channels to
	EXPORT_DIR=$1
	
	# Declare array containing all channel_ids
	declare -a channel_ids=(
		"1ab4e3287ce745ee9166bb13021a3b55"
		"20e95963caea4ab5ac505c60f3c5a5bb"
		"b21103bd85f64e18b6a6e4cb50665386"
		"cf1b82ba14524cf78a08ce8c01626b28"
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
CONTENT_PACK_DIR=~/level6_content/KOLIBRI_DATA/

# If the content pack directory does not exist, create it
if [ ! -d "$CONTENT_PACK_DIR" ]; then
	mkdir -p "$CONTENT_PACK_DIR"
	echo "Creating directory : $CONTENT_PACK_DIR"
else
	echo "${BLUE}$CONTENT_PACK_DIR already exists. Skipping this step${RESET}"
fi

# Run the export channels function passing in the content pack directory
export_channels $CONTENT_PACK_DIR

