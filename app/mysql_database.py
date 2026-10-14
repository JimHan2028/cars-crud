from pathlib import Path
import pymysql
import os
from pymysql.cursors import DictCursor


def connect():
    return pymysql.connect(
        host=os.environ["MYSQL_HOST"],
        port=int(os.environ["MYSQL_PORT"]),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        cursorclass=DictCursor
    )


def initialize(_database_path: Path) -> None:
    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
CREATE TABLE IF NOT EXISTS cars (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
make VARCHAR(60) NOT NULL,
model VARCHAR(60) NOT NULL,
year INT NOT NULL,
color VARCHAR(40) NOT NULL DEFAULT '',
CONSTRAINT valid_make CHECK (CHAR_LENGTH(TRIM(make)) > 0),
CONSTRAINT valid_model CHECK (CHAR_LENGTH(TRIM(model)) > 0),
CONSTRAINT valid_year CHECK (year BETWEEN 1886 AND 2100)
) CHARACTER SET utf8mb4
""")
        connection.commit()
    finally:
        connection.close()


def list_cars(_database_path: Path):
    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, make, model, year, color FROM cars")
            return cursor.fetchall()
    finally:
        connection.close()


def get_car(_database_path: Path, car_id: int):
    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, make, model, year, color FROM cars WHERE id = %s", (car_id,))
            return cursor.fetchone()
    finally:
        connection.close()


def create_car(_database_path: Path, car):
    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO cars(make, model, year, color) VALUES (%s, %s, %s, %s)",
                (car.make, car.model, car.year, car.color)
            )
            connection.commit()
            return cursor.lastrowid
    finally:
        connection.close()


def update_car(_database_path: Path, car_id: int, car):
    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE cars SET make=%s, model=%s, year=%s, color=%s WHERE id=%s",
                (car.make, car.model, car.year, car.color, car_id)
            )
            connection.commit()
            return cursor.rowcount > 0
    finally:
        connection.close()


def delete_car(_database_path: Path, car_id: int):
    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM cars WHERE id = %s", (car_id,))
            connection.commit()
            return cursor.rowcount > 0
    finally:
        connection.close()
