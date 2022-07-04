#!/bin/bash

# channel_ids
#==============
# Level 6 Section 1 - 1ab4e3287ce745ee9166bb13021a3b55
# Level 6 Section 2 - 20e95963caea4ab5ac505c60f3c5a5bb
# Level 6 Section 3 - b21103bd85f64e18b6a6e4cb50665386
# Level 6 Section 4 - cf1b82ba14524cf78a08ce8c01626b28



import_level_six(){
    
    # Declare array containing all channel_ids
    declare -a channel_ids=(
        "1ab4e3287ce745ee9166bb13021a3b55"
        "20e95963caea4ab5ac505c60f3c5a5bb"
        "b21103bd85f64e18b6a6e4cb50665386"
        "cf1b82ba14524cf78a08ce8c01626b28"
        )

    # Inform the user that the importing has begun
    echo "Importing numeracy playlists from the Internet"

    # To import channels individually, 
    # run the two lines as below and insert the appropriate channel_id e.g
    # python -m kolibri manage importchannel -- network <channel_id>
    # python -m kolibri manage importcontent -- network <channel_id>

    # Loop through channel_ids array
    for channel in "${channel_ids[@]}"
    do
        # For each channel, always importchannel before importcontent
        python -m kolibri manage importchannel -- network "$channel"
        python -m kolibri manage importcontent -- network "$channel"
    done
}

import_level_six