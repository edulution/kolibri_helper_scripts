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
                    subscriptions = '"[\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\",\"f6e8f1f569c54bc58ecb54d826cd3783\",\"5126a907e5284345847c8ca749c8cd9b\",\"521f889dc8634998b5542a526d428b85\",\"0985900c047a41738e796f19d9b57ed5\",\"c0302f6cd0624778bc8dd7a2b91d09b4\",\"ddf25e8fcde84e8998118daffb2d8655\",\"e2217b872f784190a0a55c46e9ee8bc1\",\"f908fac9fe5644b996abe25dfbd530bc\",\"d4b44e6dd4de450ebbc799085ba656e5\",\"763eafc24e684dbe8f54c9a22dd63599\",\"7de1d8eca4874856b508c1a4f51a839e\",\"904d419f53e24b6fb60d2aca7e729683\",\"5b679315a02c40359505fc84701c482d\",\"a5cd9f9f000e41459a95875d7dfd3e68\",\"6c4089232a72447eabbdf83b7c5612a4\",\"28f4920a7b444e29af4f1e8d00ca332b\", \"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\",\"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 1'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"f6e8f1f569c54bc58ecb54d826cd3783\",\"5126a907e5284345847c8ca749c8cd9b\",\"521f889dc8634998b5542a526d428b85\",\"0985900c047a41738e796f19d9b57ed5\",\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\",\"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 2'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"f6e8f1f569c54bc58ecb54d826cd3783\",\"5126a907e5284345847c8ca749c8cd9b\",\"521f889dc8634998b5542a526d428b85\",\"0985900c047a41738e796f19d9b57ed5\",\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\",\"c0302f6cd0624778bc8dd7a2b91d09b4\",\"ddf25e8fcde84e8998118daffb2d8655\",\"e2217b872f784190a0a55c46e9ee8bc1\",\"f908fac9fe5644b996abe25dfbd530bc\",\"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 3'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"f6e8f1f569c54bc58ecb54d826cd3783\",\"5126a907e5284345847c8ca749c8cd9b\",\"521f889dc8634998b5542a526d428b85\",\"0985900c047a41738e796f19d9b57ed5\",\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\",\"c0302f6cd0624778bc8dd7a2b91d09b4\",\"ddf25e8fcde84e8998118daffb2d8655\",\"e2217b872f784190a0a55c46e9ee8bc1\",\"f908fac9fe5644b996abe25dfbd530bc\",\"d4b44e6dd4de450ebbc799085ba656e5\",\"763eafc24e684dbe8f54c9a22dd63599\",\"7de1d8eca4874856b508c1a4f51a839e\",\"904d419f53e24b6fb60d2aca7e729683\",\"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 4'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"f6e8f1f569c54bc58ecb54d826cd3783\",\"5126a907e5284345847c8ca749c8cd9b\",\"521f889dc8634998b5542a526d428b85\",\"0985900c047a41738e796f19d9b57ed5\",\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\",\"c0302f6cd0624778bc8dd7a2b91d09b4\",\"ddf25e8fcde84e8998118daffb2d8655\",\"e2217b872f784190a0a55c46e9ee8bc1\",\"f908fac9fe5644b996abe25dfbd530bc\",\"d4b44e6dd4de450ebbc799085ba656e5\",\"763eafc24e684dbe8f54c9a22dd63599\",\"7de1d8eca4874856b508c1a4f51a839e\",\"904d419f53e24b6fb60d2aca7e729683\",\"5b679315a02c40359505fc84701c482d\",\"a5cd9f9f000e41459a95875d7dfd3e68\",\"6c4089232a72447eabbdf83b7c5612a4\",\"28f4920a7b444e29af4f1e8d00ca332b\",\"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 5'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"f6e8f1f569c54bc58ecb54d826cd3783\",\"5126a907e5284345847c8ca749c8cd9b\",\"521f889dc8634998b5542a526d428b85\",\"0985900c047a41738e796f19d9b57ed5\",\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\",\"c0302f6cd0624778bc8dd7a2b91d09b4\",\"ddf25e8fcde84e8998118daffb2d8655\",\"e2217b872f784190a0a55c46e9ee8bc1\",\"f908fac9fe5644b996abe25dfbd530bc\",\"d4b44e6dd4de450ebbc799085ba656e5\",\"763eafc24e684dbe8f54c9a22dd63599\",\"7de1d8eca4874856b508c1a4f51a839e\",\"904d419f53e24b6fb60d2aca7e729683\",\"5b679315a02c40359505fc84701c482d\",\"a5cd9f9f000e41459a95875d7dfd3e68\",\"6c4089232a72447eabbdf83b7c5612a4\",\"28f4920a7b444e29af4f1e8d00ca332b\",\"cf1b82ba-1452-4cf7-8a08-ce8c01626b28\",\"b21103bd-85f6-4e18-b6a6-e4cb50665386\",\"20e95963-caea-4ab5-ac50-5c60f3c5a5bb\",\"1ab4e328-7ce7-45ee-9166-bb13021a3b55\",\"8d368058656544e2b7fe62eb2a632698\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 6'
                    AND parent_id = classRow.id;

                /*If the classroom name is not like Grade 7,
                 Only add the levels to subscriptions for each respective level*/
            ELSE
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\",\"f6e8f1f569c54bc58ecb54d826cd3783\",\"5126a907e5284345847c8ca749c8cd9b\",\"521f889dc8634998b5542a526d428b85\",\"0985900c047a41738e796f19d9b57ed5\",\"c0302f6cd0624778bc8dd7a2b91d09b4\",\"ddf25e8fcde84e8998118daffb2d8655\",\"e2217b872f784190a0a55c46e9ee8bc1\",\"f908fac9fe5644b996abe25dfbd530bc\",\"d4b44e6dd4de450ebbc799085ba656e5\",\"763eafc24e684dbe8f54c9a22dd63599\",\"7de1d8eca4874856b508c1a4f51a839e\",\"904d419f53e24b6fb60d2aca7e729683\",\"5b679315a02c40359505fc84701c482d\",\"a5cd9f9f000e41459a95875d7dfd3e68\",\"6c4089232a72447eabbdf83b7c5612a4\",\"28f4920a7b444e29af4f1e8d00ca332b\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    kind = 'classroom'
                    AND id = classRow.id;

                /*Subscriptions for each level*/
                /*Each group corresponds to 1 level and can see all the sections for that level and all preceeding levels */
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 1'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"f6e8f1f569c54bc58ecb54d826cd3783\",\"5126a907e5284345847c8ca749c8cd9b\",\"521f889dc8634998b5542a526d428b85\",\"0985900c047a41738e796f19d9b57ed5\",\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 2'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"f6e8f1f569c54bc58ecb54d826cd3783\",\"5126a907e5284345847c8ca749c8cd9b\",\"521f889dc8634998b5542a526d428b85\",\"0985900c047a41738e796f19d9b57ed5\",\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\",\"c0302f6cd0624778bc8dd7a2b91d09b4\",\"ddf25e8fcde84e8998118daffb2d8655\",\"e2217b872f784190a0a55c46e9ee8bc1\",\"f908fac9fe5644b996abe25dfbd530bc\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 3'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"f6e8f1f569c54bc58ecb54d826cd3783\",\"5126a907e5284345847c8ca749c8cd9b\",\"521f889dc8634998b5542a526d428b85\",\"0985900c047a41738e796f19d9b57ed5\",\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\",\"c0302f6cd0624778bc8dd7a2b91d09b4\",\"ddf25e8fcde84e8998118daffb2d8655\",\"e2217b872f784190a0a55c46e9ee8bc1\",\"f908fac9fe5644b996abe25dfbd530bc\",\"d4b44e6dd4de450ebbc799085ba656e5\",\"763eafc24e684dbe8f54c9a22dd63599\",\"7de1d8eca4874856b508c1a4f51a839e\",\"904d419f53e24b6fb60d2aca7e729683\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 4'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"f6e8f1f569c54bc58ecb54d826cd3783\",\"5126a907e5284345847c8ca749c8cd9b\",\"521f889dc8634998b5542a526d428b85\",\"0985900c047a41738e796f19d9b57ed5\",\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\",\"c0302f6cd0624778bc8dd7a2b91d09b4\",\"ddf25e8fcde84e8998118daffb2d8655\",\"e2217b872f784190a0a55c46e9ee8bc1\",\"f908fac9fe5644b996abe25dfbd530bc\",\"d4b44e6dd4de450ebbc799085ba656e5\",\"763eafc24e684dbe8f54c9a22dd63599\",\"7de1d8eca4874856b508c1a4f51a839e\",\"904d419f53e24b6fb60d2aca7e729683\",\"5b679315a02c40359505fc84701c482d\",\"a5cd9f9f000e41459a95875d7dfd3e68\",\"6c4089232a72447eabbdf83b7c5612a4\",\"28f4920a7b444e29af4f1e8d00ca332b\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 5'
                    AND parent_id = classRow.id;
                UPDATE
                    kolibriauth_collection
                SET
                    subscriptions = '"[\"f6e8f1f569c54bc58ecb54d826cd3783\",\"5126a907e5284345847c8ca749c8cd9b\",\"521f889dc8634998b5542a526d428b85\",\"0985900c047a41738e796f19d9b57ed5\",\"f3f6bf4b9c424b6fbd90bece1418a415\",\"3a126f041a9e4127978bb6544a099d0d\",\"03761fe9a2424e9ebd367fbae14dc134\",\"f12e2f67d5894b34bb942484d880c4a6\",\"c0302f6cd0624778bc8dd7a2b91d09b4\",\"ddf25e8fcde84e8998118daffb2d8655\",\"e2217b872f784190a0a55c46e9ee8bc1\",\"f908fac9fe5644b996abe25dfbd530bc\",\"d4b44e6dd4de450ebbc799085ba656e5\",\"763eafc24e684dbe8f54c9a22dd63599\",\"7de1d8eca4874856b508c1a4f51a839e\",\"904d419f53e24b6fb60d2aca7e729683\",\"5b679315a02c40359505fc84701c482d\",\"a5cd9f9f000e41459a95875d7dfd3e68\",\"6c4089232a72447eabbdf83b7c5612a4\",\"28f4920a7b444e29af4f1e8d00ca332b\",\"cf1b82ba14524cf78a08ce8c01626b28\",\"b21103bd85f64e18b6a6e4cb50665386\",\"20e95963caea4ab5ac505c60f3c5a5bb\",\"1ab4e3287ce745ee9166bb13021a3b55\", \"4c5f286c4d4c473abff55402a6cf0f9e\"]"'
                WHERE
                    name = 'Level 6'
                    AND parent_id = classRow.id;
            END IF;
        END LOOP;
    RAISE NOTICE 'Channel subscription complete';
    END$$;

