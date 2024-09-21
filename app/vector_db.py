import os

from llama_index.core import SQLDatabase
from llama_index.core.objects import ObjectIndex
from llama_index.core.program import LLMTextCompletionProgram
from sqlalchemy import Engine

from models.table import TableInfo
from prompts import prompts
from table import TableDescriber
from text_to_sql import VectorStoreRetriever


def initialize_vector_db(llm, engine: Engine, db: SQLDatabase) -> ObjectIndex:
    table_info_dir = os.getenv("LOCAL_PERSISTENCE_PATH")

    program = LLMTextCompletionProgram.from_defaults(
        output_cls=TableInfo,
        llm=llm,
        prompt_template_str=prompts.table_summary,
    )

    # Get table names and returns a list of SQLTableSchema with table names and general description
    describer = TableDescriber(engine, program, table_info_dir)
    tables_schemas = describer.get_descriptions()

    # Retrieve relevant information from Vector Store
    object_index = VectorStoreRetriever(db, tables_schemas)
    obj_retriever = object_index.get_retriever()

    return obj_retriever
