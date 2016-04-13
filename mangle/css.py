from rcssmin import cssmin

from .base import Mangler


class CssMangler(Mangler):
    '''
    Mixin post-processor for minifying CSS files
    '''
    def can_process(self, file_obj):
        exts = file_obj.current_name.suffixes
        if exts[-1] != '.css':
            return False
        if len(exts) > 1 and exts[-2] == '.min':
            return False
        return True

    def process_file(self, file_obj):
        content = cssmin(file_obj.content)

        self.target.delete(file_obj.current_name)

        file_obj = file_obj.fork(file_obj.current_name.stem + '.min.css', content)
        yield file_obj
