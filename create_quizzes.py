import kolibri  # noqa F401
import django
import uuid
import random
from colors import *
from helpers import (
    get_facility_or_default,
    get_or_create_classroom,
    get_or_create_learnergroup,
    get_channels_in_module,
    get_admins_for_facility,
)

django.setup()

from kolibri.core.auth.models import Facility, FacilityUser  # noqa E402
from kolibri.core.exams.models import Exam, ExamAssignment  # noqa E402
from kolibri.core.content.models import ContentNode, ChannelMetadata  # noqa E402
from le_utils.constants import content_kinds  # noqa E402


def create_quizzes(modulename, classroomname, facilityname=None):
    """Function that creates 1 quiz for each topic in each channel having the module passed in
    each quiz contains 10 questions
    e.g create_quizzes('numeracy','a1') will create 1 quiz for each topic in each numeracy channel

    Args:
        modulename (string): Name of the module
        classroomname (string): Name of the classroom to create the quizzes in
        facilityname (string): Name of the facility to create the quizzes for(default facility if not specified)

    Returns:
        None
    """

    # get a reference to the facility to create the lessons in
    facility_for_quizzes = get_facility_or_default(facilityname)

    # set the seed that will be used to generate the sequence of exam_ids
    seed = random.randint(1, 100)
    # get or create the class to create the quizzes for
    # store a reference to the classroom object if it is created
    class_for_quizzes = get_or_create_classroom(classroomname, facilityname)

    # get a list of the admin and coach accounts on the device
    admin_for_quizzes = get_admins_for_facility(facility_for_quizzes)[0]

    # get all channels with the module passed in
    channels = get_channels_in_module(modulename)

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
            # create the title for the Quiz using the  title of the topic + the channel name
            quiz_title = (
                str(ContentNode.objects.get(id=topic_id).title) + " - " + channel_name
            )

            # Quiz titles have a constraint of 50 characters
            # if this is exceeded, remove the difference from the Quiz title
            if len(quiz_title) > 50:
                diff_len = len(quiz_title) - 50
                quiz_title = (
                    str(ContentNode.objects.get(id=topic_id).title[:-diff_len])
                    + " - "
                    + channel_name
                )

            # filter only the exercises in the topic
            # assumes that the next level beneath a topic is an exercise/video
            exercise_content = ContentNode.objects.filter(
                parent_id=topic_id, kind=content_kinds.EXERCISE
            )

            # Set the quiz length
            quiz_length = 20

            # Placeholder var for the number of items in a quiz
            n_content_items = 0

            # initialize empty array to hold the content
            quiz_content = []

            # Loop until we have number of items in a quiz = quiz length
            while n_content_items < quiz_length:
                # If there is only 1 exercise, break the loop and don't create the quiz
                if len(exercise_content) < 2:
                    break
                else:
                    # Randomly select an exercise content node in the topic to add to the quiz
                    random_node = random.choice(exercise_content)

                # grab this exercise node's assessment ids
                # assessment_item_ids = random_node.assessmentmetadata.first().assessment_item_ids
                assessment_item_ids = (
                    random_node.assessmentmetadata.first().assessment_item_ids
                )

                # select a random assessment item from the assessment items of the exercise
                # create a json object with information about the exerise node and the random assessment id chosen
                content = {
                    "exercise_id": random_node.id,
                    "question_id": random.choice(assessment_item_ids),
                    "title": random_node.title,
                }

                # append the content json object to the quiz_content array
                # quiz_content.append(content)
                quiz_content.append(content)

                # increment number of items by 1
                n_content_items += 1

            # If there werent enough items to make a quiz, inform the user
            if len(quiz_content) == 0:
                print(
                    "Could not cerate quiz {}. Not enough content".format(
                        str(quiz_title)
                    ),
                    colors.fg.red,
                )

            else:
                # create a new quiz object with the content items gathered above
                # use uuid1 with a set seed to make pseudo-random uuids
                new_quiz = Exam.objects.create(
                    id=uuid.uuid1(node=None, clock_seq=seed),
                    title=quiz_title,
                    question_count=n_content_items,
                    question_sources=quiz_content,
                    active=True,
                    collection=class_for_quizzes,
                    creator=admin_for_quizzes,
                    data_model_version=1,
                )

                # Inform the user that the new quiz has been generated in the class
                # Print('Quiz {} created in class {}'.format(str(new_quiz.title), str(class_for_quizzes.name)))
                print_colored(
                    "Quiz {} created in class {} with {} content items".format(
                        str(new_quiz.title),
                        str(class_for_quizzes.name),
                        str(n_content_items),
                        colors.fg.yellow,
                    )
                )

                # get or create a group to assign the quiz to based on the channel name
                group_for_quiz = get_or_create_learnergroup(
                    channel_name, classroomname, facilityname
                )

                # create an ExamAssignment object to assign the quiz to a group
                ExamAssignment.objects.create(
                    exam=new_quiz,
                    collection=group_for_quiz,
                    assigned_by=admin_for_quizzes,
                )

                # inform the user that the quiz has been assigned successfully
                print_colored(
                    "Quiz {} assigned to group {}".format(
                        str(new_quiz.title),
                        str(group_for_quiz.name),
                        colors.fg.green,
                    )
                )
