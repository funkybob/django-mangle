import hashlib
from pathlib import PurePath

from .base import Mangler


class HashMangler(Mangler):

    def __init__(self, target, hash_name='md5', suffixes=None):
        super().__init__(target)
        self.hash_name = hash_name
        self.suffixes = suffixes or ['.css', '.js']

    def can_process(self, file_obj):
        return file_obj.current_name.suffix in self.suffixes

    def hash_file(self, content):
        return hashlib.new(self.hash_name, content).hexdigest()

    def process_file(self, file_obj):
        extensions = ''.join(file_obj.current_name.suffixes)
        ext_len = len(extensions)
        base_name = str(file_obj.current_name)[:-ext_len]

        hash_value = self.hash_file(file_obj.content)
        hash_name = '{}-{}{}'.format(base_name, hash_value, extensions)

        file_obj.current_name = PurePath(hash_name)
        yield file_obj
