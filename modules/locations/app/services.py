import os
import psycopg2
from geoalchemy2.functions import ST_Point

import location_pb2
import location_pb2_grpc

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )

        cursor = conn.cursor()
        query = "INSERT INTO location (person_id, coordinate) VALUES (%s, ST_Point(%s, %s))"

        new_location = (
            request.person_id,
            request.latitude,
            request.longitude,
        )

        cursor.execute(query, new_location)
        conn.commit()

        location = {
            "person_id": request.person_id,
            "latitude": request.latitude,
            "longitude": request.longitude,
        }
        return location_pb2.LocationMessage(**location)
