from database.database import get_connection
from apis.pacientes.models.entities.Pacientes import Pacientes
from datetime import date   # 👈 agregar esta línea

class PacientesModels:

    @classmethod
    def get_all_pacientes(cls):
        try:
            connection = get_connection()
            pacientes_list = []
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.id_paciente, p.nombre, p.fecha_nacimiento, p.email, t.numero_telefono
                    FROM pacientes p
                    LEFT JOIN telefonos t ON p.id_paciente = t.id_paciente
                    ORDER BY p.fecha_nacimiento DESC;
                """)
                resultset = cursor.fetchall()
                for row in resultset:
                    paciente = Pacientes(
                        id_paciente=row[0],
                        nombre=row[1],
                        fecha_nacimiento=row[2],
                        email=row[3],
                        telefono=row[4]  # puede ser NULL si no tiene teléfono
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
                    SELECT p.id_paciente, p.nombre, p.fecha_nacimiento, p.email, t.numero_telefono
                    FROM pacientes p
                    LEFT JOIN telefonos t ON p.id_paciente = t.id_paciente
                    WHERE p.id_paciente = %s
                """, (id_paciente,))
                row = cursor.fetchone()
                if row:
                    paciente = Pacientes(
                        id_paciente=row[0],
                        nombre=row[1],
                        fecha_nacimiento=row[2],
                        email=row[3],
                        telefono=row[4]
                    )
                    paciente_json = paciente.to_JSON()
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
                    date.fromisoformat(paciente.fecha_nacimiento),
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
                    # ✅ conversión correcta a date:
                    date.fromisoformat(paciente.fecha_nacimiento),
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
