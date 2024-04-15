--Subscribe all classrooms to all numeracy channels
UPDATE
    kolibriauth_collection
SET
    subscriptions = '"[\"d8d0a31db57e44a8a9564a7c6b1f6368\",\"14ba8f9f3fc54f0384f493a77b07ac1e\",\"da831fef8ade4759a1126a6120e92210\",\"27939b34516c4e09b86f9abc5f7746c0\",\"cab0fe89ddc841dfbd40e1c279df86de\",\"76453bfda0594b318c2e2da87febce97\",\"fb2ca0b1ca554a049f2e5884564e2d23\",\"dbb67c5dfec84e668753c469583e93f2\",\"4f1079f9438a4d5d88d92d91ab0911a4\",\"514cf2b44b664dbe9446558d73868c0f\",\"04621abf99d6400ab00e2a8f9924ee48\",\"480741a8686c451b9d152b960b53a5c8\",\"ca07ea33dc4d4a0eaba973898e85577b\",\"e80e29b8abe649979143a3ae0c1a27dc\",\"6b40757c62664e759e4f39808529b21c\",\"c1ab61bad6314ee7aa7adbdcbd217be2\",\"8eea5e9d043547bcace01f35959a91ec\",\"ff5782ffa9bd4ee280a272ab13653f97\",\"960e361cbe5e4f5fa3d139724a8cb18d\",\"cad83700eba444509dd1234655fc6670\",\"cf1b82ba14524cf78a08ce8c01626b28\",\"b21103bd85f64e18b6a6e4cb50665386\",\"20e95963caea4ab5ac505c60f3c5a5bb\",\"1ab4e3287ce745ee9166bb13021a3b55\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
WHERE
    kind = 'classroom';

--Subscriptions for each level
--Each group corresponds to 1 level and can see all the sections for that level and all preceeding levels
UPDATE
    kolibriauth_collection
SET
    subscriptions = '"[\"d8d0a31db57e44a8a9564a7c6b1f6368\",\"14ba8f9f3fc54f0384f493a77b07ac1e\",\"da831fef8ade4759a1126a6120e92210\",\"27939b34516c4e09b86f9abc5f7746c0\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
WHERE
    name = 'Level 1';

UPDATE
    kolibriauth_collection
SET
    subscriptions = '"[\"d8d0a31db57e44a8a9564a7c6b1f6368\",\"14ba8f9f3fc54f0384f493a77b07ac1e\",\"da831fef8ade4759a1126a6120e92210\",\"27939b34516c4e09b86f9abc5f7746c0\",\"cab0fe89ddc841dfbd40e1c279df86de\",\"76453bfda0594b318c2e2da87febce97\",\"fb2ca0b1ca554a049f2e5884564e2d23\",\"dbb67c5dfec84e668753c469583e93f2\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
WHERE
    name = 'Level 2';

UPDATE
    kolibriauth_collection
SET
    subscriptions = '"[\"d8d0a31db57e44a8a9564a7c6b1f6368\",\"14ba8f9f3fc54f0384f493a77b07ac1e\",\"da831fef8ade4759a1126a6120e92210\",\"27939b34516c4e09b86f9abc5f7746c0\",\"cab0fe89ddc841dfbd40e1c279df86de\",\"76453bfda0594b318c2e2da87febce97\",\"fb2ca0b1ca554a049f2e5884564e2d23\",\"dbb67c5dfec84e668753c469583e93f2\",\"4f1079f9438a4d5d88d92d91ab0911a4\",\"514cf2b44b664dbe9446558d73868c0f\",\"04621abf99d6400ab00e2a8f9924ee48\",\"480741a8686c451b9d152b960b53a5c8\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
WHERE
    name = 'Level 3';

UPDATE
    kolibriauth_collection
