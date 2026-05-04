from abc import ABC, abstractmethod
import datetime

# ==============================
# ARCHIVO LOG
# ==============================
def registrar_log(mensaje):
    with open("log.txt", "a") as archivo:
        archivo.write(f"{datetime.datetime.now()} - {mensaje}\n")


# ==============================
# EXCEPCIONES PERSONALIZADAS
# ==============================
class ErrorCliente(Exception):
    pass

class ErrorServicio(Exception):
    pass

class ErrorReserva(Exception):
    pass


# ==============================
# CLASE ABSTRACTA BASE
# ==============================
class Entidad(ABC):
    @abstractmethod
    def mostrar_info(self):
        pass


# ==============================
# CLASE CLIENTE
# ==============================
class Cliente(Entidad):
    def __init__(self, nombre, edad):
        try:
            if not nombre:
                raise ErrorCliente("Nombre vacío")
            if edad <= 0:
                raise ErrorCliente("Edad inválida")

            self.nombre = nombre
            self.edad = edad

        except Exception as e:
            registrar_log(f"Error en cliente: {e}")
            raise

    def mostrar_info(self):
        return f"Cliente: {self.nombre}, Edad: {self.edad}"


# ==============================
# CLASE ABSTRACTA SERVICIO
# ==============================
class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self):
        pass


# ==============================
# SERVICIOS (HERENCIA + "SOBRECARGA")
# ==============================
class ReservaSala(Servicio):
    def calcular_costo(self, horas=1, descuento=0, impuesto=0):
        costo = self.precio_base * horas
        costo -= costo * descuento
        costo += costo * impuesto
        return costo


class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias=1, descuento=0, impuesto=0):
        costo = self.precio_base * dias
        costo -= costo * descuento
        costo += costo * impuesto
        return costo


class Asesoria(Servicio):
    def calcular_costo(self, sesiones=1, descuento=0, impuesto=0):
        costo = self.precio_base * sesiones
        costo -= costo * descuento
        costo += costo * impuesto
        return costo


# ==============================
# CLASE RESERVA
# ==============================
class Reserva:
    def __init__(self, cliente, servicio):
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"
        print("Reserva confirmada")

    def cancelar(self):
        self.estado = "Cancelada"
        print("Reserva cancelada")

    def procesar(self):
        try:
            if self.servicio is None:
                raise ErrorReserva("Servicio no disponible")

            costo = self.servicio.calcular_costo()

        except Exception as e:
            registrar_log(f"Error al calcular costo: {e}")
            raise ErrorReserva("No se pudo procesar la reserva") from e

        else:
            self.confirmar()
            print(f"Costo total: {costo}")

        finally:
            print("Intento de procesamiento finalizado")


# ==============================
# LISTAS DEL SISTEMA
# ==============================
clientes = []
servicios = []
reservas = []


# ==============================
# SIMULACIÓN (10 OPERACIONES)
# ==============================
def simulacion():
    try:
        # Cliente válido
        c1 = Cliente("Juan", 25)
        clientes.append(c1)

        # Cliente inválido
        try:
            c2 = Cliente("", -5)
        except:
            pass

        # Servicios
        s1 = ReservaSala("Sala VIP", 100)
        s2 = AlquilerEquipo("Laptop", 50)
        s3 = Asesoria("Consultoría", 200)

        servicios.extend([s1, s2, s3])

        # Reservas correctas
        r1 = Reserva(c1, s1)
        r1.procesar()
        reservas.append(r1)

        r2 = Reserva(c1, s2)
        r2.procesar()
        reservas.append(r2)

        r3 = Reserva(c1, s3)
        r3.procesar()
        reservas.append(r3)

        # Uso de "sobrecarga"
        print("\nReserva con descuento:")
        print(s1.calcular_costo(horas=2, descuento=0.1))

        print("\nReserva con impuesto:")
        print(s2.calcular_costo(dias=3, impuesto=0.19))

        # Error forzado
        try:
            r4 = Reserva(c1, None)
            r4.procesar()
        except Exception as e:
            registrar_log(f"Reserva inválida: {e}")

        # Cancelar y confirmar
        r3.cancelar()
        r2.confirmar()

        # Mostrar cliente
        print(c1.mostrar_info())

    except Exception as e:
        registrar_log(f"Error general: {e}")


simulacion()