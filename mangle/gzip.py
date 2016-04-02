import gzip

from django.conf import settings

from .base import Mangler, SourceFile


class GzipMangler(Mangler):
    def __init__(self, target, extensions=None):
        self.extensions = extensions or ['.css', '.js']

    def can_process(self, file_obj):
        return file_obj.path.suffix in self.extensions

    def process_file(self, file_obj):
        content = gzip.compress(file_obj.content.encode(settings.FILE_CHARSET))
        new_file = file_obj.fork(str(file_obj.path) + '.gz', content)
        yield file_obj
        yield new_file
