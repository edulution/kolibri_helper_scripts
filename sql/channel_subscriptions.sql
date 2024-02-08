/*Subscriptions for each level*/
/*Each group corresponds to 1 level and can see all the sections for that level and all preceeding levels */
DO $$
    -- variable to use as placeholder when looping through classrooms
DECLARE
    classRow record;
BEGIN
    /*Loop through all classrooms on the device*/
    FOR classRow IN (
        SELECT
            *
        FROM
            kolibriauth_collection
        WHERE
            kind = 'classroom')
        LOOP
            /*If the name of the classroom is like Grade 7,
             add the grade 7 numeracy playlist to the subscriptions for the classroom and all of its learnergroups*/
            IF classRow.name LIKE 'Grade 7%' THEN
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\",\ "a33d75c6527143ceb21310fa74882b98\",\ "4f4c4a2ff9984526a2d3b5ce5f3df78a\",\ "319c8b3a7b8c41e1ae542163228bf38f\",\ "35cccf14d93445f08e00823727af4ddf\",\ "9236e970deb6469595972119700a4506\",\ "348ee296a88a4eb8b6b103443a6e16e6\",\ "3a3d5063da77418f8139ae17e4cddab0\",\ "d9d4d1f701d24b35be2cd4e78e2074e6\",\ "aaa9cebbc6bf4a6d88f745b1f260988a\",\ "dcd8318809ab4d12b3e26008a35680cf\",\ "c9b60dc13c184288b77880976df822f3\",\ "df11dd6aea8f4591ad02bd58fbb4cb63\",\ "d36d2bf4ed5f45fbb254896552dca2da\",\ "07a3ba7d59db47d1b7b5c78ea2c896d3\",\ "47957429f8324eb7919640e3023c06f8\",\ "ea4c6ee308b7457e8af0c5e9ea0fbf93\",\ "cf1b82ba14524cf78a08ce8c01626b28\",\ "b21103bd85f64e18b6a6e4cb50665386\",\ "20e95963caea4ab5ac505c60f3c5a5bb\",\ "1ab4e3287ce745ee9166bb13021a3b55\", \"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\",\"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 1'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\",\ "a33d75c6527143ceb21310fa74882b98\",\ "4f4c4a2ff9984526a2d3b5ce5f3df78a\",\ "319c8b3a7b8c41e1ae542163228bf38f\",\ "35cccf14d93445f08e00823727af4ddf\",\"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 2'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\",\ "a33d75c6527143ceb21310fa74882b98\",\ "4f4c4a2ff9984526a2d3b5ce5f3df78a\",\ "319c8b3a7b8c41e1ae542163228bf38f\",\ "35cccf14d93445f08e00823727af4ddf\",\"9236e970deb6469595972119700a4506\",\"348ee296a88a4eb8b6b103443a6e16e6\",\"3a3d5063da77418f8139ae17e4cddab0\",\"d9d4d1f701d24b35be2cd4e78e2074e6\",\"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'

                WHERE
                    name = 'Level 3'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\",\ "a33d75c6527143ceb21310fa74882b98\",\ "4f4c4a2ff9984526a2d3b5ce5f3df78a\",\ "319c8b3a7b8c41e1ae542163228bf38f\",\ "35cccf14d93445f08e00823727af4ddf\",\"9236e970deb6469595972119700a4506\",\"348ee296a88a4eb8b6b103443a6e16e6\",\"3a3d5063da77418f8139ae17e4cddab0\",\"d9d4d1f701d24b35be2cd4e78e2074e6\",\"aaa9cebbc6bf4a6d88f745b1f260988a\",\"dcd8318809ab4d12b3e26008a35680cf\",\"c9b60dc13c184288b77880976df822f3\",\"df11dd6aea8f4591ad02bd58fbb4cb63\",\"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 4'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\",\ "a33d75c6527143ceb21310fa74882b98\",\ "4f4c4a2ff9984526a2d3b5ce5f3df78a\",\ "319c8b3a7b8c41e1ae542163228bf38f\",\ "35cccf14d93445f08e00823727af4ddf\",\"9236e970deb6469595972119700a4506\",\"348ee296a88a4eb8b6b103443a6e16e6\",\"3a3d5063da77418f8139ae17e4cddab0\",\"d9d4d1f701d24b35be2cd4e78e2074e6\",\"aaa9cebbc6bf4a6d88f745b1f260988a\",\"dcd8318809ab4d12b3e26008a35680cf\",\"c9b60dc13c184288b77880976df822f3\",\"df11dd6aea8f4591ad02bd58fbb4cb63\",\"d36d2bf4ed5f45fbb254896552dca2da\",\"07a3ba7d59db47d1b7b5c78ea2c896d3\",\"47957429f8324eb7919640e3023c06f8\",\"ea4c6ee308b7457e8af0c5e9ea0fbf93\",\"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 5'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\",\ "a33d75c6527143ceb21310fa74882b98\",\ "4f4c4a2ff9984526a2d3b5ce5f3df78a\",\ "319c8b3a7b8c41e1ae542163228bf38f\",\ "35cccf14d93445f08e00823727af4ddf\",\"9236e970deb6469595972119700a4506\",\"348ee296a88a4eb8b6b103443a6e16e6\",\"3a3d5063da77418f8139ae17e4cddab0\",\"d9d4d1f701d24b35be2cd4e78e2074e6\",\"aaa9cebbc6bf4a6d88f745b1f260988a\",\"dcd8318809ab4d12b3e26008a35680cf\",\"c9b60dc13c184288b77880976df822f3\",\"df11dd6aea8f4591ad02bd58fbb4cb63\",\"d36d2bf4ed5f45fbb254896552dca2da\",\"07a3ba7d59db47d1b7b5c78ea2c896d3\",\"47957429f8324eb7919640e3023c06f8\",\"ea4c6ee308b7457e8af0c5e9ea0fbf93\",\"cf1b82ba14524cf78a08ce8c01626b28\",\"b21103bd85f64e18b6a6e4cb50665386\",\"20e95963caea4ab5ac505c60f3c5a5bb\",\"1ab4e3287ce745ee9166bb13021a3b55\",\"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 6'
                    AND parent_id = classRow.id;

                /*If the classroom name is not like Grade 7,
                 Only add the levels to subscriptions for each respective level*/
            ELSE
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\",\ "a33d75c6527143ceb21310fa74882b98\",\ "4f4c4a2ff9984526a2d3b5ce5f3df78a\",\ "319c8b3a7b8c41e1ae542163228bf38f\",\ "35cccf14d93445f08e00823727af4ddf\",\ "9236e970deb6469595972119700a4506\",\ "348ee296a88a4eb8b6b103443a6e16e6\",\ "3a3d5063da77418f8139ae17e4cddab0\",\ "d9d4d1f701d24b35be2cd4e78e2074e6\",\ "aaa9cebbc6bf4a6d88f745b1f260988a\",\ "dcd8318809ab4d12b3e26008a35680cf\",\ "c9b60dc13c184288b77880976df822f3\",\ "df11dd6aea8f4591ad02bd58fbb4cb63\",\ "d36d2bf4ed5f45fbb254896552dca2da\",\ "07a3ba7d59db47d1b7b5c78ea2c896d3\",\ "47957429f8324eb7919640e3023c06f8\",\ "ea4c6ee308b7457e8af0c5e9ea0fbf93\",\ "cf1b82ba14524cf78a08ce8c01626b28\",\ "b21103bd85f64e18b6a6e4cb50665386\",\ "20e95963caea4ab5ac505c60f3c5a5bb\",\ "1ab4e3287ce745ee9166bb13021a3b55\",  \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 1'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\",\ "a33d75c6527143ceb21310fa74882b98\",\ "4f4c4a2ff9984526a2d3b5ce5f3df78a\",\ "319c8b3a7b8c41e1ae542163228bf38f\",\ "35cccf14d93445f08e00823727af4ddf\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 2'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\",\ "a33d75c6527143ceb21310fa74882b98\",\ "4f4c4a2ff9984526a2d3b5ce5f3df78a\",\ "319c8b3a7b8c41e1ae542163228bf38f\",\ "35cccf14d93445f08e00823727af4ddf\",\"9236e970deb6469595972119700a4506\",\"348ee296a88a4eb8b6b103443a6e16e6\",\"3a3d5063da77418f8139ae17e4cddab0\",\"d9d4d1f701d24b35be2cd4e78e2074e6\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'

                WHERE
                    name = 'Level 3'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\",\ "a33d75c6527143ceb21310fa74882b98\",\ "4f4c4a2ff9984526a2d3b5ce5f3df78a\",\ "319c8b3a7b8c41e1ae542163228bf38f\",\ "35cccf14d93445f08e00823727af4ddf\",\"9236e970deb6469595972119700a4506\",\"348ee296a88a4eb8b6b103443a6e16e6\",\"3a3d5063da77418f8139ae17e4cddab0\",\"d9d4d1f701d24b35be2cd4e78e2074e6\",\"aaa9cebbc6bf4a6d88f745b1f260988a\",\"dcd8318809ab4d12b3e26008a35680cf\",\"c9b60dc13c184288b77880976df822f3\",\"df11dd6aea8f4591ad02bd58fbb4cb63\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 4'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\",\ "a33d75c6527143ceb21310fa74882b98\",\ "4f4c4a2ff9984526a2d3b5ce5f3df78a\",\ "319c8b3a7b8c41e1ae542163228bf38f\",\ "35cccf14d93445f08e00823727af4ddf\",\"9236e970deb6469595972119700a4506\",\"348ee296a88a4eb8b6b103443a6e16e6\",\"3a3d5063da77418f8139ae17e4cddab0\",\"d9d4d1f701d24b35be2cd4e78e2074e6\",\"aaa9cebbc6bf4a6d88f745b1f260988a\",\"dcd8318809ab4d12b3e26008a35680cf\",\"c9b60dc13c184288b77880976df822f3\",\"df11dd6aea8f4591ad02bd58fbb4cb63\",\"d36d2bf4ed5f45fbb254896552dca2da\",\"07a3ba7d59db47d1b7b5c78ea2c896d3\",\"47957429f8324eb7919640e3023c06f8\",\"ea4c6ee308b7457e8af0c5e9ea0fbf93\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 5'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"547800a20c60493988f8135500654e69\",\ "d50aec3616f444a3b7313cd2b264535e\",\ "5d2577d999664724844008449f3b3e23\",\ "4b46d72f0122482682e2a4da47ad7b3e\",\ "a33d75c6527143ceb21310fa74882b98\",\ "4f4c4a2ff9984526a2d3b5ce5f3df78a\",\ "319c8b3a7b8c41e1ae542163228bf38f\",\ "35cccf14d93445f08e00823727af4ddf\",\"9236e970deb6469595972119700a4506\",\"348ee296a88a4eb8b6b103443a6e16e6\",\"3a3d5063da77418f8139ae17e4cddab0\",\"d9d4d1f701d24b35be2cd4e78e2074e6\",\"aaa9cebbc6bf4a6d88f745b1f260988a\",\"dcd8318809ab4d12b3e26008a35680cf\",\"c9b60dc13c184288b77880976df822f3\",\"df11dd6aea8f4591ad02bd58fbb4cb63\",\"d36d2bf4ed5f45fbb254896552dca2da\",\"07a3ba7d59db47d1b7b5c78ea2c896d3\",\"47957429f8324eb7919640e3023c06f8\",\"ea4c6ee308b7457e8af0c5e9ea0fbf93\",\"cf1b82ba14524cf78a08ce8c01626b28\",\"b21103bd85f64e18b6a6e4cb50665386\",\"20e95963caea4ab5ac505c60f3c5a5bb\",\"1ab4e3287ce745ee9166bb13021a3b55\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 6'
                    AND parent_id = classRow.id;
            END IF;
        END LOOP;
    RAISE NOTICE 'Channel subscription complete';
    END$$;