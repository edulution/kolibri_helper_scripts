#!/bin/bash

# channel_ids
#==============
# Level 1 - Section 1 - 547800a20c60493988f8135500654e69
# Level 1 - Section 2 - d50aec3616f444a3b7313cd2b264535e
# Level 1 - Section 3 - 5d2577d999664724844008449f3b3e23
# Level 1 - Section 4 - 4b46d72f0122482682e2a4da47ad7b3e
# Level 2 - Section 1 - a33d75c6527143ceb21310fa74882b98
# Level 2 - Section 2 - 4f4c4a2ff9984526a2d3b5ce5f3df78a
# Level 2 - Section 3 - 319c8b3a7b8c41e1ae542163228bf38f
# Level 2 - Section 4 - 35cccf14d93445f08e00823727af4ddf
# Level 3 - Section 1 - 9236e970deb6469595972119700a4506
# Level 3 - Section 2 - 348ee296a88a4eb8b6b103443a6e16e6
# Level 3 - Section 3 - 3a3d5063da77418f8139ae17e4cddab0
# Level 3 - Section 4 - d9d4d1f701d24b35be2cd4e78e2074e6
# Level 4 - Section 1 - aaa9cebbc6bf4a6d88f745b1f260988a
# Level 4 - Section 2 - dcd8318809ab4d12b3e26008a35680cf
# Level 4 - Section 3 - c9b60dc13c184288b77880976df822f3
# Level 4 - Section 4 - df11dd6aea8f4591ad02bd58fbb4cb63
# Level 5 - Section 1 - d36d2bf4ed5f45fbb254896552dca2da
# Level 5 - Section 2 - 07a3ba7d59db47d1b7b5c78ea2c896d3
# Level 5 - Section 3 - 47957429f8324eb7919640e3023c06f8
# Level 5 - Section 4 - ea4c6ee308b7457e8af0c5e9ea0fbf93
# Level 6 Section 1 - cf1b82ba14524cf78a08ce8c01626b28
# Level 6 Section 2 - b21103bd85f64e18b6a6e4cb50665386
# Level 6 Section 3 - 20e95963caea4ab5ac505c60f3c5a5bb
# Level 6 Section 4 - 1ab4e3287ce745ee9166bb13021a3b55
# Grade 7 Numeracy (Zambia) - 8d368058656544e2b7fe62eb2a632698
# Grade 7 Literacy (Zambia) - 96578ffc06e44a46b021540cb217f9c9
# Coach Professional Development - 19ea4c94ee484cb0b5bb617f5511f4c1


# Default directory to look for Kolibri content
DEFAULT_CONTENT_DIR=/opt/KOLIBRI_DATA/

import_channels_local(){
	# Use the directory passed in or the default directory if no argument is passed in
	CONTENT_DIR=${1:-$DEFAULT_CONTENT_DIR}

	# Declare array containing all channel_ids
	declare -a channel_ids=(
		"547800a20c60493988f8135500654e69"
		"d50aec3616f444a3b7313cd2b264535e"
		"5d2577d999664724844008449f3b3e23"
		"4b46d72f0122482682e2a4da47ad7b3e"
		"a33d75c6527143ceb21310fa74882b98"
		"4f4c4a2ff9984526a2d3b5ce5f3df78a"
		"319c8b3a7b8c41e1ae542163228bf38f"
		"35cccf14d93445f08e00823727af4ddf"
		"9236e970deb6469595972119700a4506"
		"348ee296a88a4eb8b6b103443a6e16e6"
		"3a3d5063da77418f8139ae17e4cddab0"
		"d9d4d1f701d24b35be2cd4e78e2074e6"
		"aaa9cebbc6bf4a6d88f745b1f260988a"
		"dcd8318809ab4d12b3e26008a35680cf"
		"c9b60dc13c184288b77880976df822f3"
		"df11dd6aea8f4591ad02bd58fbb4cb63"
		"d36d2bf4ed5f45fbb254896552dca2da"
		"07a3ba7d59db47d1b7b5c78ea2c896d3"
		"47957429f8324eb7919640e3023c06f8"
		"ea4c6ee308b7457e8af0c5e9ea0fbf93"
		"cf1b82ba14524cf78a08ce8c01626b28"
		"b21103bd85f64e18b6a6e4cb50665386"
		"20e95963caea4ab5ac505c60f3c5a5bb"
		"1ab4e3287ce745ee9166bb13021a3b55"
		"4c5f286c4d4c473abff55402a6cf0f9e"
		"8d368058656544e2b7fe62eb2a632698"
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

import_channels_local "$1"





