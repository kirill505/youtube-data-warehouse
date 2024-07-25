
# YouTube Data Warehouse

## Project Overview

This is a data engineering project designed to collect, store, process, and analyze YouTube channel and video data. The project utilizes various technologies such as PostgreSQL, ClickHouse, DBT, Apache Spark, and Apache Airflow to create a robust data warehouse that provides valuable insights into YouTube data.

## Dataset
I used Trending YouTube Video Statistics datasets on Kaggle: https://www.kaggle.com/datasets/datasnaek/youtube-new

## Features

- **Data Collection:** Extract data from the YouTube API and store it in an OLTP database (PostgreSQL).
- **Data Processing:** Use Apache Spark for efficient ETL (Extract, Transform, Load) operations.
- **Data Transformation:** Manage data transformations and layers using DBT (Data Build Tool).
- **Data Warehousing:** Store and query processed data in an OLAP database (ClickHouse).
- **Pipeline Management:** Automate and schedule ETL pipelines using Apache Airflow.
- **Data Visualization:** Integrate with Metabase and Apache Superset for insightful data visualization and reporting.

## Technologies Used

- **PostgreSQL:** OLTP database for storing raw data.
- **ClickHouse:** OLAP database for storing processed data and supporting analytical queries.
- **DBT:** Tool for data transformation and management of data models.
- **Apache Spark:** Engine for large-scale data processing and ETL operations.
- **Apache Airflow:** Platform to programmatically author, schedule, and monitor workflows.
- **Metabase:** Business intelligence tool for creating dashboards and visualizations.
- **Apache Superset:** Modern data exploration and visualization platform.

## Project Structure

1. **Data Collection:**
    - Extract data from YouTube API.
    - Store raw data in PostgreSQL.

2. **Data Processing with Spark:**
    - Perform ETL operations on raw data.
    - Load processed data into ClickHouse.

3. **Data Transformation with DBT:**
    - Create staging, integration, and data warehouse layers.
    - Define and manage data models.

4. **Pipeline Automation with Airflow:**
    - Schedule and manage ETL pipelines.
    - Ensure timely updates of data.

5. **Data Visualization:**
    - Use Metabase and Apache Superset to create dashboards and reports.

## Getting Started

### Prerequisites

- Docker (recommended for easier setup of services)
- Python 3.7+
- PostgreSQL
- ClickHouse
- Apache Spark
- Apache Airflow
- DBT
- Metabase
- Apache Superset
