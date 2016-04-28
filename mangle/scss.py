from scss.compiler import Compiler
from scss.errors import SassSyntaxError

from .base import Mangler


class ScssMangler(Mangler):
    '''
    Mangle SASS/SCSS.
    '''
    def __init__(self, target, extensions=None, include_paths=None):
        super().__init__(target)
        self.extensions = extensions or ['.sass', '.scss']
        self.include_paths = include_paths or []
        self.compiler = Compiler(search_path=self.include_paths)

    def can_process(self, file_obj):
        return file_obj.current_name.suffix in self.extensions

    def process_file(self, file_obj):
        content = self.compiler.compile_string(file_obj.str)

        self.target.delete(file_obj.current_name)

        file_obj.str = content
        file_obj.current_name = file_obj.current_name.with_suffix('.css')
        yield file_obj
