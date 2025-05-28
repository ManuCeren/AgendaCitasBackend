from database.database import get_connection
from apis.pacientes.models.entities.Pacientes import Pacientes


class PacientesModels:

    @classmethod
    def get_all_pacientes(cls):
        try:
            connection = get_connection()
            pacientes_list = []
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_paciente, nombre, fecha_nacimiento, email
                    FROM pacientes
                    ORDER BY fecha_nacimiento DESC
                """)
                resultset = cursor.fetchall()
                for row in resultset:
                    paciente = Pacientes(
                        id_paciente=row[0],
                        nombre=row[1],
                        fecha_nacimiento=row[2],
                        email=row[3]
                    )
                    pacientes_list.append(paciente.to_JSON())
            connection.close()
            return pacientes_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_paciente_by_id(cls, id_paciente):
        try:
            connection = get_connection()
            paciente_json = None
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_paciente, nombre, fecha_nacimiento, email
                    FROM pacientes
                    WHERE id_paciente = %s
                """, (id_paciente,))
                row = cursor.fetchone()
                if row:
                    paciente = Pacientes(
                        id_paciente=row[0],
                        nombre=row[1],
                        fecha_nacimiento=row[2],
                        email=row[3]
                    )
                    cliente_json = paciente.to_JSON()
            connection.close()
            return paciente_json
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_paciente(cls, paciente: Pacientes):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pacientes (id_paciente, nombre, fecha_nacimiento, email)
                    VALUES (%s, %s, %s, %s)
                """, (
                    paciente.id_paciente,
                    paciente.nombre,
                    paciente.fecha_nacimiento,
                    paciente.email
                ))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_paciente(cls, paciente: Pacientes):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE pacientes
                    SET nombre = %s,
                        fecha_nacimiento = %s,
                        email = %s
                    WHERE id_paciente = %s
                """, (
                    paciente.nombre,
                    paciente.fecha_nacimiento,
                    paciente.email,
                    paciente.id_paciente
                ))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_paciente(cls, paciente: Pacientes):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM pacientes
                    WHERE id_paciente = %s
                """, (paciente.id_paciente,))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)