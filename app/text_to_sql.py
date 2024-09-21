from typing import List

from llama_index.core import SQLDatabase, VectorStoreIndex
from llama_index.core.objects import ObjectIndex, SQLTableSchema
from llama_index.core.query_pipeline import FnComponent
from llama_index.core.llms import ChatResponse
from llama_index.core.objects import (
    SQLTableNodeMapping,
)


class VectorStoreRetriever:
    """
    A class to retrieve relevant information from a vector store.

    This class provides methods to create a mapping of SQL tables and retrieve relevant information
    from a vector store using the provided table schemas.
    """

    def __init__(self, db, table_schemas, top_k=3):
        """
        Initializes the VectorStoreRetriever with the given database, table schemas, and top_k value.

        Args:
            db (SQLDatabase): The database object used to retrieve table information.
            table_schemas (List[SQLTableSchema]): A list of table schemas to be used for retrieval.
            top_k (int): The number of top similar items to retrieve from the vector store.
        """
        self.db: SQLDatabase = db
        self.table_schemas: List[SQLTableSchema] = table_schemas
        self.top_k: int = top_k

    def get_mapping(self):
        """
        Creates a mapping of SQL tables.

        A mapping of SQL tables refers to a structured representation that links or associates SQL tables
        with their corresponding metadata or schema information. This mapping typically includes details
        such as table names, column names, data types, relationships between tables (e.g., foreign keys),
        and other relevant attributes. The purpose of this mapping is to provide a comprehensive overview
        of the database structure, which can be used for various tasks such as query generation, data
        retrieval, and schema validation.

        Returns:
            SQLTableNodeMapping: The mapping of SQL tables.
    """
        return SQLTableNodeMapping(self.db)

    def get_retriever(self):
        """
        Creates a retriever object from the vector store using the table schemas and mapping.

        Returns:
            ObjectIndex: The retriever object for the vector store.
        """
        index = ObjectIndex.from_objects(
            self.table_schemas,
            self.get_mapping(),
            index_cls=VectorStoreIndex,
        )

        return index.as_retriever(similarity_top_k=self.top_k)


class TableContextCreator:
    """
    A class to create and manage table contexts within a database.

    This class provides methods to create table schemas, retrieve table information, and generate context
    strings for tables in a database.
    """

    def __init__(self, db):
        """
        Initializes the TableContextCreator with the given database.

        Args:
            db (SQLDatabase): The database object used to retrieve table information.
        """
        self.db = db

    @staticmethod
    def create_full_context(table_info, table_context):
        """
        Creates a full context string by combining table information and table context.

        Args:
            table_info (str): The information about the table.
            table_context (str): The context description of the table.

        Returns:
            str: The combined full context string.
        """
        if table_context:
            return table_info + " The table description is: " + table_context

        return table_info

    def get_info(self, table_name: str):
        """
        Retrieves table information.

        This method fetches the table information for a specified table name from the database.
        The information includes the table name and column types (e.g., INTEGER, VARCHAR, TIMESTAMP).

        Args:
            table_name (str): The name of the table to retrieve information for.

        Returns:
            str: The table information.
        """
        return self.db.get_single_table_info(table_name)

    def get_contexts(self, tables_schemas):
        """
        Generates context strings for a list of tables.

        This method creates table schemas and retrieves table information to generate context strings
        for each table in the provided list.

        Args:
            tables_schemas (List[SQLTableSchema]): A list of table schemas to generate contexts for.

        Returns:
            str: The combined context strings for all tables.
        """
        descriptions = []

        for table in tables_schemas:
            table_info = self.get_info(table.table_name)
            table_description = self.create_full_context(table_info, table.context_str)
            descriptions.append(table_description)

        return "\n\n".join(descriptions)

    def get_component(self):
        """
        Returns a function component that generates context strings for tables.

        Returns:
            FnComponent: A function component that generates context strings for tables.
        """
        return FnComponent(fn=self.get_contexts)


class LlmResponseParser:
    """
    A class to parse responses from a language model into SQL queries.

    This class provides methods to extract and clean SQL queries from the responses generated by a language model.
    """

    @staticmethod
    def parse_response_to_sql(response: ChatResponse) -> str:
        """
        Parses the response from a language model to extract the SQL query.

        This method looks for specific prefixes in the response content to identify and extract the SQL query.
        It then cleans the extracted query by removing unnecessary characters and formatting.

        Args:
            response (ChatResponse): The response object from the language model containing the message content.

        Returns:
            str: The cleaned SQL query extracted from the response.
        """
        sql_query_prefix = "SQLQuery:"
        sql_result_prefix = "SQLResult:"

        response_content = response.message.content
        sql_query_start_index = response_content.find(sql_query_prefix)
        sql_result_start_index = response_content.find(sql_result_prefix)

        if sql_query_start_index != -1:
            response_content = response_content[sql_query_start_index + len(sql_query_prefix):]

        if sql_result_start_index != -1:
            response_content = response_content[:sql_result_start_index]

        cleaned_sql_query = response_content.strip().strip("```").strip().replace('\n', ' ')

        return cleaned_sql_query

    def parse_sql_component(self):
        """
        Returns a function component that parses responses to SQL queries.

        This method creates a function component that can be used in a query pipeline to parse responses
        from a language model into SQL queries.

        Returns:
            FnComponent: A function component that parses responses to SQL queries.
        """
        return FnComponent(fn=self.parse_response_to_sql)