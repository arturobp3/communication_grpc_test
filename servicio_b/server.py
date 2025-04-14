from concurrent import futures
import grpc
import saludo_base_pb2
import saludo_base_pb2_grpc

class SaludadorBaseServicer(saludo_base_pb2_grpc.SaludadorBaseServicer):
    def Saludar(self, request, context):
        return saludo_base_pb2.SaludoReply(mensaje=f"Hola, {request.nombre}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    saludo_base_pb2_grpc.add_SaludadorBaseServicer_to_server(SaludadorBaseServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Servicio B escuchando en el puerto 50052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()