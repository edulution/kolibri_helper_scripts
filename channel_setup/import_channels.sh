#!/bin/bash

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  echo "NAME"
  echo "  import_channels - Import numeracy channels"
  echo
  echo "SYNOPSIS"
  echo "  ./import_channels.sh"
  echo
  echo "DESCRIPTION"
  echo "  The script imports all numeracy channels from the local content pack stored"
  echo "  on a device in the /opt directory" 
  echo
  echo "Examples"
  echo " ./import_channels.sh"
  echo "	Imports all numeracy channels"
  echo
  echo "  ./import_channels.sh ~/KOLIBRI_DATA"
  echo "	Imports numeracy channels from the KOLIBRI_DATA directory"
  exit 1
fi

# channel_ids
#==============
# Level 1 Section 1 - f3f6bf4b9c424b6fbd90bece1418a415
# Level 1 Section 2 - 3a126f041a9e4127978bb6544a099d0d
# Level 1 Section 3 - 03761fe9a2424e9ebd367fbae14dc134
# Level 1 Section 4 - f12e2f67d5894b34bb942484d880c4a6
# Level 2 Section 1 - f6e8f1f569c54bc58ecb54d826cd3783
# Level 2 Section 2 - 5126a907e5284345847c8ca749c8cd9b
# Level 2 Section 3 - c32737bf26474dc8a81de3d093075830
# Level 2 Section 4 - 0985900c047a41738e796f19d9b57ed5
# Level 3 Section 1 - c0302f6cd0624778bc8dd7a2b91d09b4
# Level 3 Section 2 - ddf25e8fcde84e8998118daffb2d8655
# Level 3 Section 3 - e2217b872f784190a0a55c46e9ee8bc1
# Level 3 Section 4 - f908fac9fe5644b996abe25dfbd530bc
# Level 4 Section 1 - d4b44e6dd4de450ebbc799085ba656e5
# Level 4 Section 2 - 763eafc24e684dbe8f54c9a22dd63599
# Level 4 Section 3 - 7de1d8eca4874856b508c1a4f51a839e
# Level 4 Section 4 - 904d419f53e24b6fb60d2aca7e729683
# Level 5 Section 1 - 5b679315a02c40359505fc84701c482d
# Level 5 Section 2 - a5cd9f9f000e41459a95875d7dfd3e68
# Level 5 Section 3 - 6c4089232a72447eabbdf83b7c5612a4
# Level 5 Section 4 - 28f4920a7b444e29af4f1e8d00ca332b
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
		"f3f6bf4b9c424b6fbd90bece1418a415"
		"3a126f041a9e4127978bb6544a099d0d"
		"03761fe9a2424e9ebd367fbae14dc134"
		"f12e2f67d5894b34bb942484d880c4a6"
		"f6e8f1f569c54bc58ecb54d826cd3783"
		"5126a907e5284345847c8ca749c8cd9b"
		"c32737bf26474dc8a81de3d093075830"
		"0985900c047a41738e796f19d9b57ed5"
		"c0302f6cd0624778bc8dd7a2b91d09b4"
		"ddf25e8fcde84e8998118daffb2d8655"
		"e2217b872f784190a0a55c46e9ee8bc1"
		"f908fac9fe5644b996abe25dfbd530bc"
		"d4b44e6dd4de450ebbc799085ba656e5"
		"763eafc24e684dbe8f54c9a22dd63599"
		"7de1d8eca4874856b508c1a4f51a839e"
		"904d419f53e24b6fb60d2aca7e729683"
		"5b679315a02c40359505fc84701c482d"
		"a5cd9f9f000e41459a95875d7dfd3e68"
		"6c4089232a72447eabbdf83b7c5612a4"
		"28f4920a7b444e29af4f1e8d00ca332b"
		"8d368058656544e2b7fe62eb2a632698"
		"19ea4c94ee484cb0b5bb617f5511f4c1"
		"cf1b82ba14524cf78a08ce8c01626b28"
		"b21103bd85f64e18b6a6e4cb50665386"
		"20e95963caea4ab5ac505c60f3c5a5bb"
		"1ab4e3287ce745ee9166bb13021a3b55"
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