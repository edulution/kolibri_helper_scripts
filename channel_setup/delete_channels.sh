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


# SA channel_ids
#==============
# Level 1 - Section 1 - d8d0a31db57e44a8a9564a7c6b1f6368
# Level 1 - Section 2 - 14ba8f9f3fc54f0384f493a77b07ac1e
# Level 1 - Section 3 - da831fef8ade4759a1126a6120e92210
# Level 1 - Section 4 - 27939b34516c4e09b86f9abc5f7746c0
# Level 2 - Section 1 - cab0fe89ddc841dfbd40e1c279df86de
# Level 2 - Section 2 - 76453bfda0594b318c2e2da87febce97
# Level 2 - Section 3 - fb2ca0b1ca554a049f2e5884564e2d23
# Level 2 - Section 4 - dbb67c5dfec84e668753c469583e93f2
# Level 3 - Section 1 - 4f1079f9438a4d5d88d92d91ab0911a4
# Level 3 - Section 2 - 514cf2b44b664dbe9446558d73868c0f
# Level 3 - Section 3 - 04621abf99d6400ab00e2a8f9924ee48
# Level 3 - Section 4 - 480741a8686c451b9d152b960b53a5c8
# Level 4 - Section 1 - ca07ea33dc4d4a0eaba973898e85577b
# Level 4 - Section 2 - e80e29b8abe649979143a3ae0c1a27dc
# Level 4 - Section 3 - 6b40757c62664e759e4f39808529b21c
# Level 4 - Section 4 - c1ab61bad6314ee7aa7adbdcbd217be2
# Level 5 - Section 1 - 8eea5e9d043547bcace01f35959a91ec
# Level 5 - Section 2 - ff5782ffa9bd4ee280a272ab13653f97
# Level 5 - Section 3 - 960e361cbe5e4f5fa3d139724a8cb18d
# Level 5 - Section 4 - cad83700eba444509dd1234655fc6670
# Level 6 Section 1 - cf1b82ba14524cf78a08ce8c01626b28
# Level 6 Section 2 - b21103bd85f64e18b6a6e4cb50665386
# Level 6 Section 3 - 20e95963caea4ab5ac505c60f3c5a5bb
# Level 6 Section 4 - 1ab4e3287ce745ee9166bb13021a3b55


# New Zambia channels
#---------------------
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
		"d8d0a31db57e44a8a9564a7c6b1f6368"
		"14ba8f9f3fc54f0384f493a77b07ac1e"
		"da831fef8ade4759a1126a6120e92210"
		"27939b34516c4e09b86f9abc5f7746c0"
		"cab0fe89ddc841dfbd40e1c279df86de"
		"76453bfda0594b318c2e2da87febce97"
		"fb2ca0b1ca554a049f2e5884564e2d23"
		"dbb67c5dfec84e668753c469583e93f2"
		"4f1079f9438a4d5d88d92d91ab0911a4"
		"514cf2b44b664dbe9446558d73868c0f"
		"04621abf99d6400ab00e2a8f9924ee48"
		"480741a8686c451b9d152b960b53a5c8"
		"ca07ea33dc4d4a0eaba973898e85577b"
		"e80e29b8abe649979143a3ae0c1a27dc"
		"6b40757c62664e759e4f39808529b21c"
		"c1ab61bad6314ee7aa7adbdcbd217be2"
		"8eea5e9d043547bcace01f35959a91ec"
		"ff5782ffa9bd4ee280a272ab13653f97"
		"960e361cbe5e4f5fa3d139724a8cb18d"
		"cad83700eba444509dd1234655fc6670"
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
