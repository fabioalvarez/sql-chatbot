table_summary = """\
Give me a summary of the table with the following JSON format.

- The table name must be unique to the table and describe it while being concise. 
- Do NOT output a generic table name (e.g. table, my_table).

Do NOT make the table name one of the following: {exclude_table_name_list}

Table:
{table_str}

Summary: """

# NOTE: taken from langchain and adapted
# https://github.com/langchain-ai/langchain/blob/v0.0.303/libs/langchain/langchain/chains/sql_database/prompt.py
text_to_sql = (
    "Given an input question, first create a syntactically correct {dialect} "
    "query to run, then look at the results of the query and return the answer. "
    "You can order the results by a relevant column to return the most "
    "interesting examples in the database.\n\n"
    "Never query for all the columns from a specific table, only ask for a "
    "few relevant columns given the question.\n\n"
    "Pay attention to use only the column names that you can see in the schema "
    "description. "
    "Always give alias to the tables and use them in the query, use with the right columns "
    "in order to avoid errors. \n\n"
    "Answer only what you were asked for, do not add any additional information."
    "Be careful to not query for columns that do not exist. "
    "Pay attention to which column is in which table. "
    "Also, qualify column names with the table name when needed. "
    "You are required to use the following format, each taking one line:\n\n"
    "Question: Question here\n"
    "SQLQuery: SQL Query to run\n"
    "SQLResult: Result of the SQLQuery\n"
    "Answer: Final answer here\n\n"
    "Only use tables listed below.\n"
    "{schema}\n\n"
    "Question: {question}\n"
    "SQLQuery: "
)

question_synthesis = """\
Given an input question, synthesize a response from the query results.\n"
If the user ask a question that is not related to get information from the database, 
you should answer with a generic response.\n"
"Question: {question}\n"
"SQL: {sql_query}\n"
"SQL Response: {context_str}\n"
"Response: """