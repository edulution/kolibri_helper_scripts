# import kolibri and django to ensure that the script runs in kolibri shell
import kolibri
import django

# import all the helper functions
from helpers import *
django.setup()


# creates 1 quiz for each topic in each channel having the module passed in (module specified in channel_module table)
# each quiz contains 10 questions


# e.g create_quizzes('numeracy','a1') will create 1 quiz for each topic in each numeracy channel
def create_quizzes(modulename, classroomname, facilityname=None):
    # set the seed that will be used to generate the sequence of exam_ids
    seed = random.randint(1, 100)
    # get or create the class to create the quizzes for
    # store a reference to the classroom object if it is created
    class_for_quizzes = get_or_create_classroom(classroomname, facilityname)

    # get a list of the admin and coach accounts on the device
    admins = FacilityUser.objects.raw("select * from kolibriauth_facilityuser where id in (select user_id from kolibriauth_role where kind in ('admin','coach'))")

    # if there is no admin or coach account on the device
    # raise an error and terminate the script
    if len(list(admins)) == 0:
        raise ValueError('There is no Admin or Coach account on the device. Cannot create quizzes without an Admin or Coach account ')
        sys.exit()
    else:
        # if admin accounts exist, choose the first one and use it to create and assign the quizzes
        admin_for_quizzes = admins[0]

    # get all channels with the module passed in
    channels = ChannelMetadata.objects.raw("select * from content_channelmetadata where id in (select channel_id from channel_module where module = %s)", [modulename.lower()])

    # get a list of all the channel ids for the channels in the above query
    channel_ids = [channel.id for channel in channels]

    # if there are no channel_ids, then there are no channels that have the module requested
    # raise an error and terminate the script
    if len(channel_ids) == 0:
        raise ValueError('There are no channels with a Module called {}. Cannot create quizzes without channels '.format(modulename))
        sys.exit()

    # loop through the channels with the module passed in
    for channel_id in channel_ids:
        # get the channel name for use in the inner loop
        channel_name = str(ChannelMetadata.objects.get(id=channel_id).name)

        # channels are found in topics but have no parent_id and id == parent_id
        # get all topics by getting all contentnodes of type topic which fulfil criteria above
        topics = ContentNode.objects.filter(kind='topic', parent_id=channel_id).exclude(parent_id__isnull=True).order_by('sort_order')

        # get contentnode_ids of all the topics as an array
        topic_ids = [topic.id for topic in topics]

        # begin looping through topics
        for topic_id in topic_ids:
            # create the title for the lesson using the  title of the topic + the channel name
            quiz_title = str(ContentNode.objects.get(id=topic_id).title)+' - '+channel_name

            # lesson titles have a constraint of 50 characters
            # if this is exceeded, remove the difference from the topic title
            if len(quiz_title) > 50:
                diff_len = len(quiz_title) - 50
                quiz_title = str(ContentNode.objects.get(id=topic_id).title[:-diff_len])+' - '+channel_name

            # filter only the exercises in the topic
            # assumes that the next level beneath a topic is an exercise/video
            exercise_content = ContentNode.objects.filter(parent_id=topic_id, kind=content_kinds.EXERCISE)

            # only add 10 exercises in a quiz:
            n_content_items = 10

            # initialize empty array to hold the content
            quiz_content = []

            for i in range(0, n_content_items):
                # Randomly select an exercise content node in the topic to add to the quiz
                random_node = random.choice(exercise_content)

                # grab this exercise node's assessment ids
                assessment_item_ids = random_node.assessmentmetadata.first().assessment_item_ids

                # select a random assessment item from the assessment items of the exercise
                # create a json object with information about the exerise node and the random assessment id chosen
                content = {"exercise_id": random_node.id, "question_id": random.choice(assessment_item_ids), "title": random_node.title}

                # append the content json object to the quiz_content array
                quiz_content.append(content)

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
            print('Quiz {} created in class {}'.format(str(new_quiz.title), str(class_for_quizzes.name)))

            # get or create a group to assign the quiz to based on the channel name
            group_for_quiz = get_or_create_learnergroup(channel_name, classroomname, facilityname)

            # create an ExamAssignment object to assign the quiz to a group
            ExamAssignment.objects.create(
                exam=new_quiz,
                collection=group_for_quiz,
                assigned_by=admin_for_quizzes
            )

            # inform the user that the quiz has been assigned successfully
            print('Quiz {} assigned to group {}'.format(str(new_quiz.title), str(group_for_quiz.name)))
