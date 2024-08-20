
# YouTube Data Warehouse

## Project Overview

This is a data engineering project designed to collect, store, process, and analyze YouTube channel and video data. The project utilizes various technologies such as PostgreSQL, ClickHouse, DBT, Apache Spark, and Apache Airflow to create a robust data warehouse that provides valuable insights into YouTube data.

## Dataset
I used Trending YouTube Video Statistics datasets on Kaggle: https://www.kaggle.com/datasets/datasnaek/youtube-new

## What I have done:
- Configured Data Models for OLTP Database (PostgreSQL): Designed and set up relational data models to efficiently handle transactional operations
- Developed APIs for Parsing YouTube Video and Channel Information: Implemented RESTful APIs to retrieve and process data related to YouTube videos and channels
- Created a DAG for Downloading Top 200 YouTube Videos
- Implemented an asynchronous mechanism for recording transactions into the database
- Configured Kafka: Set up a Kafka producer to regularly trigger the task of parsing the top 200 popular videos and a Kafka consumer to handle the processing of this data
- Created docker-compose.yaml File for Deployment.

## Project plan

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
