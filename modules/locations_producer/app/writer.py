import grpc
import location_pb2
import location_pb2_grpc

channel = grpc.insecure_channel("localhost:30001")
stub = location_pb2_grpc.LocationServiceStub(channel)


location = location_pb2.LocationMessage(person_id=24, latitude=43.233485, longitude=76.922217)

response = stub.Create(location)

print(response)
