"""
Replicate SQL Server tables to Snowflake using PyAirbyte.

This sample demonstrates how to use the official Airbyte SQL Server
source connector and Snowflake destination connector without requiring
Airbyte Cloud or a self-hosted Airbyte instance. Docker is used to run
the connectors locally.
"""

import airbyte as ab
import datetime

import config

def create_source() -> ab.Source:
    """Create and configure the SQL Server source connector.

    Returns:
        ab.Source: A configured SQL Server source connector.
    """
    return ab.get_source(
        "source-mssql",
        config={
            "host": config.SQLSERVER_HOST,
            "port": config.SQLSERVER_PORT,
            "database": config.SQLSERVER_DATABASE,
            "username": config.SQLSERVER_USERNAME,
            "password": config.SQLSERVER_PASSWORD
        },
        install_if_missing=True         # installs source-mssql if not already installed (Requires Docker to be installed and running on the host machine)
    )

def create_destination() ->ab.Destination:
    """Create and configure the Snowflake destination connector.

    Reads the private key from the configured PEM/P8 file and uses
    key-pair authentication to connect to Snowflake.

    Returns:
        ab.Destination: A configured Snowflake destination connector.
    """

    # Read the PEM file contents into a string
    with open(file=config.PRIVATE_KEY_FILE, mode="r") as f:
        private_key_str = f.read()

    return ab.get_destination(
        "destination-snowflake",
        config={
            "host": config.SNOWFLAKE_HOST,
            "username": config.SNOWFLAKE_USERNAME,
            "password": config.SNOWFLAKE_PASSWORD,
            "database": config.SNOWFLAKE_DATABASE,
            "schema": config.SNOWFLAKE_SCHEMA,
            "warehouse": config.SNOWFLAKE_WAREHOUSE,
            "role": config.SNOWFLAKE_ROLE,
            "credentials": {
                "auth_type": "Key Pair Authentication",
                "private_key": private_key_str,
                "private_key_password": config.PRIVATE_KEY_PASSWORD
            }
        },
        install_if_missing=True             # installs destination-snowflake if not already installed (Requires Docker to be installed and running on the host machine)
    )

def main()-> None:
    """Replicate SQL Server tables to Snowflake using PyAirbyte.

    The script performs a full refresh of the selected tables using the
    official Airbyte SQL Server source connector and Snowflake destination
    connector.
    """

    TABLES = [
    "products",
    "customers",
    "orders",
    "order_items",
    ]

    print(f"Starting the ETL process at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

    source = create_source()

    source.select_streams(TABLES)

    dest = create_destination()
    write_result: ab.WriteResult = dest.write(
            source_data=source,
            cache=False,                    # Bypass the local DuckDB cache and stream directly from the
                                            # source connector to the destination connector.
            force_full_refresh=True,        # Replace the destination tables with a fresh copy of the source data.
        )

    print(
            f"Completed writing {write_result.processed_records:,} records "
            f"to destination at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
        )

if __name__ == "__main__":
    main()