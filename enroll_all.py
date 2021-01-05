# emergency script to enroll all users into the live learners class in case the assign memberships script does not work

import kolibri  # noqa F401
import django

django.setup()

from kolibri.core.auth.models import Collection, FacilityUser, Membership  # noqa E402

# get a reference to all of the classrooms called live learners across the device
live_learners_classes = Collection.objects.filter(name__contains="Live Learners")

# convert the iterable above into a dictionary
# the parent_id(facility_id) of the classroom is the key, and the classroom itself is the value
class_dict = {c.parent_id: c for c in live_learners_classes}

# get a list of all the users on the device
# use raw SQL to get users that are not admins or coaches
all_users_query = """select * from kolibriauth_facilityuser
where id not in
(select user_id from kolibriauth_role where kind in ('admin','coach'))"""

all_users = FacilityUser.objects.raw(all_users_query)

# delete all memberships
Membership.objects.all().delete()

# assign every user to the live learners class
# using learner's matching facility_id from the dict of live learners classes
for learner in all_users:
    Membership.objects.create(
        user=learner, collection=class_dict.get(learner.facility_id)
    )
