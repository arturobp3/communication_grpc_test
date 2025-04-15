import grpc
import saludo_personalizado_pb2
import saludo_personalizado_pb2_grpc

def run():
    canal = grpc.insecure_channel('127.0.0.1:49783') # url del servicio a en minikube
    stub = saludo_personalizado_pb2_grpc.SaludadorPersonalizadoStub(canal)

    nombre = input("Como te llamas? ")
    respuesta = stub.SaludoCompleto(saludo_personalizado_pb2.SaludoCompletoRequest(nombre=nombre))

    print("Respuesta del servidor: ", respuesta.mensaje)

if __name__ == '__main__':
    run()

