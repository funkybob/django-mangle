import hashlib
from pathlib import PurePath

from .base import Mangler


class HashMangler(Mangler):

    def __init__(self, target, hash_name='md5', suffixes=None):
        super().__init__(target)
        self.hash_name = hash_name
        self.suffixes = suffixes or ['.css', '.js']

    def can_process(self, file_obj):
        return file_obj.path.suffix in self.suffixes

    def hash_file(self, content):
        return hashlib.new(self.hash_name, content).hexdigest()

    def process_file(self, file_obj):
        extensions = ''.join(file_obj.path.suffixes)
        ext_len = len(extensions)
        base_name = str(file_obj.path)[:-ext_len]

        hash_value = self.hash_file(file_obj.content.encode('utf-8'))
        hash_name = '{}-{}{}'.format(base_name, hash_value, extensions)
        print(hash_name)
        file_obj.path = PurePath(hash_name)
        file_obj.processed = True
        file_obj.save_pending = True
        return file_obj
