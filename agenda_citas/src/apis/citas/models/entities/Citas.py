from utils.DateFormat import DateFormat

class Cita:
    def __init__(self, id_cita, id_paciente, fecha_hora, motivo, estado):
        self.id_cita = id_cita
        self.id_paciente = id_paciente
        self.fecha_hora = DateFormat.convert_datetime(fecha_hora)
        self.motivo = motivo
        self.estado = estado

    def to_JSON(self):
        return {
            "id_cita": self.id_cita,
            "id_paciente": self.id_paciente,
            "Fecha y hora": self.fecha_hora,
            "Motivo": self.motivo,
            "Estado": self.estado

        }
