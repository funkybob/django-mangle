import os

from django.test import override_settings


from . import StaticTestCase


BASE_DIR = os.path.dirname(__file__)


@override_settings(
    MANGLERS=[
        ('mangle.gzip.GzipMangler', {}),
    ]
)
class CssMixinTestCase(StaticTestCase):

    @override_settings(
        STATICFILES_DIRS=[os.path.join(BASE_DIR, 'files', 'css_no_mangle')]
    )
    def test_no_mangle(self):
        stats = self.collect()
        self.assertIn('input.txt', stats['modified'])
        self.assertFileExists('input.txt')

    @override_settings(
        STATICFILES_DIRS=[os.path.join(BASE_DIR, 'files', 'gzip_mangle')]
    )
    def test_mangle(self):
        self.collect()
        self.assertFileExists('input.css')
        self.assertFileExists('input.css.gz')

    @override_settings(
        STATICFILES_DIRS=[os.path.join(BASE_DIR, 'files', 'gzip_premin')]
    )
    def test_premin(self):
        stats = self.collect()
        self.assertIn('input.txt.gz', stats['modified'])
