import pytest  # noqa F401
import kolibri  # noqa F401
import django

django.setup()

from kolibri.core.auth.models import Facility  # noqa F401

import sys  # noqa F401

sys.path.append("../")
from helpers import create_facility, get_facility_or_default  # noqa F401

# Fixture to create a facility for the tests, then tear it down
@pytest.fixture
def setup_teardown_facility():
    # Create a new facility called Shangri La
    new_facility = Facility.objects.create(name="Shangri La")
    # Yield this facility
    yield new_facility
    # Tear it down
    Facility.objects.get(id=new_facility.id).delete()


class TestFacilityHelpers:
    def test_create_facility_that_already_exists(self, setup_teardown_facility):
        # Get the name of the Facility created in the fixture
        already_exists = setup_teardown_facility.name

        # Expect a value error if you attempt to create a facility with the same name
        with pytest.raises(ValueError):
            create_facility(already_exists)

    def test_get_default_facility(self):
        # Get Default facility using Facility class method
        def_facility = Facility.get_default_facility()

        # Get default facility using get_facility_or_default with no arguments
        get_facitity = get_facility_or_default()

        # check that the two facility_ids are equal
        assert def_facility.id == get_facitity.id

    def test_get_other_facility_that_exists(self, setup_teardown_facility):
        # Attempt to get a facility called Shangri La
        other_fac = get_facility_or_default("Shangri La")
        # The facility id of this facility
        # should be equal to the one created in setup_teardown
        assert other_fac.id == setup_teardown_facility.id

    def test_get_facility_that_doesnt_exist(self):
        # Attempt to get a facility that does not exist on the device
        # Expect to get value error when ran with random string
        with pytest.raises(ValueError):
            get_facility_or_default("g6oLjw")
