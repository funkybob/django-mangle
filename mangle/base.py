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
            for path, storage in paths.items():
                yield SourceFile(self, path)

    def post_process(self, paths, **options):
        # Chain all the manglers
        source = self.source(paths, **options)
        for mangler in self.manglers:
            source = mangler.process(source)

        # Crank the handle
        for file_obj in source:
            if file_obj.save_pending:
                file_obj.save()
            yield str(file_obj.orig_path), str(file_obj.path), file_obj.processed


class SourceFile:
    def __init__(self, storage, path, orig_path=None, processed=False, save_pending=False):
        self.storage = storage
        self.path = PurePath(path)
        self.orig_path = PurePath(orig_path or path)
        self.processed = processed
        self.save_pending = save_pending

    def __str__(self):  # pragma: no cover
        return '"{}" from {} (was {})'.format(self.path, self.storage, self.orig_path)

    @cached_property
    def content(self):
        with self.storage.open(self.path) as source:
            return source.read().decode(settings.FILE_CHARSET)

    def save(self):
        self.storage._save(self.path, ContentFile(self.content))

    def delete(self, name=None):
        if name is None:
            name = self.path
        self.storage.delete(name)

    def fork(self, new_name, content):
        new_obj = SourceFile(self.storage, new_name, self.orig_path, processed=True, save_pending=True)
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
