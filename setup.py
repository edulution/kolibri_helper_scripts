import kolibri  # noqa F401
import django

django.setup()

from kolibri.core.auth.models import Classroom

from create_lessons_by_level import create_lessons_by_level
from create_quizzes_by_level import create_quizzes_by_level

# Create classrooms first if needed
# from helpers import get_or_create_classroom
# get_or_create_classroom()

# Get a list of all of the existing classrooms
classroom_names = [str(c) for c in Classroom.objects.all()]

# Create lessons and Quizzes by level for each
for classroom in classroom_names:
    create_lessons_by_level(classroom)
    create_quizzes_by_level(classroom)
