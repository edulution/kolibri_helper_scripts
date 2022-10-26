#!/bin/bash

# export the python path

# Order the channels to have Level 1 - Section 1 appearing first and Coach Professional Development last

python -m kolibri manage setchannelposition f3f6bf4b-9c42-4b6f-bd90-bece1418a415 1 # Level 1 Section 1
python -m kolibri manage setchannelposition 3a126f04-1a9e-4127-978b-b6544a099d0d 2 # Level 1 Section 2
python -m kolibri manage setchannelposition 03761fe9-a242-4e9e-bd36-7fbae14dc134 3 # Level 1 Section 3
python -m kolibri manage setchannelposition f12e2f67-d589-4b34-bb94-2484d880c4a6 4 # Level 1 Section 4
python -m kolibri manage setchannelposition f6e8f1f5-69c5-4bc5-8ecb-54d826cd3783 5 # Level 2 Section 1
python -m kolibri manage setchannelposition 5126a907-e528-4345-847c-8ca749c8cd9b 6 # Level 2 Section 2
# python -m kolibri manage setchannelposition c32737bf-2647-4dc8-a81d-e3d093075830 7 # Level 2 Section 3
python -m kolibri manage setchannelposition 521f889d-c863-4998-b554-2a526d428b85 7 # Level 2 Section 3
python -m kolibri manage setchannelposition 0985900c-047a-4173-8e79-6f19d9b57ed5 8 # Level 2 Section 4
python -m kolibri manage setchannelposition c0302f6c-d062-4778-bc8d-d7a2b91d09b4 9 # Level 3 Section 1
python -m kolibri manage setchannelposition ddf25e8f-cde8-4e89-9811-8daffb2d8655 10 # Level 3 Section 2
python -m kolibri manage setchannelposition e2217b87-2f78-4190-a0a5-5c46e9ee8bc1 11 # Level 3 Section 3
python -m kolibri manage setchannelposition f908fac9-fe56-44b9-96ab-e25dfbd530bc 12 # Level 3 Section 4
python -m kolibri manage setchannelposition d4b44e6d-d4de-450e-bbc7-99085ba656e5 13 # Level 4 Section 1
python -m kolibri manage setchannelposition 763eafc2-4e68-4dbe-8f54-c9a22dd63599 14 # Level 4 Section 2
python -m kolibri manage setchannelposition 7de1d8ec-a487-4856-b508-c1a4f51a839e 15 # Level 4 Section 3
python -m kolibri manage setchannelposition 904d419f-53e2-4b6f-b60d-2aca7e729683 16 # Level 4 Section 4
python -m kolibri manage setchannelposition 5b679315-a02c-4035-9505-fc84701c482d 17 # Level 5 Section 1
python -m kolibri manage setchannelposition a5cd9f9f-000e-4145-9a95-875d7dfd3e68 18 # Level 5 Section 2
python -m kolibri manage setchannelposition 6c408923-2a72-447e-abbd-f83b7c5612a4 19 # Level 5 Section 3
python -m kolibri manage setchannelposition 28f4920a-7b44-4e29-af4f-1e8d00ca332b 20 # Level 5 Section 4
python -m kolibri manage setchannelposition cf1b82ba-1452-4cf7-8a08-ce8c01626b28 21 # Level 6 Section 1
python -m kolibri manage setchannelposition b21103bd-85f6-4e18-b6a6-e4cb50665386 22 # Level 6 Section 2
python -m kolibri manage setchannelposition 20e95963-caea-4ab5-ac50-5c60f3c5a5bb 23 # Level 6 Section 3
python -m kolibri manage setchannelposition 1ab4e328-7ce7-45ee-9166-bb13021a3b55 24 # Level 6 Section 4
python -m kolibri manage setchannelposition 8d368058-6565-44e2-b7fe-62eb2a632698 25 # Grade 7 Numeracy (Zambia)
python -m kolibri manage setchannelposition 96578ffc-06e4-4a46-b021-540cb217f9c9 26 # Grade 7 Literacy (Zambia)
python -m kolibri manage setchannelposition 8784b9f7-8d58-4273-aff5-79b246529215 27 # Alpha A
python -m kolibri manage setchannelposition cc805378-86cb-498e-b564-242f44c87723 28 # Alpha B
python -m kolibri manage setchannelposition 7035e792-1ddf-489f-ad45-44c814a199fb 29 # Alpha C
python -m kolibri manage setchannelposition 1d8f1428-da33-4779-b956-85c4581186c4 30 # Alpha D
python -m kolibri manage setchannelposition 57995474-194c-4068-bfed-1ee16108093f 31 # Bravo A
python -m kolibri manage setchannelposition b7214b92-1fd9-4a1c-b758-821919bcd3e0 32 # Bravo B
python -m kolibri manage setchannelposition 5aee4435-135b-4039-a3a8-24d96f72bfcb 33 # Bravo C
python -m kolibri manage setchannelposition 98ab8048-1075-45da-92e3-394409955526 34 # Bravo D
python -m kolibri manage setchannelposition 19ea4c94-ee48-4cb0-b5bb-617f5511f4c1 35 # Coach Professional Development

echo "Successfully reordered channels"


