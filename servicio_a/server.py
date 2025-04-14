from concurrent import futures
import grpc
import saludo_personalizado_pb2_grpc as saludo_a_grpc
import saludo_personalizado_pb2 as saludo_a_pb2

import sys
sys.path.append('../servicio_b')
import saludo_base_pb2 as saludo_b_pb2
import saludo_base_pb2_grpc as saludo_b_grpc

class SaludadorPersonalizado(saludo_a_grpc.SaludadorPersonalizadoServicer):
    def SaludoCompleto(self, request, context):
        canal_b = grpc.insecure_channel('localhost:50052')
        stub_b = saludo_b_grpc.SaludadorBaseStub(canal_b)

        respuesta_base = stub_b.Saludar(saludo_b_pb2.SaludoRequest(nombre=request.nombre))

        mensaje_final = f"{respuesta_base.mensaje}, espero que tengas un buen día"
        return saludo_a_pb2.SaludoCompletoReply(mensaje=mensaje_final)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    saludo_a_grpc.add_SaludadorPersonalizadoServicer_to_server(SaludadorPersonalizado(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Servicio A escuchando en el puerto 50053")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()