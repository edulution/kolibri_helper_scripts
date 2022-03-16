import kolibri  # noqa F401
import django

import uuid
import random
from helpers import (
    get_facility_or_default,
    get_or_create_classroom,
    get_or_create_learnergroup,
    get_channels_in_module,
    get_channels_in_level,
    get_admins_for_facility,
)

django.setup()

from kolibri.core.auth.models import Facility, FacilityUser  # noqa E402
from kolibri.core.exams.models import Exam, ExamAssignment  # noqa E402
from kolibri.core.content.models import ContentNode, ChannelMetadata  # noqa E402
from le_utils.constants import content_kinds  # noqa E402


def create_revision_quizzes(
    classroomname,
    facilityname=None,
    levels=["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"],
):
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

    for level in levels:
        # get all channels with the level passed in
        channels = get_channels_in_level(level)

        # get a list of all the channel ids for the channels in the level
        channel_ids = [channel.id for channel in channels]

        # Get the exercise content nodes for all the channels within a level
        level_exercise_content = (
            ContentNode.objects.filter(
                channel_id__in=channel_ids, kind=content_kinds.EXERCISE
            )
            .exclude(parent_id__isnull=True)
            .order_by("sort_order")
        )

        # Number of revision quizzes to create
        num_revision_quizzes = 3

        # Loop to generate number of quizzes above
        for quiz_num in range(1, num_revision_quizzes + 1):
            # Set the quiz name
            quiz_title = level + " - " + "Revision Quiz " + str(quiz_num)

            # Set the quiz length (number of questions)
            quiz_length = 30

            # Placeholder var for the number of items in a quiz
            n_content_items = 0

            # initialize empty array to hold the content
            quiz_content = []

            # Loop until we have number of items in a quiz = quiz length
            while n_content_items < quiz_length:
                # If there is only 1 exercise, break the loop and don't create the quiz
                if len(level_exercise_content) < 2:
                    break
                else:
                    # Randomly select an exercise content node in the topic to add to the quiz
                    random_node = random.choice(level_exercise_content)

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
                print "Could not cerate quiz {}. Not enough content".format(
                    str(quiz_title)
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
                print (
                    "Quiz {} created in class {} with {} content items".format(
                        str(new_quiz.title),
                        str(class_for_quizzes.name),
                        str(n_content_items),
                    )
                )

                # get or create a group to assign the quiz to based on the channel name
                group_for_quiz = get_or_create_learnergroup(
                    level, classroomname, facilityname
                )

                # create an ExamAssignment object to assign the quiz to a group
                ExamAssignment.objects.create(
                    exam=new_quiz,
                    collection=group_for_quiz,
                    assigned_by=admin_for_quizzes,
                )

                # inform the user that the quiz has been assigned successfully
                print (
                    "Quiz {} assigned to group {}".format(
                        str(new_quiz.title), str(group_for_quiz.name)
                    )
                )
