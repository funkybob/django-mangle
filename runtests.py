#!/usr/bin/env python

# Adapted from https://raw.githubusercontent.com/hzy/django-polarize/master/runtests.py
import os
import sys

from django.conf import settings
from django.core.management import execute_from_command_line

import django

HERE = os.path.dirname(__file__)

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=(
            'tests',
        ),
        MIDDLEWARE_CLASSES=[],
        ROOT_URLCONF='tests.urls',
        STATIC_URL='/static/',
        STATIC_ROOT=os.path.join(HERE, 'static', '_'),
    )


def runtests():
    argv = sys.argv[:1] + ['test', 'tests']
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
