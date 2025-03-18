Project Overview
This project involves creating a local REST API to facilitate the migration of data from CSV files into a new SQL database. The API is designed to handle three different tables: departments, jobs, and hired_employees. Additionally, the project includes endpoints to retrieve specific metrics from the data.

Section 1: API
Features
Upload CSV Data: The API can receive historical data from CSV files and load this data into the new database.
Batch Insert Transactions: The API supports batch insertion of transactions (from 1 to 1000 rows) with a single request.
Technologies Used
Flask: A lightweight WSGI web application framework in Python.
SQLAlchemy: An SQL toolkit and Object-Relational Mapping (ORM) library for Python.
Pandas: A data manipulation and analysis library for Python, used for reading CSV files.
Key Endpoints
/upload/<table_name> [POST]: Uploads data from a CSV file to a specified table (departments, jobs, or hired_employees).
/batch_insert [POST]: Inserts data in batches into a specified table.
Section 2: SQL
Metrics Endpoints
/metrics/quarterly_hires [GET]: Retrieves the number of employees hired for each job and department in 2021, divided by quarter.
/metrics/above_average_hires [GET]: Lists the IDs, names, and number of employees hired for each department that hired more employees than the average number of hires in 2021.
B
