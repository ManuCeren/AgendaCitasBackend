from utils.DateFormat import DateFormat


class Pacientes:
    def __init__(self, id_paciente, nombre, fecha_nacimiento, email):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.email = email

    def to_JSON(self):
        return {
            "id_paciente": self.id_paciente,
            "nombre": self.nombre,
            "fecha_nacimiento": self.fecha_nacimiento,
            "email": self.email  
        }