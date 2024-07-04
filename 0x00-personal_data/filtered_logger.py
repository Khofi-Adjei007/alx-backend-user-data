#!/usr/bin/env python3
"""
Module for replacing occurrences of certain field values using regex.
"""
import re
from typing import List
import logging
import mysql.connector
import os


class RedactingFormatter(logging.Formatter):
    """
    Custom logging formatter to redact specified fields in log messages.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter.

        Args:
            fields (List[str]): List of fields to redact in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by redacting specified fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record with redacted fields.
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establish and return a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: Database
        connection instance.
    """
    db_connection = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connection


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscate specified fields in a log message using regex.

    Args:
        fields (List[str]): List of fields to redact.
        redaction (str): The string to replace the field
        values with.
        message (str): The original log message.
        separator (str): The character that separates
        key-value pairs in the message.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    Create and configure a logger for user data.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def main() -> None:
    """
    Connect to the database, retrieve all rows from
    the users table,
    and log each row with sensitive data redacted.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    field_names = [field[0] for field in cursor.description]
    logger = get_logger()

    for row in cursor:
        log_message_parts = [
            f'{field}={str(value)}; '
            for value, field in zip(row, field_names)
        ]
        log_message = ''.join(log_message_parts)
        logger.info(log_message.strip())

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
