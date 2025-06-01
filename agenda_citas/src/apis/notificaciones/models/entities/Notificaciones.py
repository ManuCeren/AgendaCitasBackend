from utils.DateFormat import DateFormat

class Notificaciones:
    def __init__(self, id_notificacion, id_cita, fecha_envio, medio, estado):
        self.id_notificacion = id_notificacion
        self.id_cita = id_cita
        self.fecha_envio = DateFormat.convert_date(fecha_envio)
        self.medio = medio
        self.estado = estado

def to_JSON(self):
    return {
        "id_paciente": self.id_notificacion,
        "id_cita": self.id_cita,
        "Fecha y hora": self.fecha_envio,
        "Motivo": self.medio,
        "Estado": self.estado

    }