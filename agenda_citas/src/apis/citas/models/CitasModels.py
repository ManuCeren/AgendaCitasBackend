from database.database import get_connection
from apis.citas.models.entities.Citas import Cita

class CitaModel:
    @classmethod
    def get_all_citas(cls):
        try:
            connection = get_connection()
            citas_list = []
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.id_cita, c.id_paciente, p.nombre, c.fecha_hora, c.motivo, c.estado
                    FROM citas c
                    INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                    ORDER BY c.fecha_hora DESC
                """)
                resultset = cursor.fetchall()
                for row in resultset:
                    cita = Cita(
                        id_cita=row[0],
                        id_paciente=row[1],
                        nombre_paciente=row[2],
                        fecha_hora=row[3],
                        motivo=row[4],
                        estado=row[5]
                    )
                    citas_list.append(cita.to_JSON())
            connection.close()
            return citas_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_cita_by_id(cls, id_cita):
        try:
            connection = get_connection()
            cita_json = None
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.id_cita, c.id_paciente, p.nombre, c.fecha_hora, c.motivo, c.estado
                    FROM citas c
                    INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                    WHERE c.id_cita = %s
                """, (id_cita,))
                row = cursor.fetchone()
                if row:
                    cita = Cita(
                        id_cita=row[0],
                        id_paciente=row[1],
                        nombre_paciente=row[2],
                        fecha_hora=row[3],
                        motivo=row[4],
                        estado=row[5]
                    )
                    cita_json = cita.to_JSON()
            connection.close()
            return cita_json
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_cita(cls, cita: Cita):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO citas (id_cita, id_paciente, fecha_hora, motivo, estado)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    cita.id_cita,
                    cita.id_paciente,
                    cita.fecha_hora,
                    cita.motivo,
                    cita.estado
                ))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_cita(cls, cita: Cita):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(""" 
                    UPDATE citas
                    SET id_paciente = %s,
                        fecha_hora = %s,
                        motivo = %s,
                        estado = %s
                    WHERE id_cita = %s
                """, (
                    cita.id_paciente,
                    cita.fecha_hora,
                    cita.motivo,
                    cita.estado,
                    cita.id_cita
                ))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_cita_by_id(cls, id_cita):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM citas
                    WHERE id_cita = %s
                """, (id_cita,))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

