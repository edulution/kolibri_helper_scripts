# emergency script to enroll all users into the live learners class in case the assign memberships script does not work

import kolibri
import django
from kolibri.core.auth.models import Collection, FacilityUser, Membership
django.setup()

# import all the helper functions


# get a reference to the live learners class
live_learners_class = Collection.objects.get(name='Live Learners')

# get a list of all the users on the device
all_users = FacilityUser.objects.all()

# delete all memberships
Membership.objects.all().delete()

# assign every user to the live learners class
for learner in all_users:
    Membership.objects.create(user=learner, collection=live_learners_class)
