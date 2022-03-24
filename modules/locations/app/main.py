from concurrent import futures
import grpc
from services import LocationServicer
import location_pb2_grpc


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)
    print("Server starting on port 5005")
    server.add_insecure_port("[::]:5005")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
