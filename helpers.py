import sys
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from kolibri.core.exams.models import Exam
from kolibri.core.lessons.models import Lesson
from kolibri.core.auth.models import (
    Facility,
    FacilityUser,
    Classroom,
    LearnerGroup,
    Role,
)
from kolibri.core.content.models import ChannelMetadata


def delete_all_lessons_for_class(classroomname, facilityname=None):
    """Function to delete all lessons that have been assigned to a classroom.
    The actutal Lesson objects are deleted, not just the assignment

    Args:
        classroomname (string): name of the classroom
        facilityname (string): name of the facility (default facility if not specified)

    Returns:
        None
    """

    facility_for_class = get_facility_or_default(facilityname)

    try:
        class_obj = Classroom.objects.get(name=classroomname, parent=facility_for_class)
    except ObjectDoesNotExist:
        raise ValueError(
            "There is no Class called {} in Facility {}. No Lessons were deleted".format(
                classroomname, facility_for_class
            )
        )
        sys.exit()

    print(
        "{} Lessons found in class {}".format(
            Lesson.objects.filter(collection=class_obj).count(), classroomname
        )
    )

    # delete all the lessons found for that class
    Lesson.objects.filter(collection=class_obj).delete()
    print("Lessons successfully deleted")


def delete_all_quizzes_for_class(classroomname, facilityname=None):
    """Function to delete all the quizzes created for a class

    Args:
        classroomname (string): name of the classroom
        facilityname (string): name of the facility (default facility if not specified)

    Returns:
        None
    """

    facility_for_class = get_facility_or_default(facilityname)

    try:
        class_obj = Classroom.objects.get(name=classroomname, parent=facility_for_class)
    except ObjectDoesNotExist:
        raise ValueError(
            "There is no Class called {} in Facility {}. No Quizzes were deleted".format(
                classroomname, facility_for_class
            )
        )
        sys.exit()

    print(
        "{} Quizzes found in class {}".format(
            Exam.objects.filter(collection=class_obj).count(), classroomname
        )
    )

    # delete all the quizzes found for that class
    Exam.objects.filter(collection=class_obj).delete()
    print("Quizzes successfully deleted")


def get_facility_or_default(facilityname=None):
    """Function to check if a facility exists or get the default facility

    Args:
        facilityname (string): name of the facility (default facility if not specified)

    Returns:
        Facility: a reference to the Facility created

    """

    # check if facilityname argument was passed in
    if facilityname:
        # if it was passed in
        # check if the facility requested exists
        facility_exists = Facility.objects.filter(name=facilityname).exists()
        # if the facility exists, store a reference to the object in the chosen_facility variable
        if facility_exists:
            chosen_facility = Facility.objects.get(name=facilityname)
            # inform the user which facility has been chosen
            print("Using Facility: {}".format(str(chosen_facility.name)))
        else:
            # if the facility does not exist, raise a value error and terminate the script
            raise ValueError("There is no Facility called {}".format(facilityname))
            sys.exit()
    else:
        # if the facilityname argument was not passed in, choose the default facility
        chosen_facility = Facility.get_default_facility()
        # inform the user which facility has been chosen
        print("Using Default Facility: {}".format(str(chosen_facility.name)))

    # return chosen facility
    return chosen_facility


def get_or_create_classroom(classroomname, facilityname=None):
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


def get_or_create_learnergroup(groupname, classroomname, facilityname=None):
    """Function to create a Learnergroup in a specified Classroom belonging to a specified Facility
    Creates both the Learergroup and Classroom objects if they do not exist

    Args:
        groupname (string):
        classroomname (string):
        facilityname (string):

    Returns:
        Learnergroup : A reference to the Learnergroup object created
    """

    # get the facility passed in or the default facility
    # facility_for_class = get_facility_or_default(facilityname)

    # get the classroom passed in or create it
    class_for_group = get_or_create_classroom(classroomname, facilityname)

    # check if the learnergroup passed in already exists
    learnergroup_exists = LearnerGroup.objects.filter(
        name=groupname, parent=class_for_group
    ).exists()

    # if the learnergroup already exists, store a reference to it in the learnergroup_obj variable
    if learnergroup_exists:
        # Inform the user that the group already exists
        print(
            "Group {} already exists in Class {}".format(
                groupname, str(class_for_group.name)
            )
        )
        learnergroup_obj = LearnerGroup.objects.get(
            name=groupname, parent=class_for_group
        )
    else:
        # if the group does not exist, create it in the class and inform the user that it has been created
        print(
            "Creating Group {} in Class {}".format(groupname, str(class_for_group.name))
        )
        learnergroup_obj = LearnerGroup.objects.create(
            name=groupname, parent=class_for_group
        )

    # return a reference to the LearnerGroup object that was created or fetched
    return learnergroup_obj


