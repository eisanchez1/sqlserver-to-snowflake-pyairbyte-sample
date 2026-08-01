# SQL Server to Snowflake Replication with PyAirbyte

This project demonstrates how to replicate Microsoft SQL Server tables to Snowflake using **PyAirbyte** with the official **Airbyte SQL Server Source** and **Snowflake Destination** connectors.

Unlike the typical Airbyte deployment, this sample does **not** require:

* Airbyte Cloud
* Airbyte OSS (Core)
* An Airbyte web UI

Instead, PyAirbyte orchestrates the official Airbyte connectors directly from Python. The connectors are automatically downloaded and executed as Docker containers.

## Features

* Replicate SQL Server tables to Snowflake
* Uses the official Airbyte SQL Server source connector
* Uses the official Airbyte Snowflake destination connector
* Performs a **Full Refresh** replication
* Creates destination tables automatically
* Uses Snowflake Key Pair Authentication
* Stores configuration in a `.env` file
* Simple, lightweight Python implementation

## Prerequisites

Before running the sample, install the following:

* Python 3.11 or later (or a compatible version supported by PyAirbyte)
* Docker
* A SQL Server database
* A Snowflake account
* A Snowflake user configured for Key Pair Authentication

The Docker service must be running before executing the script.

For Linux:

```bash
sudo systemctl start docker
```

## Installation

Clone the repository.

```bash
git clone https://github.com/<your-account>/sqlserver-to-snowflake-pyairbyte-sample.git

cd sqlserver-to-snowflake-pyairbyte-sample
```

Create and activate a virtual environment.

```bash
python -m venv .venv

source .venv/bin/activate
```

Install the required packages.

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root.

Example:

```text
SQLSERVER_HOST=
SQLSERVER_PORT=1433
SQLSERVER_DATABASE=
SQLSERVER_USERNAME=
SQLSERVER_PASSWORD=

SNOWFLAKE_HOST=
SNOWFLAKE_DATABASE=
SNOWFLAKE_SCHEMA=AIRBYTE
SNOWFLAKE_WAREHOUSE=
SNOWFLAKE_ROLE=
SNOWFLAKE_USERNAME=
SNOWFLAKE_PASSWORD=

PRIVATE_KEY_FILE=
PRIVATE_KEY_PASSWORD=
```
The project contains a .env.example, so you don't type them manually.

The private key file should be readable only by its owner.

For Linux:

```bash
chmod 600 your_private_key.p8
```

## Running the Sample

Execute:

```bash
python main.py
```

The script performs the following steps:

1. Creates a SQL Server source connector.
2. Creates a Snowflake destination connector.
3. Selects the tables to replicate.
4. Performs a Full Refresh.
5. Writes the data into Snowflake.

## Tables Replicated

This sample replicates the following tables:

* customers
* products
* orders
* order_items

Below is the database diagram:

![Diagram](/images/source-db-diagram.png "Database Diagram")

Modify the `TABLES` list in `main.py` to replicate different tables.

## Snowflake Destination

The destination connector creates the required destination objects automatically.

In this sample, the source tables belong to the `dbo` schema in SQL Server. During replication, the connector preserves the source namespace and creates the destination tables under the `DBO` schema in Snowflake.

## Project Structure

```text
.
├── .env
├── .env.example
├── config.py
├── main.py
├── requirements.txt
└── README.md
```
## Sample Output

Below is a sample runtime output in my own Terminal:

![Sample Output](/images/airbyte-pipeline-results.png)

Below is the replication result in Snowflake:

![Snowflake Replicated Tables](/images/airbyte-snowflake-tables-list.png)

Airbyte added a few columns in each table for tracking changes:
![Replicated Products table with added columns](/images/airbyte-snowflake-additional-table-columns.png)

Finally, here's a sample preview of one of the tables:

![Sample data preview](/images/airbyte-snowflake-products-data-preview.png)

## Notes

This project uses:

* PyAirbyte
* Official Airbyte SQL Server Source connector
* Official Airbyte Snowflake Destination connector

During testing, the following approach successfully replicated the data:

```python
destination.write(
    source_data=source,
    cache=False,
    force_full_refresh=True
)
```

Using a `ReadResult` produced by `source.read()` as the input to `destination.write()` did not work for this SQL Server-to-Snowflake scenario during testing. Passing the `Source` object directly proved to be the successful approach.

## License

This sample is provided for educational purposes.
