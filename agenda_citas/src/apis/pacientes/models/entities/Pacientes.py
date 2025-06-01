from utils.DateFormat import DateFormat
import datetime

class Pacientes:
    def __init__(self, id_paciente, nombre, fecha_nacimiento, email, telefono=None):
        self.id_paciente = id_paciente
        self.nombre = nombre
        # 🔥 CORREGIDO → siempre será datetime.date o string YYYY-MM-DD:
        self.fecha_nacimiento = DateFormat.convert_date(fecha_nacimiento)
        self.email = email
        self.telefono = telefono

    def to_JSON(self):
        return {
            "id_paciente": self.id_paciente,
            "nombre": self.nombre,
            "fecha_nacimiento": (
                self.fecha_nacimiento.strftime('%Y-%m-%d')
                if isinstance(self.fecha_nacimiento, datetime.date)
                else self.fecha_nacimiento
            ),
            "email": self.email,
            "telefono": self.telefono
        }
