import kolibri
import django
django.setup()

from helpers import *
from create_lessons import *
from create_quizzes import *


# Create lessons and quizzes for the live learners cleass
# The class will be created if it does not exist
create_quizzes('numeracy','Live Learners')
create_lessons('numeracy','Live Learners')
