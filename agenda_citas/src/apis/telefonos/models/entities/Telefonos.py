class Telefonos:
    def __init__(self, id_telefono, id_paciente, numero_telefono):
        self.id_telefono = id_telefono
        self.id_paciente = id_paciente
        self.numero_telefono = numero_telefono

    def to_JSON(self):
        return {
            "id_telefono": self.id_telefono,
            "id_paciente": self.id_paciente,
            "numero_telefono": self.numero_telefono
        }
