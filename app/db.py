import mysql.connector


class DbConnection:
    def __init__(self, host, port, user, password, database):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password
        }
        self.database = database
        self.connection = None

    def get_connection(self):
        self.connection = mysql.connector.connect(**self.config)

        if not self.connection.is_connected:
            raise ConnectionError("Couldn't connect to the database")

        return self.connection

    def create_table(self):
        cnx = self.get_connection()
        create_statement = """
                CREATE TABLE IF NOT EXISTS weapons (
                id INT AUTO_INCREMENT PRIMARY KEY,
                weapon_id VARCHAR(255),
                weapon_name VARCHAR(255),
                weapon_type VARCHAR(255),
                range_km INT,
                weight_kg FLOAT,
                manufacturer VARCHAR(255),
                origin_country VARCHAR(255),
                storage_location VARCHAR(255),
                year_estimated INT,
                risk_level VARCHAR(255)
                );"""

        with cnx.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")

            cursor.execute(f"USE {self.database}")

            cursor.execute(create_statement)
            self.connection.commit()

    def insert_weapon(self, weapons):
        cnx = self.get_connection()

        insert_statement = """INSERT INTO weapons (
                    weapon_id, weapon_name, weapon_type,
                    range_km, weight_kg, manufacturer, origin_country, storage_location, year_estimated, risk_level)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ;"""

        values = [tuple(weapon.values()) for weapon in weapons]

        with cnx.cursor(dictionary=True) as cursor:
            cursor.execute('SELECT COUNT(*) FROM weapons;')
            length_before = cursor.fetchone()[0]

            cursor.execute(f"USE {self.database}")

            if len(values) > 1:
                cursor.executemany(insert_statement, values)
            elif len(values) == 1:
                cursor.execute(insert_statement, values[0])
            else:
                raise ValueError("No weapons to insert")

            cursor.execute('SELECT COUNT(*) FROM weapons;')
            length_after = cursor.fetchone()

        cnx.commit()
        return {
            "status": "success",
            "inserted_records": int(length_after)-int(length_before)
        }
