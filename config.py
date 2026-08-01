import os

from dotenv import load_dotenv

load_dotenv()

def get_env(name: str) -> str:
    """Retrieve the value of an environment variable and avoid None values.
    Args:
        name (str): The name of the environment variable to retrieve.
    Returns:
        str: The value of the environment variable converted to string.
        
    Raises:
        ValueError: If the environment variable is not set.
    """

    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable '{name}' is not set.")
    return value

SQLSERVER_HOST=get_env("SQLSERVER_HOST")
SQLSERVER_PORT=int(get_env("SQLSERVER_PORT"))  # port needs an int value, so we convert it from string to int
SQLSERVER_DATABASE=get_env("SQLSERVER_DATABASE")
SQLSERVER_USERNAME=get_env("SQLSERVER_USERNAME")
SQLSERVER_PASSWORD=get_env("SQLSERVER_PASSWORD")

SNOWFLAKE_HOST=get_env("SNOWFLAKE_HOST")
SNOWFLAKE_DATABASE=get_env("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA=get_env("SNOWFLAKE_SCHEMA")
SNOWFLAKE_WAREHOUSE=get_env("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_ROLE=get_env("SNOWFLAKE_ROLE")
SNOWFLAKE_USERNAME=get_env("SNOWFLAKE_USERNAME")
SNOWFLAKE_PASSWORD=get_env("SNOWFLAKE_PASSWORD")
PRIVATE_KEY_FILE=get_env("PRIVATE_KEY_FILE")
PRIVATE_KEY_PASSWORD=get_env("PRIVATE_KEY_PASSWORD")