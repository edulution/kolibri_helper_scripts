import kolibri # noqa F401
import django
from helpers import *
from create_lessons import create_quizzes
from create_quizzes import create_lessons

django.setup()

# Create lessons and quizzes for the live learners cleass
# The class will be created if it does not exist
create_quizzes('numeracy', 'Live Learners')
create_lessons('numeracy', 'Live Learners')
