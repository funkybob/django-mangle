import os

from django.test import override_settings

from . import StaticTestCase


BASE_DIR = os.path.dirname(__file__)


@override_settings(
    MANGLERS=[
        ('mangle.hasher.HashMangler', {}),
    ]
)
class HasherMixinTestCase(StaticTestCase):

    @override_settings(
        STATICFILES_DIRS=[os.path.join(BASE_DIR, 'files', 'hash_no_mangle')]
    )
    def test_no_mangle(self):
        stats = self.collect()
        self.assertIn('input.txt', stats['modified'])
        self.assertFileExists('input.txt')

    @override_settings(
        STATICFILES_DIRS=[os.path.join(BASE_DIR, 'files', 'hash_mangle')]
    )
    def test_mangle(self):
        self.collect()
        self.assertFileExists('input-0342d868f2fed3adb5370472ad752bc8.css')
