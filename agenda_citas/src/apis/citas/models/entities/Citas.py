from utils.DateFormat import DateFormat

class Cita:
    def __init__(self, id_cita, id_paciente, fecha_hora, motivo, estado, nombre_paciente=None):
        self.id_cita = id_cita
        self.id_paciente = id_paciente
        self.fecha_hora = fecha_hora 
        self.motivo = motivo
        self.estado = estado
        self.nombre_paciente = nombre_paciente

    def to_JSON(self):
        return {
            "id_cita": self.id_cita,
            "id_paciente": self.id_paciente,
            "fecha_hora": self.fecha_hora,
            "motivo": self.motivo,
            "estado": self.estado,
            "nombre_paciente": self.nombre_paciente
        }

