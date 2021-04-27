/*SQL to reorder channels in case script does not work*/

/*Pre Alpha Alpha*/
UPDATE content_channelmetadata
SET "order" = 1
WHERE id = '3d6c9d72-a2e0-47d4-b7a0-ed20699e1b1f';

/*Pre Alpha B*/
UPDATE content_channelmetadata
SET "order" = 2
WHERE id = '6380a6a9-8a4c-4b26-8b31-47ad1c7ada13';

/*Pre Alpha C*/
UPDATE content_channelmetadata
SET "order" = 3
WHERE id = '20113bf1-ba07-4e08-bcc7-faaca03ade8a';

/*Pre Alpha D*/
UPDATE content_channelmetadata
SET "order" = 4
WHERE id = '1700bf9e-7109-4857-abf3-6c04a1963004';

/*Alpha A*/
UPDATE content_channelmetadata
SET "order" = 5
WHERE id = '8784b9f7-8d58-4273-aff5-79b246529215';

/*Alpha B*/
UPDATE content_channelmetadata
SET "order" = 6
WHERE id = 'cc805378-86cb-498e-b564-242f44c87723';

/*Alpha C*/
UPDATE content_channelmetadata
SET "order" = 7
WHERE id = '7035e792-1ddf-489f-ad45-44c814a199fb';

/*Alpha D*/
UPDATE content_channelmetadata
SET "order" = 8
WHERE id = '1d8f1428-da33-4779-b956-85c4581186c4';

/*Bravo A*/
UPDATE content_channelmetadata
SET "order" = 9
WHERE id = '57995474-194c-4068-bfed-1ee16108093f';

/*Bravo B*/
UPDATE content_channelmetadata
SET "order" = 10
WHERE id = 'b7214b92-1fd9-4a1c-b758-821919bcd3e0';

/*Bravo C*/
UPDATE content_channelmetadata
SET "order" = 11
WHERE id = '5aee4435-135b-4039-a3a8-24d96f72bfcb';

/*Bravo D*/
UPDATE content_channelmetadata
SET "order" = 12
WHERE id = '98ab8048-1075-45da-92e3-394409955526';