def create_facility(facilityname):
    """Function to create a new Facility object

    Args:
        facilityname (string): name of the facility to create

    Returns:
        Facility: a reference to the Facility created

    Settings on the created Facility:
        - Annonymous users cannot access content
        - Learners cannot sign up
        - Learners cannot delete their accounts
        - Learners cannot edit username, and name
        - Learners are allowed to log in without a password
        - Download button is not displayed on content
    """

    # check if a facility with the name passed in already exists
    facility_exists = Facility.objects.filter(name=facilityname).exists()

    # if a facility with the name passed in already exists,
    if facility_exists:
        # raise a value error and exit in an error state
        raise ValueError(
            "Error: Facility with the name {} already exists".format(facilityname)
        )
        sys.exit("Facility was not created. Please check the errors above")
    else:
        # if a facility with the name passed in does not exist, generate a new facility object
        new_facility = Facility.objects.create(name=facilityname)

        # set the permissions on the facility
        new_facility.learner_can_edit_username = False
        new_facility.learner_can_edit_name = False
        new_facility.learner_can_edit_password = False
        new_facility.learner_can_sign_up = False
        new_facility.learner_can_delete_account = False
        new_facility.learner_can_login_with_no_password = True
        new_facility.show_download_button_in_learn = False
        new_facility.allow_guest_access = False

        # save the object after modifying its properties
        new_facility.save()

    # return the new facility object
    return new_facility


def create_admin_for_facility(admin_uname, admin_password, facilityname):
    """Function to create an admin account in a specified Facility.
    An admin is simply a FacilityUser with admin privileges

    Args:
        admin_uname (string): Username of the admin account to create
        admin_password (string): Password of the admin account to create
        facilityname (string): Name of the facility in which to create the admin account

    Returns:
        FacilityUser: a reference to the admin account created

    """

    # check if a user or admin with the name passed in already exists
    user_exists = FacilityUser.objects.filter(username=admin_uname).exists()
    if user_exists:
        # if the user already exists, raise a value error and terminate the script
        raise ValueError(
            "There is already a user or admin called {}".format(admin_uname)
        )
        sys.exit()
    else:
        # if the user does not already exist
        # check if the facility passed in already exists
        try:
            # get a reference to the facility object with the name passed in
            facility_obj = Facility.objects.get(name=facilityname)

            # get the facility id and dataset id
            facility_id = facility_obj.id
            dataset_id = facility_obj.dataset_id

        # catch the exception when the object does not exist
        except ObjectDoesNotExist:
            # print out the id that does not exist
            raise ValueError(
                "Error: Facility with the name {} does not exist".format(facilityname)
            )
            # exit in an error state
            # if the facility does not exist, raise a value error and terminate the script
            sys.exit("Admin was not created successfully. Check the error(s) above")

        # generate a new user_id
        new_user_id = uuid.uuid4()

        # use the user_id and dataset_id from the facility object to create the morango partition
        _morango_partition = "{dataset_id}:user-ro:{user_id}".format(
            dataset_id=dataset_id, user_id=new_user_id
        )

        # an admin account is simply a user with an admin role for a facility
        # create a new user object with the username, password, and facility passed in (full name can be omitted)
        new_admin = FacilityUser.objects.create(
            username=admin_uname,
            password=make_password(admin_password),
            dataset_id=dataset_id,
            facility_id=facility_id,
            _morango_partition=_morango_partition,
            _morango_source_id=uuid.uuid4(),
        )

        # create a new admin role for the user that has just been created
        Role.objects.create(user=new_admin, collection=facility_obj, kind="admin")

    # return the newly created admin
    print("Admin : {} was created successfully".format(new_admin.username))
    return new_admin


