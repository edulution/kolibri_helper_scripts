import kolibri  # noqa F401
import django
from colors import *

django.setup()

from kolibri.core.lessons.models import Lesson
from kolibri.core.exams.models import Exam
from kolibri.core.auth.models import Classroom, LearnerGroup

from create_lessons_by_topic import create_lessons_by_topic
from create_quizzes_by_topic import create_quizzes_by_topic
from create_level_revision_quizzes import create_revision_quizzes

# To avoid creating duplicate groups, lesson or quizzes

# Delete all groups
LearnerGroup.objects.all().delete()
print_colored(
    "Deleting all existing Groups",
    colors.fg.yellow,
)

# Delete all lessons
Lesson.objects.all().delete()
print_colored(
    "Deleting all existing Lessons",
    colors.fg.yellow,
)

# Delete all quizzes
Exam.objects.all().delete()
print_colored(
    "Deleting all existing Quizzes",
    colors.fg.yellow,
)

# Get a list of all of the existing classrooms
classrooms = Classroom.objects.all()

for classroom in classrooms:
    # Get the facility for each classroom
    facility_for_class = classroom.get_facility()

    # Get the facility name
    facility_name = str(facility_for_class.name)

    # Get the name of the classroom from the object
    classroom_name = str(classroom.name)

    # Now create lessons, quizzes and revision quizzes passing in classroom and facility
    create_lessons_by_topic(classroomname=classroom_name, facilityname=facility_name)
    create_quizzes_by_topic(classroomname=classroom_name, facilityname=facility_name)
    create_revision_quizzes(classroomname=classroom_name, facilityname=facility_name)
