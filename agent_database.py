import sqlite3
from sqlite3 import Error
from typing import List, Tuple, Dict, Union
import logging


class AgentDatabase:
    def __init__(self, database: str):
        """
        Initialize the SQLite database connection.
        :param database: Name of the database file, e.g., 'agent.db'
        """
        self.db_file = database
        self.connection = None

    def connect(self):
        """Establish a connection to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_file)
            logging.info("Connected to SQLite database")
        except Error as e:
            logging.error(f"Error connecting to SQLite: {e}")
            raise RuntimeError(f"Error connecting to SQLite: {e}")

    def close_connection(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logging.info("Connection to SQLite database closed")

    def create_new_table(self, table_name: str, schema: str):
        """
        Create a new table in the SQLite database.
        :param table_name: Name of the table
        :param schema: Schema of the table, e.g., "(id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
        """
        try:
            self.connect()
            with self.connection:
                self.connection.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {schema}")
            logging.info(f"Table '{table_name}' created or already exists")
        except Error as e:
            logging.error(f"Error creating table '{table_name}': {e}")
            raise RuntimeError(f"Error creating table '{table_name}': {e}")
        finally:
            self.close_connection()

    def insert(self, table_name: str, columns: List[str], values: Tuple):
        """
        Insert data into a table.
        :param table_name: Name of the table
        :param columns: List of column names
        :param values: Tuple of values to insert
        """
        try:
            self.connect()
            with self.connection:
                placeholders = ", ".join(["?"] * len(values))
                query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                self.connection.execute(query, values)
            logging.info("Data inserted successfully into '%s'", table_name)
        except Error as e:
            logging.error(f"Error inserting data into table '{table_name}': {e}")
            raise RuntimeError(f"Error inserting data into table '{table_name}': {e}")
        finally:
            self.close_connection()

    def delete(self, table_name: str, condition: str):
        """
        Delete data from a table.
        :param table_name: Name of the table
        :param condition: SQL condition string, e.g., "id = 1"
        """
        try:
            self.connect()
            with self.connection:
                query = f"DELETE FROM {table_name} WHERE {condition}"
                self.connection.execute(query)
            logging.info(f"Data deleted successfully from '{table_name}' where {condition}")
        except Error as e:
            logging.error(f"Error deleting data from table '{table_name}': {e}")
            raise RuntimeError(f"Error deleting data from table '{table_name}': {e}")
        finally:
            self.close_connection()

    def select(self, table_name: str, columns: Union[str, List[str]] = "*", condition: str = None) -> List[Dict]:
        """
        Select data from a table.
        :param table_name: Name of the table
        :param columns: List of columns to select or "*" for all columns
        :param condition: Optional SQL condition string, e.g., "id = 1"
        :return: List of rows as dictionaries
        """
        cursor = None
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = f"SELECT {columns} FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            cursor.execute(query)
            results = cursor.fetchall()
            logging.info(f"Data selected successfully from '{table_name}'")
            return results
        except Error as e:
            logging.error(f"Error selecting data from table '{table_name}': {e}")
            raise RuntimeError(f"Error selecting data from table '{table_name}': {e}")
        finally:
            if cursor:
                cursor.close()
            self.close_connection()

    def update(self, table_name: str, updates: Dict[str, Union[str, int]], where: Dict[str, Union[str, int]]):
        """
        Update data in a table.
        :param table_name: Name of the table
        :param updates: Dictionary of column-value pairs to update
        :param where: Dictionary of column-value pairs for the WHERE clause
        """
        try:
            self.connect()
            with self.connection:
                set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
                set_values = list(updates.values())

                where_clause = " AND ".join([f"{key} = ?" for key in where.keys()])
                where_values = list(where.values())

                query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
                self.connection.execute(query, set_values + where_values)
            logging.info(f"Data updated successfully in '{table_name}'")
        except Error as e:
            logging.error(f"Error updating data in table '{table_name}': {e}")
            raise RuntimeError(f"Error updating data in table '{table_name}': {e}")
        finally:
            self.close_connection()