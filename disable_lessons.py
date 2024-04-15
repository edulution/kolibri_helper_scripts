import kolibri  # noqa F401
import django
from colors import *

django.setup()

from kolibri.core.auth.models import Facility
from helpers import get_facility_or_default


def disable_lessons(facilityname=None):
    # Attempt to get facility passed in or get the default facility on the device
    facility = get_facility_or_default(facilityname)

    # Set the value of learner_can_view_lessons in the dataset to False
    facility.dataset.learner_can_view_lessons = False

    # Save the facilitydataset
    facility.dataset.save()

    # Print a success message
    print_colored(
        "Lessons disabled on Facility: {}".format(facility.name),
        colors.fg.lightgreen,
    )


# Main function called when script is run
if __name__ == "__main__":
    disable_lessons()
