#!/bin/bash

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  echo "NAME"
  echo "  delete_channels - Delete numeracy channels"
  echo
  echo "SYNOPSIS"
  echo "  ./delete_channels.sh"
  echo
  echo "DESCRIPTION"
  echo "  The script deletes all numeracy channels from a device"
  echo 
  echo "Examples"
  echo " ./delete_channels.sh"
  echo "	Deletes all numeracy channels"
  echo
  exit 1
fi

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
# Coach Professional Development (Old) - 2c8cd5f3a4694adbb4be45025d9ca3dc
# Coach Professional Development - 19ea4c94ee484cb0b5bb617f5511f4c1

# Level 1 Section 1 - f3f6bf4b9c424b6fbd90bece1418a415
# Level 1 Section 2 - 3a126f041a9e4127978bb6544a099d0d
# Level 1 Section 3 - 03761fe9a2424e9ebd367fbae14dc134
# Level 1 Section 4 - f12e2f67d5894b34bb942484d880c4a6
# Level 2 Section 1 - f6e8f1f569c54bc58ecb54d826cd3783
# Level 2 Section 2 - 5126a907e5284345847c8ca749c8cd9b
# Level 2 Section 3 (old) - c32737bf26474dc8a81de3d093075830
# Level 2 Section 3 (new) - 521f889dc8634998b5542a526d428b85
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
		"96578ffc06e44a46b021540cb217f9c9"
		"2c8cd5f3a4694adbb4be45025d9ca3dc"
		"19ea4c94ee484cb0b5bb617f5511f4c1"
		"f3f6bf4b9c424b6fbd90bece1418a415"
		"3a126f041a9e4127978bb6544a099d0d"
		"03761fe9a2424e9ebd367fbae14dc134"
		"f12e2f67d5894b34bb942484d880c4a6"
		"f6e8f1f569c54bc58ecb54d826cd3783"
		"5126a907e5284345847c8ca749c8cd9b"
		"c32737bf26474dc8a81de3d093075830"
		"521f889dc8634998b5542a526d428b85"
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
		"cf1b82ba14524cf78a08ce8c01626b28"
		"b21103bd85f64e18b6a6e4cb50665386"
		"20e95963caea4ab5ac505c60f3c5a5bb"
		"1ab4e3287ce745ee9166bb13021a3b55"
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
