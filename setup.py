import kolibri  # noqa F401
import django

django.setup()

from create_lessons import create_lessons  # noqa E402
from create_quizzes import create_quizzes  # noqa E402
from create_class import create_class # noqa E402

# Create lessons and quizzes for the live learners cleass
# The class will be created if it does not exist
create_quizzes("numeracy", "Live Learners")
create_lessons("numeracy", "Live Learners")
create_class("Leaners on Program")
create_class("Zarchive")

