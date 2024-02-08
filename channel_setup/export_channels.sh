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


# Export channels to a specified directory
export_channels(){
	# Directory to export the channels to
	EXPORT_DIR=$1
	
	# Declare array containing all channel_ids
	declare -a channel_ids=(
		"319c8b3a7b8c41e1ae542163228bf38f"
		"3a3d5063da77418f8139ae17e4cddab0"
		"ea4c6ee308b7457e8af0c5e9ea0fbf93"
		"d36d2bf4ed5f45fbb254896552dca2da"
		"dcd8318809ab4d12b3e26008a35680cf"
		"4b46d72f0122482682e2a4da47ad7b3e"
		"aaa9cebbc6bf4a6d88f745b1f260988a"
		"9236e970deb6469595972119700a4506"
		"547800a20c60493988f8135500654e69"
		"35cccf14d93445f08e00823727af4ddf"
		"4f4c4a2ff9984526a2d3b5ce5f3df78a"
		"5d2577d999664724844008449f3b3e23"
		"d50aec3616f444a3b7313cd2b264535e"
		"47957429f8324eb7919640e3023c06f8"
		"07a3ba7d59db47d1b7b5c78ea2c896d3"
		"df11dd6aea8f4591ad02bd58fbb4cb63"
		"c9b60dc13c184288b77880976df822f3"
		"348ee296a88a4eb8b6b103443a6e16e6"
		"d9d4d1f701d24b35be2cd4e78e2074e6"
		"a33d75c6527143ceb21310fa74882b98"
		"cf1b82ba14524cf78a08ce8c01626b28"
		"b21103bd85f64e18b6a6e4cb50665386"
		"20e95963caea4ab5ac505c60f3c5a5bb"
		"1ab4e3287ce745ee9166bb13021a3b55"
		"4c5f286c4d4c473abff55402a6cf0f9e"
		"8d368058656544e2b7fe62eb2a632698"
		"19ea4c94ee484cb0b5bb617f5511f4c1"
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
CONTENT_PACK_DIR=${1:-'~/new_kolibri_content_pack/KOLIBRI_DATA/'}

# If the content pack directory does not exist, create it
if [ ! -d "$CONTENT_PACK_DIR" ]; then
	mkdir -p "$CONTENT_PACK_DIR"
	echo "Creating directory : $CONTENT_PACK_DIR"
else
	echo "${BLUE}$CONTENT_PACK_DIR already exists. Skipping this step${RESET}"
fi

# Run the export channels function passing in the content pack directory
export_channels $CONTENT_PACK_DIR

