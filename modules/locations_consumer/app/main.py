import os
import logging
import json
import os
import psycopg2
from kafka import KafkaConsumer

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

logging.basicConfig(level=logging.INFO)


class Consumer:
    def __init__(self):
        self._init_database()
        
    def _init_database(self):
        self.consumer = KafkaConsumer("location", bootstrap_servers=[KAFKA_SERVER])
        self.conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        self.cursor = self.conn.cursor()

    def consume_from_kafka(self):
        for message in self.consumer:
            kafka_data = message.value.decode("utf-8")
            location = json.loads(kafka_data)
            location = (
                int(location["person_id"]),
                float(location["latitude"]),
                float(location["longitude"]),
            )
            query = "INSERT INTO location (person_id, coordinate) VALUES (%s, ST_Point(%s, %s))"
            self.cursor.execute(query, location)
            self.conn.commit()


if __name__ == "__main__":

    consumer = Consumer()

    while True:
        consumer.consume_from_kafka()