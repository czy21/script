#!/usr/bin/env python3
import logging
import pathlib

from domain.meta import mongo as mongo_meta
from domain.source import base as base_source
from utility import db as db_util, collection as list_util, basic as basic_util

logger = logging.getLogger()


class MongoSource(base_source.AbstractSource):

    def __init__(self, context: base_source.ExecutionContext) -> None:
        super().__init__(context)
        self.host = self.context.param.param_main_db_mongo_host
        self.port = self.context.param.param_main_db_mongo_port
        self.username = self.context.param.param_main_db_mongo_username
        self.password = self.context.param.param_main_db_mongo_password
        self.database = self.context.param.param_main_db_mongo_database

    def assemble(self) -> None:
        db_util.assemble_ql(pathlib.Path(self.context.param.param_main_db_mongo_file_path), pathlib.Path(self.context.param.output_db_all_in_one_mongo), mongo_meta, "mongo")

    def get_basic_uri(self, with_database=False) -> str:
        return "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(self.username, self.password, self.host, self.port, self.database if with_database else "")

    def get_recreate_command(self) -> str:
        return list_util.flat_to_str("mongo", self.get_basic_uri(False), [
            "--eval \"{0}\"".format("".join(
                [
                    "db = db.getSiblingDB('{0}');db.dropDatabase();".format(self.database)
                ])
            )
        ])

    def recreate(self) -> None:
        command = self.get_recreate_command()
        basic_util.execute(command)

    def execute(self) -> None:
        command = list_util.flat_to_str(
            "mongo", self.get_basic_uri(True),
            self.context.param.output_db_all_in_one_mongo
        )
        basic_util.execute(command, db_util.print_ql_msg)

    def backup(self) -> None:
        command = list_util.flat_to_str(
            "mongodump", f"--uri={self.get_basic_uri(True)}",
            f"--archive={self.context.param.output_db_bak_gz_mongo}",
            "--gzip"
        )
        basic_util.execute(command)
