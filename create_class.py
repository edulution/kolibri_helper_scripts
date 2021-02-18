import kolibri  # noqa F401
import django

import uuid
import random
from helpers import (
    get_facility_or_default,
    get_or_create_classroom,
    get_or_create_learnergroup,
    get_channels_in_module,
    get_admins_for_facility,
)

django.setup()

from kolibri.core.auth.models import Facility, FacilityUser,Classroom  # noqa E402
from kolibri.core.exams.models import Exam, ExamAssignment  # noqa E402
from kolibri.core.content.models import ContentNode, ChannelMetadata  # noqa E402
from le_utils.constants import content_kinds  # noqa E402


def create_class(classroomname, facilityname=None):
    """Function to get a reference to a specified Classroom object in a specified Facility
    Creates the Classroom object in the a specified Facility if it does not exist
    Args:

    classroomname (string): name of the classroom
        facilityname (string): name of the facility (default facility if not specified)
    Returns:
        Classroom: a reference to Classroom created
    """

    # get the facility passed in or the default facility
    facility_for_class = get_facility_or_default(facilityname)

    # filter the collections objects to check if a class with the name passed in already exists
    # get a boolean of whether found or not
    class_exists = Classroom.objects.filter(name=classroomname).exists()
    if class_exists:

        # if the class already exists return a reference of the object
        class_obj = Classroom.objects.get(name=classroomname, parent=facility_for_class)
    else:
        print(
            "Creating Class {} in Facility {}".format(
                classroomname, facility_for_class.name
            )
        )
        class_obj = Classroom.objects.create(
            name=classroomname, parent=facility_for_class
        )

    # return a reference to the ClassRoom object that was fetched or created
    return class_obj