SET
    subscriptions = '"[\"d8d0a31db57e44a8a9564a7c6b1f6368\",\"14ba8f9f3fc54f0384f493a77b07ac1e\",\"da831fef8ade4759a1126a6120e92210\",\"27939b34516c4e09b86f9abc5f7746c0\",\"cab0fe89ddc841dfbd40e1c279df86de\",\"76453bfda0594b318c2e2da87febce97\",\"fb2ca0b1ca554a049f2e5884564e2d23\",\"dbb67c5dfec84e668753c469583e93f2\",\"4f1079f9438a4d5d88d92d91ab0911a4\",\"514cf2b44b664dbe9446558d73868c0f\",\"04621abf99d6400ab00e2a8f9924ee48\",\"480741a8686c451b9d152b960b53a5c8\",\"ca07ea33dc4d4a0eaba973898e85577b\",\"e80e29b8abe649979143a3ae0c1a27dc\",\"6b40757c62664e759e4f39808529b21c\",\"c1ab61bad6314ee7aa7adbdcbd217be2\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
WHERE
    name = 'Level 4';

UPDATE
    kolibriauth_collection
SET
    subscriptions = '"[\"d8d0a31db57e44a8a9564a7c6b1f6368\",\"14ba8f9f3fc54f0384f493a77b07ac1e\",\"da831fef8ade4759a1126a6120e92210\",\"27939b34516c4e09b86f9abc5f7746c0\",\"cab0fe89ddc841dfbd40e1c279df86de\",\"76453bfda0594b318c2e2da87febce97\",\"fb2ca0b1ca554a049f2e5884564e2d23\",\"dbb67c5dfec84e668753c469583e93f2\",\"4f1079f9438a4d5d88d92d91ab0911a4\",\"514cf2b44b664dbe9446558d73868c0f\",\"04621abf99d6400ab00e2a8f9924ee48\",\"480741a8686c451b9d152b960b53a5c8\",\"ca07ea33dc4d4a0eaba973898e85577b\",\"e80e29b8abe649979143a3ae0c1a27dc\",\"6b40757c62664e759e4f39808529b21c\",\"c1ab61bad6314ee7aa7adbdcbd217be2\",\"8eea5e9d043547bcace01f35959a91ec\",\"ff5782ffa9bd4ee280a272ab13653f97\",\"960e361cbe5e4f5fa3d139724a8cb18d\",\"cad83700eba444509dd1234655fc6670\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
WHERE
    name = 'Level 5';


UPDATE
    kolibriauth_collection
SET
    subscriptions = '"[\"d8d0a31db57e44a8a9564a7c6b1f6368\",\"14ba8f9f3fc54f0384f493a77b07ac1e\",\"da831fef8ade4759a1126a6120e92210\",\"27939b34516c4e09b86f9abc5f7746c0\",\"cab0fe89ddc841dfbd40e1c279df86de\",\"76453bfda0594b318c2e2da87febce97\",\"fb2ca0b1ca554a049f2e5884564e2d23\",\"dbb67c5dfec84e668753c469583e93f2\",\"4f1079f9438a4d5d88d92d91ab0911a4\",\"514cf2b44b664dbe9446558d73868c0f\",\"04621abf99d6400ab00e2a8f9924ee48\",\"480741a8686c451b9d152b960b53a5c8\",\"ca07ea33dc4d4a0eaba973898e85577b\",\"e80e29b8abe649979143a3ae0c1a27dc\",\"6b40757c62664e759e4f39808529b21c\",\"c1ab61bad6314ee7aa7adbdcbd217be2\",\"8eea5e9d043547bcace01f35959a91ec\",\"ff5782ffa9bd4ee280a272ab13653f97\",\"960e361cbe5e4f5fa3d139724a8cb18d\",\"cad83700eba444509dd1234655fc6670\",\"cf1b82ba14524cf78a08ce8c01626b28\",\"b21103bd85f64e18b6a6e4cb50665386\",\"20e95963caea4ab5ac505c60f3c5a5bb\",\"1ab4e3287ce745ee9166bb13021a3b55\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
WHERE
    name = 'Level 6';