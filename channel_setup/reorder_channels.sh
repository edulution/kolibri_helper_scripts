#!/bin/bash

# export the python path

# Order the channels to have Level 1 - Section 1 appearing first and Coach Professional Development last

python -m kolibri manage setchannelposition d8d0a31d-b57e-44a8-a956-4a7c6b1f6368 1 # Level 1 Section 1
python -m kolibri manage setchannelposition 14ba8f9f-3fc5-4f03-84f4-93a77b07ac1e 2 # Level 1 Section 2
python -m kolibri manage setchannelposition da831fef-8ade-4759-a112-6a6120e92210 3 # Level 1 Section 3
python -m kolibri manage setchannelposition 27939b34-516c-4e09-b86f-9abc5f7746c0 4 # Level 1 Section 4
python -m kolibri manage setchannelposition cab0fe89-ddc8-41df-bd40-e1c279df86de 5 # Level 2 Section 1
python -m kolibri manage setchannelposition 76453bfd-a059-4b31-8c2e-2da87febce97 6 # Level 2 Section 2
python -m kolibri manage setchannelposition fb2ca0b1-ca55-4a04-9f2e-5884564e2d23 7 # Level 2 Section 3
python -m kolibri manage setchannelposition dbb67c5d-fec8-4e66-8753-c469583e93f2 8 # Level 2 Section 4
python -m kolibri manage setchannelposition 4f1079f9-438a-4d5d-88d9-2d91ab0911a4 9 # Level 3 Section 1
python -m kolibri manage setchannelposition 514cf2b4-4b66-4dbe-9446-558d73868c0f 10 # Level 3 Section 2
python -m kolibri manage setchannelposition 04621abf-99d6-400a-b00e-2a8f9924ee48 11 # Level 3 Section 3
python -m kolibri manage setchannelposition 480741a8-686c-451b-9d15-2b960b53a5c8 12 # Level 3 Section 4
python -m kolibri manage setchannelposition ca07ea33-dc4d-4a0e-aba9-73898e85577b 13 # Level 4 Section 1
python -m kolibri manage setchannelposition e80e29b8-abe6-4997-9143-a3ae0c1a27dc 14 # Level 4 Section 2
python -m kolibri manage setchannelposition 6b40757c-6266-4e75-9e4f-39808529b21c 15 # Level 4 Section 3
python -m kolibri manage setchannelposition c1ab61ba-d631-4ee7-aa7a-dbdcbd217be2 16 # Level 4 Section 4
python -m kolibri manage setchannelposition 8eea5e9d-0435-47bc-ace0-1f35959a91ec 17 # Level 5 Section 1
python -m kolibri manage setchannelposition ff5782ff-a9bd-4ee2-80a2-72ab13653f97 18 # Level 5 Section 2
python -m kolibri manage setchannelposition 960e361c-be5e-4f5f-a3d1-39724a8cb18d 19 # Level 5 Section 3
python -m kolibri manage setchannelposition cad83700-eba4-4450-9dd1-234655fc6670 20 # Level 5 Section 4
python -m kolibri manage setchannelposition cf1b82ba-1452-4cf7-8a08-ce8c01626b28 21 # Level 6 Section 1
python -m kolibri manage setchannelposition b21103bd-85f6-4e18-b6a6-e4cb50665386 22 # Level 6 Section 2
python -m kolibri manage setchannelposition 20e95963-caea-4ab5-ac50-5c60f3c5a5bb 23 # Level 6 Section 3
python -m kolibri manage setchannelposition 1ab4e328-7ce7-45ee-9166-bb13021a3b55 24 # Level 6 Section 4


echo "Successfully reordered channels"