def change_password(id, new_password):
    """Helper function to change the password of a FacilityUser specified by id

    Args:
        id (string): The id of the FacilityUser to change the password for
        new_password (string): The new password of the FacilityUser

    Returns:
        None
    """

    # get a reference to the user
    u = FacilityUser.objects.get(id=id)
    # change the password of the user
    u.password = make_password(new_password)
    # save the user object
    u.save()


# TODO: Write helper function to move users from one facility to another
# changes to kolibriauth_facilityuser,loggers
# morango_source = uuid
# morango_partition = dataset_id
# dataset_id = generated when new facility is created


def get_channels_in_module(modulename):
    """Function to get all channels with the module passed in
    Uses channel_metadata and channel_module tables
        Args:
            modulename (string): The module to get channels for

        Returns:
            A list of ChannelMetadata objects
    """

    # Query to get all channels that have the module specified
    channels_query = """select * from content_channelmetadata
    where id in
    (select channel_id from channel_module where module = '{}')""".format(
        modulename.lower()
    )

    # Use the query to get ChannelMetadata objects
    # can't use django ORM __in method because it doesnt work on uuid data type
    # Convert the rawquery to a list
    channels = list(ChannelMetadata.objects.raw(channels_query))

    # check that the channels for the passed in module exist
    if len(channels) == 0:
        # Raise a value error and exist the script if the list is empty
        raise ValueError(
            """No channels with the module {} were found.
            Check that the expected channel(s) have been imported, and exist in channel_module""".format(
                modulename
            )
        )
        sys.exit()

    # Return a list ChannelMetadata objects
    return channels


def get_channels_in_level(levelname):
    """Function to get all channels with the level passed in
    Uses channel_metadata table
        Args:
            levelname (string): The name of the level

        Returns:
            A list of ChannelMetadata objects
    """

    # Use the query to get ChannelMetadata objects
    # can't use django ORM __in method because it doesnt work on uuid data type
    # Convert the rawquery to a list
    channels = list(ChannelMetadata.objects.filter(name__contains = levelname))

    # check that the channels for the passed in level exist
    if len(channels) == 0:
        # Raise a value error and exist the script if the list is empty
        raise ValueError(
            """No channels with the Level name {} were found.
            Check that the expected channel(s) have been imported sucessfully""".format(
                levelname
            )
        )
        sys.exit()

    # Return a list ChannelMetadata objects
    return channels

def get_admins_for_facility(facility):
    """Get a list of admins and coaches for a Facility
    Args:
        facility (Facility): A Facility object
    Returns:
        A list of FacilityUser objects containing the admins and coaches for the Facility
    """

    admins_query = """select * from kolibriauth_facilityuser
    where id in
    (select user_id from kolibriauth_role where kind in ('admin','coach'))
    and facility_id = '{}'""".format(
        facility.id
    )

    admins = list(FacilityUser.objects.raw(admins_query))

    # if there is no admin or coach account on the device
    # raise an error and terminate the script
    if len(admins) == 0:
        raise ValueError(
            "There is no Admin or Coach account on the device. Cannot create quizzes without an Admin or Coach account "
        )
        sys.exit()

    return admins

def update_facilityuser_details():


    # ORM to retrieve all facility user daetails
    facility_users = FacilityUser.objects.all()

    # loop through the table to retieve user details
    for user in facility_users:

        # retrieved object to update and used function title() to update each of the objects to proper casing
        user.full_name.title()

        # save te changes to the database
        user.save()

        # ORM to retrieve retrieve update values
        updated_facility_users = FacilityUser.objects.values_list('full_name', flat=True)

        # loop through the table to retieve updated user details 
        for updated_user in updated_facility_users:

            # print updated user's full_name
            print("full_name: {}".format(updated_user)
            )
