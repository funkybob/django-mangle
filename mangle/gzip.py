import gzip

from .base import Mangler


class GzipMangler(Mangler):
    def __init__(self, target, extensions=None):
        self.extensions = extensions or ['.css', '.js']

    def can_process(self, file_obj):
        return file_obj.current_name.suffix in self.extensions

    def process_file(self, file_obj):
        content = gzip.compress(file_obj.content)
        new_file = file_obj.fork(str(file_obj.current_name) + '.gz', content)
        yield file_obj
        yield new_file
