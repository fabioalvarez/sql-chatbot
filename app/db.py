from sqlalchemy import text, Sequence, Row, Connection, create_engine, Engine
import os


def create_db_url() -> str:
    """
    Creates a database URL from environment variables.

    This function retrieves PostgresSQL connection details from environment variables and constructs
    a database URL in the format required by SQLAlchemy.

    Returns:
        str: The constructed PostgresSQL database URL.

    Raises:
        ValueError: If one or more required environment variables are not set or are empty.
    """
    postgres_user = os.getenv("POSTGRES_USER", "")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "")
    postgres_host = os.getenv("POSTGRES_HOST", "")
    postgres_port = os.getenv("POSTGRES_PORT", "")
    postgres_db = os.getenv("POSTGRES_DB", "")

    if not all([postgres_user, postgres_password, postgres_host, postgres_port, postgres_db]):
        raise ValueError("One or more POSTGRES environment variables are not set or are empty.")

    return (f"postgresql+psycopg2://"
            f"{postgres_user}:"
            f"{postgres_password}@"
            f"{postgres_host}:"
            f"{postgres_port}/"
            f"{postgres_db}")


def init_db_engine() -> Engine:
    try:
        # Create the database engine using the URL from environment variables
        postgres_uri = create_db_url()
        engine = create_engine(postgres_uri)

    except ValueError as e:
        # Raise an error if the database engine creation fails
        raise ValueError(f"error occurred while creating db engine: {e}")

    return engine


def get_db_connection(engine):
    """
    Retrieves a database connection from the given engine.

    This function connects to the database using the provided SQLAlchemy engine.

    Args:
        engine (Engine): The SQLAlchemy engine connected to the database.

    Returns:
        Connection: The database connection object.

    Raises:
        ValueError: If the engine is not initialized.
    """
    if engine:
        return engine.connect()
    else:
        raise ValueError("Engine is not initialized.")


def get_table_rows(conn: Connection, table: str) -> Sequence[Row]:
    """
    Retrieves rows from a specified table.

    This function executes a SQL query to fetch the first 5 rows from the specified table.

    Args:
        conn (Connection): The database connection object.
        table (str): The name of the table to retrieve rows from.

    Returns:
        Sequence[Row]: A sequence of rows from the table.

    Raises:
        ValueError: If the connection is not initialized.
    """
    if conn is None:
        raise ValueError("Connection is not initialized.")
    query = text(f"SELECT * FROM {table} LIMIT 5;")
    exe = conn.execute(query)
    results = exe.fetchall()
    result = [row for row in results]
    return result


def get_all_tables(conn) -> list[str]:
    """
    Retrieves all table names from the database.

    This function executes a SQL query to fetch the names of all tables in the public schema.

    Args:
        conn (Connection): The database connection object.

    Returns:
        list[str]: A list of table names.

    Raises:
        ValueError: If the connection is not initialized.
    """
    if conn is None:
        raise ValueError("Connection is not initialized.")
    query = text("""
    SELECT table_name FROM 
    information_schema.tables 
    WHERE table_schema = 'public' 
      AND table_type = 'BASE TABLE';
    """)
    exe = conn.execute(query)
    results = exe.fetchall()
    return [row[0] for row in results]
