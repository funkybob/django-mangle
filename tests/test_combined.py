import os

from django.test import override_settings

from . import StaticTestCase


BASE_DIR = os.path.dirname(__file__)


@override_settings(
    MANGLERS=[
        ('mangle.css.CssMangler', {}),
        ('mangle.js.JsMangler', {}),
        ('mangle.gzip.GzipMangler', {}),
    ]
)
class MidedMixinTestCase(StaticTestCase):

    @override_settings(
        STATICFILES_DIRS=[os.path.join(BASE_DIR, 'files', 'mixed')],
    )
    def test_mixed(self):
        stats = self.collect()
        print(stats)
