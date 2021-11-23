import kolibri  # noqa F401
import django

django.setup()

from kolibri.core.lessons.models import Lesson
from kolibri.core.exams.models import Exam
from kolibri.core.auth.models import Classroom, LearnerGroup

from create_lessons_by_level import create_lessons_by_level
from create_quizzes_by_level import create_quizzes_by_level

# To avoid creating duplicate groups, lesson or quizzes

# Delete all groups
LearnerGroup.objects.all().delete()
print("Deleting all existing Groups")

# Delete all lessons
Lesson.objects.all().delete()
print("Deleting all existing Lessons")

# Delete all quizzes
Exam.objects.all().delete()
print("Deleting all existing Quizzes")

# Get a list of all of the existing classrooms
classroom_names = [str(c) for c in Classroom.objects.all()]

# Create lessons and Quizzes by level for each classroom
for classroom in classroom_names:
    create_lessons_by_level(classroom)
    create_quizzes_by_level(classroom)
