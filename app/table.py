from typing import List
from llama_index.core.bridge.pydantic import BaseModel
from llama_index.core.objects import SQLTableSchema
from llama_index.core.program import LLMTextCompletionProgram
from sqlalchemy import text, Sequence, Row, Engine

import db
from models.table import TableInfo
from pathlib import Path
import json


class TableDescriber:
    """
    A class to describe SQL tables and manage their information.

    This class is responsible for describing SQL tables by retrieving their information,
    parsing it, and saving it to the file system. It uses an LLMTextCompletionProgram
    to generate descriptions and manages the storage of these descriptions.
    """

    def __init__(
            self,
            engine: Engine,
            program: LLMTextCompletionProgram,
            table_info_dir: str,
    ):
        """
        Initializes the TableDescriber with the given engine, program, and directory.

        Args:
            engine (Engine): The SQLAlchemy engine connected to the database.
            program (LLMTextCompletionProgram): The program used to generate table descriptions.
            table_info_dir (str): The directory where table information files are stored.
        """
        self.table_info_dir = table_info_dir
        self.program = program
        self.conn = db.get_db_connection(engine)
        self.table_infos: List[SQLTableSchema] = []
        self.loaded_tables: set = set()
        self._create_folder()

    def _create_folder(self):
        """
        Creates the directory for storing table information files if it does not exist.
        """
        Path(self.table_info_dir).mkdir(parents=True, exist_ok=True)

    def _get_table_info_with_index(self, filename: str) -> TableInfo | None:
        """
        Retrieves table information for a given filename from the file system, validates it, and returns a TableInfo
        instance.

        Args:
            filename (str): The name of the file to retrieve table information from.

        Returns:
            TableInfo | None: The TableInfo instance if found and valid, otherwise None.
        """
        results_list = list(Path(self.table_info_dir).glob(f"{filename}*"))
        results_len = len(results_list)

        if results_len == 0:
            return None
        elif results_len == 1:
            path = results_list[0]
            return TableInfo.parse_file(path)
        else:
            raise ValueError(f"More than one file matching index: {results_list}")

    def _parse_table_info(self, rows: Sequence[Row], table_name: str) -> BaseModel | None:
        """
        Parses table information from database rows and returns a BaseModel instance.

        Args:
            rows (Sequence[Row]): The rows retrieved from the database.
            table_name (str): The name of the table being parsed.

        Returns:
            BaseModel | None: The parsed table information as a BaseModel (representing TableInfo Model) instance,
             or None if parsing fails.
        """
        try:
            table_info = self.program(
                table_str=rows,
                exclude_table_name_list=str(list(self.loaded_tables))
            )
            table_info.table_name = table_name

        except Exception as e:
            print(f"Error parsing table: {e}")
            return None

        return table_info

    def _add_table_name(self, table_info) -> bool:
        """
        Adds a table name to the set of loaded tables if it is not already present.

        Args:
            table_info: The table information containing the table name.

        Returns:
            bool: True if the table name was added, False if it was already present.
        """
        table_name = table_info.table_name
        if table_name not in self.loaded_tables:
            print(f"Processed table: {table_name}")
            self.loaded_tables.add(table_name)
            return True
        else:
            print(f"Table name {table_name} already exists. Skipping...")
            return False

    def _save_table_info_file(self, table_info, save_file):
        """
        Saves the table information to a file if save_file is True.

        Args:
            table_info: The table information to save.
            save_file (bool): Whether to save the file or not.
        """
        if not save_file:
            return
        out_file = f"{self.table_info_dir}/{table_info.table_name}.json"
        json.dump(table_info.dict(), open(out_file, "w"))

    def _process_parsing(self, table_name: str) -> BaseModel:
        """
        Processes the parsing of a table and saves its information.

        Args:
            table_name (str): The name of the table to process.

        Returns:
            BaseModel: The parsed table information.
        """
        rows = db.get_table_rows(self.conn, table_name)
        table_info = self._parse_table_info(rows, table_name)
        save_file = self._add_table_name(table_info)
        self._save_table_info_file(table_info, save_file)
        return table_info

    def get_descriptions(self):
        """
        Retrieves descriptions for all tables in the database.

        Returns:
            List[SQLTableSchema]: A list of SQLTableSchema instances containing table descriptions.
        """
        tables = db.get_all_tables(self.conn)

        for table_name in tables:
            table_info = self._get_table_info_with_index(table_name)

            if table_info is None:
                table_info = self._process_parsing(table_name)

            self.table_infos.append(
                SQLTableSchema(
                    table_name=table_info.table_name,
                    context_str=table_info.table_summary,
                ),
            )

        return self.table_infos
