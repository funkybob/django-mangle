from pathlib import PurePath

from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

# Manglers:
# - CSS Minify
# - GZipper

# - JS Minify
# - SASS Compiler
# - RequiresJS config builder


class ManglerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        manglers = []
        for path, config in getattr(settings, 'MANGLERS', []):
            klass = import_string(path)
            manglers.append(klass(self, **config))
        self.manglers = tuple(manglers)

    def source(self, paths, **options):
        if hasattr(super(), 'post_pocess'):
            for orig_path, path, processed in super().post_process(paths, **options):
                yield SourceFile(self, path, orig_path, processed)
        else:
            for prefixed_path, (storage, path) in paths.items():
                yield SourceFile(storage, prefixed_path, path)

    def post_process(self, paths, **options):
        # Chain all the manglers
        source = self.source(paths, **options)
        for mangler in self.manglers:
            source = mangler.process(source)

        # Crank the handle
        for file_obj in source:
            print("Saving to {}".format(file_obj.current_name))
            self._save(str(file_obj.current_name), ContentFile(file_obj.content))
            yield str(file_obj.original_name), str(file_obj.current_name), True


class SourceFile:
    def __init__(self, storage, original_name, current_name=None):
        self.storage = storage
        self.original_name = PurePath(original_name)
        self.current_name = PurePath(current_name or original_name)

    @cached_property
    def content(self):
        with self.storage.open(self.original_name) as source:
            return source.read().decode(settings.FILE_CHARSET)

    def fork(self, new_name, content):
        new_obj = SourceFile(self.storage, self.original_name, new_name)
        new_obj.content = content
        return new_obj


class Mangler:

    def __init__(self, target):
        self.target = target

    def process(self, processor):
        for file_obj in processor:

            if self.can_process(file_obj):
                yield from self.process_file(file_obj)

    def can_process(self, file_obj):  # pragma: no cover
        return False

    def process_file(self, file_obj):  # pragma: no cover
        raise NotImplementedError
