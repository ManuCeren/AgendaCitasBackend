from database.database import get_connection
from apis.telefonos.models.entities.Telefonos import Telefonos


class TelefonosModels:

    @classmethod
    def get_all_telefonos(cls):
        try:
            connection = get_connection()
            telefonos_list = []
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_telefono, id_paciente, numero_telefono
                    FROM telefonos
                """)
                resultset = cursor.fetchall()
                for row in resultset:
                    telefono = Telefonos(
                        id_telefono=row[0],
                        id_paciente=row[1],
                        numero_telefono=row[2]
                    )
                    telefonos_list.append(telefono.to_JSON())
            connection.close()
            return telefonos_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_telefono_by_id(cls, id_telefono):
        try:
            connection = get_connection()
            telefono_json = None
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_telefono, id_paciente, numero_telefono
                    FROM telefonos
                    WHERE id_telefono = %s
                """, (id_telefono,))
                row = cursor.fetchone()
                if row:
                    telefono = Telefonos(
                        id_telefono=row[0],
                        id_paciente=row[1],
                        numero_telefono=row[2]
                    )
                    telefono_json = telefono.to_JSON()
            connection.close()
            return telefono_json
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_telefono(cls, telefono: Telefonos):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO telefonos (id_telefono, id_paciente, numero_telefono)
                    VALUES (%s, %s, %s, %s)
                """, (
                    telefono.id_telefono,
                    telefono.id_paciente,
                    telefono.numero_telefono
                ))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_telefono(cls, telefono: Telefonos):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE telefonos
                    SET id_paciente = %s,
                        numero_telefono = %s
                    WHERE id_telefono = %s
                """, (
                    telefono.id_paciente,
                    telefono.numero_telefono,
                    telefono.id_telefono
                ))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_telefono(cls, telefono: Telefonos):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM telefonos
                    WHERE id_telefono = %s
                """, (telefono.id_telefono,))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
