from concurrent import futures
import grpc
import saludo_base_pb2
import saludo_base_pb2_grpc
import traceback

class SaludadorBaseServicer(saludo_base_pb2_grpc.SaludadorBaseServicer):
    def Saludar(self, request, context):
        print(f"[B] Recibido nombre: {request.nombre}", flush=True)
        return saludo_base_pb2.SaludoReply(mensaje=f"Hola, {request.nombre}")

def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        saludo_base_pb2_grpc.add_SaludadorBaseServicer_to_server(SaludadorBaseServicer(), server)
        server.add_insecure_port('0.0.0.0:50052')
        print("[B] Servicio B escuchando en el puerto 50052", flush=True)
        server.start()
        server.wait_for_termination()
    except Exception as e:
        print("[B] Error al arrancar servicio B:", flush=True)
        traceback.print_exc()

if __name__ == '__main__':
    serve()
