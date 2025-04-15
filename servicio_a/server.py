import traceback
from concurrent import futures
import grpc
import saludo_personalizado_pb2 as saludo_a_pb2
import saludo_personalizado_pb2_grpc as saludo_a_grpc
import saludo_base_pb2 as saludo_b_pb2
import saludo_base_pb2_grpc as saludo_b_grpc

class SaludadorPersonalizado(saludo_a_grpc.SaludadorPersonalizadoServicer):
    def SaludoCompleto(self, request, context):
        try:
            print("[A] Conectando a servicio-b:50052...", flush=True)
            canal_b = grpc.insecure_channel('servicio-b:50052')
            print("[A] Canal listo", flush=True)

            stub_b = saludo_b_grpc.SaludadorBaseStub(canal_b)
            respuesta_base = stub_b.Saludar(saludo_b_pb2.SaludoRequest(nombre=request.nombre))

            mensaje_final = f"{respuesta_base.mensaje}, espero que tengas un buen día"
            return saludo_a_pb2.SaludoCompletoReply(mensaje=mensaje_final)

        except Exception as e:
            print("[A] Error al contactar con servicio B:", flush=True)
            traceback.print_exc()
            return saludo_a_pb2.SaludoCompletoReply(mensaje="Error interno al contactar con servicio base.")


def serve():
    print("SERVICIO A", flush=True)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    saludo_a_grpc.add_SaludadorPersonalizadoServicer_to_server(SaludadorPersonalizado(), server)
    server.add_insecure_port('[::]:50053')
    print("[A] Servicio A escuchando en el puerto 50053", flush=True)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
