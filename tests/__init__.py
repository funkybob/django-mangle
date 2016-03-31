import shutil
import os

from django.conf import settings
from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectstaticCommand
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.test import SimpleTestCase, override_settings

import mangle

COLLECTSTATIC_ARGS = {
    'interactive': False,
    'verbosity': 0,
    'link': False,
    'clear': False,
    'dry_run': False,
    'post_process': True,
    'use_default_ignore_patterns': True,
    'ignore_patterns': ['*.ignoreme'],
}


class CustomStorage(mangle.ManglerMixin, StaticFilesStorage):
    pass


@override_settings(STATICFILES_STORAGE='tests.CustomStorage')
class StaticTestCase(SimpleTestCase):

    def setUp(self):
        try:
            shutil.rmtree(settings.STATIC_ROOT)
        except FileNotFoundError:
            pass

    def assertFileExists(self, name):
        full_path = os.path.join(settings.STATIC_ROOT, name)
        assert os.path.isfile(full_path), 'Could not find file at {}'.format(full_path)

    def assertFileNotExists(self, name):
        full_path = os.path.join(settings.STATIC_ROOT, name)
        assert not os.path.exists(full_path), 'Unexpected file found at {}'.format(full_path)

    def collect(self):
        collectstatic_cmd = CollectstaticCommand()
        collectstatic_cmd.set_options(**COLLECTSTATIC_ARGS)
        return collectstatic_cmd.collect()
