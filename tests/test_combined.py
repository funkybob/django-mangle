import os

from django.test import override_settings

from . import StaticTestCase


BASE_DIR = os.path.dirname(__file__)


@override_settings(
    MANGLERS=[
        ('mangle.css.CssMangler', {}),
        ('mangle.js.JsMangler', {}),
        ('mangle.gzip.GzipMangler', {'extensions': ['.js', '.css', '.txt']}),
    ]
)
class MidedMixinTestCase(StaticTestCase):

    @override_settings(
        STATICFILES_DIRS=[os.path.join(BASE_DIR, 'files', 'mixed')],
    )
    def test_mixed(self):
        stats = self.collect()
        self.assertFileExists('input.min.js')
        self.assertFileExists('input.min.js.gz')
        self.assertFileExists('input.min.css')
        self.assertFileExists('input.min.css.gz')
        self.assertFileExists('input.txt')
        self.assertFileExists('input.txt.gz')
        self.assertFileNotExists('input.min.txt')
        self.assertFileNotExists('input.min.txt.gz')
