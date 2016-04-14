from slimit import minify

from .base import Mangler


class JsMangler(Mangler):
    '''
    Mixin post-processor for minifying CSS files
    '''
    def __init__(self, target, mangle=True, mangle_toplevel=False):
        super().__init__(target)
        self.mangle = mangle
        self.mangle_toplevel = mangle_toplevel

    def can_process(self, file_obj):
        exts = file_obj.current_name.suffixes
        if exts[-1] != '.js':
            return False
        if len(exts) > 1 and exts[-2] == '.min':
            return False
        return True

    def process_file(self, file_obj):
        content = minify(file_obj.content,
                         mangle=self.mangle,
                         mangle_toplevel=self.mangle_toplevel)

        self.target.delete(file_obj.current_name)

        file_obj.content = content
        file_obj.add_suffix('.min', -2)
        yield file_obj
