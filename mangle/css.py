from rcssmin import cssmin

from .base import Mangler


class CssMangler(Mangler):
    '''
    Mixin post-processor for minifying CSS files
    '''
    def can_process(self, file_obj):
        exts = file_obj.path.suffixes
        if exts[-1] != '.css':
            return False
        if len(exts) > 1 and exts[-2] == '.min':
            return False
        return True

    def process_file(self, file_obj):
        content = cssmin(file_obj.content)

        file_obj.delete()

        file_obj.path = file_obj.path.stem + '.min.css'
        file_obj.content = content
        file_obj.processed = True
        file_obj.save_pending = True
        yield file_obj
