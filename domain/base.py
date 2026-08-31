#!/usr/bin/env python3
import abc
import logging
import pathlib
import typing
from types import SimpleNamespace
from utility import db as db_util, collection as list_util, basic as basic_util, file as file_util

logger = logging.getLogger()

class EnhancedNamespace(SimpleNamespace):

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

class ExecutionContext(typing.NamedTuple):
    root_path: pathlib.Path
    output_path: pathlib.Path
    param: EnhancedNamespace

class AbstractDBSource(metaclass=abc.ABCMeta):
    def __init__(self, context: ExecutionContext) -> None:
        self.context = context

    def key(self) -> str:
        pass

    def ext(self) -> str:
        return 'sql'

    def assemble(self) -> None:
        everyone_prep_content = db_util.assemble_ql(pathlib.Path(self.context.param.get(f'param_main_db_{self.key()}_everyone_path')).joinpath("prep"), self.meta(), self.ext())
        version_content = db_util.assemble_ql(pathlib.Path(self.context.param.get(f'param_main_db_{self.key()}_version_path')), self.meta(), self.ext())
        everyone_post_content = db_util.assemble_ql(pathlib.Path(self.context.param.get(f'param_main_db_{self.key()}_everyone_path')).joinpath("post"), self.meta(), self.ext())
        file_util.write_text(pathlib.Path(self.output_db_all_in_one), u'{}'.format("\n\n".join([*everyone_prep_content,*version_content,*everyone_post_content])))
    
    def assemble_release(self) -> None:
        everyone_prep_content = db_util.assemble_ql(pathlib.Path(self.context.param.get(f'param_main_db_{self.key()}_everyone_path')).joinpath("prep"), self.meta(), self.ext())
        version_file = pathlib.Path(self.context.param.version_file)
        release_path = None
        release_name = self.context.param.get(f'param_main_db_{self.key()}_release_name',f"release-{version_file.read_text()}" if version_file.exists() else "")
        release_path = pathlib.Path(self.context.param.get(f'param_main_db_{self.key()}_version_path')).joinpath(release_name)
        if not self.context.param.get(f'param_main_db_{self.key()}_release_name') and not version_file.exists():
            raise Exception(f"param_main_db_{self.key()}_release_name must be not null")
        if not release_path.exists():
            raise Exception(f"{release_path.as_posix()} not exist")
        release_content = db_util.assemble_ql(release_path, self.meta(), self.ext())
        everyone_post_content = db_util.assemble_ql(pathlib.Path(self.context.param.get(f'param_main_db_{self.key()}_everyone_path')).joinpath("post"), self.meta(), self.ext())
        file_util.write_text(pathlib.Path(self.output_db_all_in_one), u'{}'.format("\n\n".join([*everyone_prep_content,*release_content,*everyone_post_content])))
