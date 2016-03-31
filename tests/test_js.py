import os

from django.test import override_settings

from . import StaticTestCase


BASE_DIR = os.path.dirname(__file__)


@override_settings(
    MANGLERS=[
        ('mangle.js.JsMangler', {}),
    ]
)
class JsMixinTestCase(StaticTestCase):

    @override_settings(
        STATICFILES_DIRS=[os.path.join(BASE_DIR, 'files', 'js_no_mangle')]
    )
    def test_no_mangle(self):
        stats = self.collect()
        self.assertIn('input.txt', stats['modified'])
        self.assertFileExists('input.txt')

    @override_settings(
        STATICFILES_DIRS=[os.path.join(BASE_DIR, 'files', 'js_mangle')]
    )
    def test_mangle(self):
        self.collect()
        self.assertFileExists('input.min.js')
        self.assertFileNotExists('input.js')

    @override_settings(
        STATICFILES_DIRS=[os.path.join(BASE_DIR, 'files', 'js_premin')]
    )
    def test_premin(self):
        stats = self.collect()
        self.assertIn('input.min.js', stats['modified'])
