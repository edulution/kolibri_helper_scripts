# import kolibri and django to ensure that the script runs in kolibri shell
import kolibri  # noqa F401
import django
import random
import uuid
from colors import *
from helpers import (
    get_channels_in_module,
    get_channels_in_level,
    get_facility_or_default,
    get_or_create_classroom,
    get_or_create_learnergroup,
    get_admins_for_facility,
)

django.setup()

# import all the helper functions
from kolibri.core.auth.models import Facility, FacilityUser  # noqa E402
from kolibri.core.lessons.models import Lesson, LessonAssignment  # noqa E402
from kolibri.core.content.models import ContentNode, ChannelMetadata  # noqa E402


def create_lessons_by_topic(
    classroomname,
    facilityname=None,
    levels=["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6"],
):
    """Function to create 1  Lesson for each topic in each Channel for a specified Module, then assign them to a Classroom.
    The Classroom object is created if it does not exist.

    Args:
        modulename (string): name of the module
        classroomname (string): name of the class
        facilityname (string): name of the facility (default facility if not specified)

    Returns:
        None
    """

    # get a reference to the facility to create the lessons in
    facility_for_lessons = get_facility_or_default(facilityname)

    # set the seed that will be used to generate the sequence of lesson_ids
    seed = random.randint(1, 100)
    # get or create the class to create the lessons for
    # store a reference to the classroom object if it is created
    class_for_lessons = get_or_create_classroom(classroomname, facilityname)

    # get a list of the admin and coach accounts on the device
    # use raw query because __in ORM method doesn't work with uuid data type
    admin_for_lessons = get_admins_for_facility(facility_for_lessons)[0]

    for level in levels:
        # get all channels with the module passed in
        channels = get_channels_in_level(level)

        # get a list of all the channel ids for the channels in the above query
        channel_ids = [channel.id for channel in channels]

        # loop through the channels with the module passed in
        for channel_id in channel_ids:
            # get the channel name for use in the inner loop
            channel_name = str(ChannelMetadata.objects.get(id=channel_id).name)

            # channels are found in topics but have no parent_id and id == parent_id
            # get all topics by getting all contentnodes of type topic which fulfil criteria above
            topics = (
                ContentNode.objects.filter(kind="topic", parent_id=channel_id)
                .exclude(parent_id__isnull=True)
                .order_by("sort_order")
            )

            # get contentnode_ids of all the topics as an array
            topic_ids = [topic.id for topic in topics]

            # begin looping through topics
            for topic_id in topic_ids:
                # create the title for the lesson using the  title of the topic + the channel name
                lesson_title = (
                    str(ContentNode.objects.get(id=topic_id).title)
                    + " - "
                    + channel_name
                )

                # lesson titles have a constraint of 50 characters
                # if this is exceeded, remove the difference from the topic title
                if len(lesson_title) > 50:
                    diff_len = len(lesson_title) - 50
                    lesson_title = (
                        str(ContentNode.objects.get(id=topic_id).title[:-diff_len])
                        + " - "
                        + channel_name
                    )

                # instantiate a new lesson object for the topic
                # title, collection and created by are needed to instantiate a lesson object. Other attributes can be set later
                # set the title of the lesson as the title of the topic + the channel name
                lesson_for_topic = Lesson.objects.create(
                    id=uuid.uuid1(node=None, clock_seq=seed),
                    title=lesson_title,
                    collection=class_for_lessons,
                    created_by=admin_for_lessons,
                    _morango_source_id=uuid.uuid4(),
                )

                # get the child nodes of the topic
                child_nodes = ContentNode.objects.filter(parent_id=topic_id)

                # create an array of the resources for the lesson
                # structure of content resource in a lesson
                # {
                #   contentnode_id: string,
                #   content_id: string,
                #   channel_id: string
                # }

                lesson_for_topic.resources = [
                    {
                        "contentnode_id": node.id,
                        "content_id": node.content_id,
                        "channel_id": node.channel_id,
                    }
                    for node in child_nodes
                ]

                # set the morango partition the lesson
                lesson_for_topic._morango_partition = (
                    lesson_for_topic.calculate_partition()
                )

                # inform the user that the lesson has been created
                print_colored(
                    "Created Lesson {} with {} resources".format(
                        lesson_title, len(lesson_for_topic.resources)
                    ),
                    colors.fg.lightblue,
                )

                # get or create a group with the same name as the channel and assign the lesson to it
                group_for_lesson = get_or_create_learnergroup(
                    level, classroomname, facilityname
                )

                # create a new lesson assignment object
                LessonAssignment.objects.create(
                    lesson=lesson_for_topic,
                    collection=group_for_lesson,
                    assigned_by=admin_for_lessons,
                )

                # inform the user that the lesson has been created
                print_colored(
                    "Lesson {} successfully assigned to Group {}".format(
                        lesson_title, str(group_for_lesson.name)
                    ),
                    colors.fg.lightblue,
                )

                # activate the lesson
                lesson_for_topic.is_active = True

                # save the lesson object
                lesson_for_topic.save()
