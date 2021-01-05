# A script to rename the Numeracy class in Kolibri to Learners on Program

import kolibri  # noqa F401
import django

import sys
import argparse
from django.core.exceptions import ObjectDoesNotExist

django.setup()

from kolibri.core.auth.models import Classroom  # noqa E402

argParser = argparse.ArgumentParser()
argParser.add_argument(
    "--old_name", "-o", help="Current name of the class you with to rename"
)
argParser.add_argument(
    "--new_name", "-n", help="New name of the class you with to rename"
)


def rename_class(old_name, new_name):
    try:
        Classroom.objects.get(name=old_name)
    except ObjectDoesNotExist:
        print("A classroom with the name {} was not found".format(old_name))
        sys.exit("The Classroom was not renamed. Please check the error(s) above")

    # get a reference to the classroom object to rename
    class_to_rename = Classroom.objects.get(name=old_name)

    # change to name of the class
    class_to_rename.name = new_name
    # save the object
    class_to_rename.save()

    # print a message to the console to indicate that it was successful
    print("Done! Class {} was renamed to {}".format(old_name, new_name))


if __name__ == "__main__":
    args = argParser.parse_args()
    if args.old_name and args.new_name:
        old_name = args.old_name
        new_name = args.new_name
        rename_class(old_name, new_name)
    else:
        sys.exit(
            "Please supply the old name and new name of the class with the appropriate arguments"
        )
