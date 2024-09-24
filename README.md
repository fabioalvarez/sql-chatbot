# Text-to-SQL Query Pipeline

This project provides a pipeline for converting natural language queries into SQL queries using a language model.
The pipeline orchestrates the process of generating and executing SQL queries, retrieving relevant table information,
and synthesizing responses.

## Prerequisites

- Python 3.8+
- Docker
- Docker Compose

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-repo/text-to-sql-pipeline.git
    cd text-to-sql-pipeline
    ```

2. Create a `.env` file with the following environment variables:
    ```env
    POSTGRES_USER=your_postgres_user
    POSTGRES_PASSWORD=your_postgres_password
    POSTGRES_HOST=localhost
    POSTGRES_PORT=your_postgres_port
    POSTGRES_DB=your_postgres_db
    OPENAI_API_KEY=your_openai_api_key
    LOCAL_PERSISTENCE_PATH={your_local_persistence_path}/rest-text-to-sql/tableinfo
    ```

3. Build and start the Docker containers:
    ```sh
    docker-compose up --build
    ```
   
4. Run Text To SQL application file:
    ```sh
     streamlit run app/front.py
    ```

