import kolibri  # noqa F401
import django

django.setup()

from create_lessons import create_lessons  # noqa E402
from create_quizzes import create_quizzes  # noqa E402
from helpers import get_or_create_classroom # noqa E402

# Create lessons and quizzes for the live learners cleass
# The class will be created if it does not exist
create_quizzes("numeracy", "Live Learners")
create_lessons("numeracy", "Live Learners")

# Create Learners on Program class if it does not exist
get_or_create_classroom("Learners on Program")

# Create Zarchive class if it does not exist
get_or_create_classroom("Zarchive")

