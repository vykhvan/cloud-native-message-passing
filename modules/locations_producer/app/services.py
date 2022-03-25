import os
import json
import location_pb2
import location_pb2_grpc
from kafka import KafkaProducer


KAFKA_SERVER = os.environ["KAFKA_SERVER"]

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):

        kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        
        location = {
            "person_id": request.person_id,
            "latitude": request.latitude,
            "longitude": request.longitude,
        }

        kafka_data = json.dumps(location).encode()
        kafka_producer.send("location", kafka_data)
        kafka_producer.flush()

        return location_pb2.LocationMessage(**location)
