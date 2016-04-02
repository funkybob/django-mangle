import gzip

from .base import Mangler, SourceFile


class GzipMangler(Mangler):
    def __init__(self, target, extensions=None):
        self.extensions = extensions or ['.css', '.js']

    def can_process(self, file_obj):
        return file_obj.path.suffix in self.extensions

    def process_file(self, file_obj):
        content = gzip.compress(file_obj.content)
        new_file = file_obj.fork(file_obj.path + '.gz', content)
        yield orig_file
        yield new_file
