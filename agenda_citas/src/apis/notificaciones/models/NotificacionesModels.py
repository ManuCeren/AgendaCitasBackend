from database.database import get_connection
from apis.notificaciones.models.entities.Notificaciones import Notificaciones

class NotificacionesModels:
    @classmethod
    def get_all_notificaciones(cls):
        try:
            connection = get_connection()
            notificaciones_list = []
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_notificacion, id_cita,  fecha_envio, medio, estado
                    FROM notificaciones
                    ORDER BY fecha_envio DESC
                """)
                resultset = cursor.fetchall()
                for row in resultset:
                    notificaion = Notificaciones(
                        id_notificacio=row[0],
                        id_cita=row[1],
                        fecha_envio=row[2],
                        medio=row[3],
                        estado=row[4]
                    )
                    notificaciones_list.append(notificaion.to_JSON())
            connection.close()
            return notificaciones_list
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_notificacion_by_id(cls, id_notificacion):
        try:
            connection = get_connection()
            notificacion_json = None
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_notificacion, id_cita, fecha_envio, medio, estado
                    FROM notificaciones
                    WHERE id_notificacion = %s
                """, (id_notificacion,))
                row = cursor.fetchone()
                if row:
                    notificacion = Notificaciones(
                        id_notificacio=row[0],
                        id_cita=row[1],
                        fecha_envio=row[2],
                        medio=row[3],
                        estado=row[4]
                    )
                    notificacion_json = notificacion.to_JSON()
            connection.close()
            return notificacion_json
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_notificacion(cls, notificacion: Notificaciones):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO notificaciones (id_notificacion, id_cita, fecha_envio, medio, estado)
                    VALUES (%s, %s, %s, %s,%s)
                """, (
                    notificacion.id_notificacion,
                    notificacion.id_cita,
                    notificacion.fecha_envio,
                    notificacion.medio,
                    notificacion.estado
                ))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_notificacion(cls, notificacion: Notificaciones):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(""" 
                               UPDATE notificaciones
                    SET id_cita = %s,
                        fecha_envio = %s,
                        medio = %s,
                        estado = %s
                    WHERE id_cita = %s
                """, (
                    notificacion.id_cita,
                    notificacion.fecha_envio,
                    notificacion.medio,
                    notificacion.estado
                ))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_notificacion(cls, notificacion: Notificaciones):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM citas
                    WHERE id_cita = %s
                """, (notificacion.id_notificacion,))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)